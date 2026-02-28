from __future__ import annotations

import orjson

from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.common.transport.base import (
    HttpTransport,
)
from insta_wizard.common.transport.exceptions import (
    TransportNetworkError,
    TransportTimeoutError,
)
from insta_wizard.common.transport.models import (
    HttpMethod,
    HttpRequest,
    ResponseInfo,
    TransportResponse,
)
from insta_wizard.web.common.headers_factory import (
    WebClientHeadersFactory,
)
from insta_wizard.web.exceptions import (
    BadRequestError,
    CheckpointRequiredError,
    InstagramResponseError,
    NetworkError,
    TooManyRequestsError,
    UnexpectedRedirectResponseError,
    UnexpectedResponseContentTypeError,
    WebClientError,
)
from insta_wizard.web.models.other import CheckpointRequiredErrorData
from insta_wizard.web.models.state import WebClientState


class WebApiRequester:
    def __init__(
        self,
        state: WebClientState,
        headers_factory: WebClientHeadersFactory,
        transport: HttpTransport,
        logger: InstagramClientLogger,
    ):
        self.state = state
        self.headers = headers_factory
        self.transport = transport
        self.logger = logger

    def _parse_response_body(self, response: TransportResponse) -> dict | str:
        content = response.content

        p = b"for (;;);"
        if content.startswith(p):
            content = content[len(p) :].lstrip()

        try:
            return orjson.loads(content)
        except orjson.JSONDecodeError:
            if response.headers.get("Transfer-Encoding") == "chunked":
                try:
                    lines = [line for line in content.splitlines() if line.strip()]
                    return {"chunked_ig_response_content": [orjson.loads(line) for line in lines]}
                except Exception:
                    pass

            return content.decode("utf-8", errors="replace")

    async def _execute_request(self, request: HttpRequest) -> dict:
        try:
            response = await self.transport.send(request, follow_redirects=False)
        except (TransportTimeoutError, TransportNetworkError) as e:
            raise NetworkError(message=str(e)) from e

        self._update_state_from_response_headers(response)

        body = self._parse_response_body(response)

        self.logger.response(resp=response, body=body)

        if 300 <= response.status < 400:
            raise UnexpectedRedirectResponseError(
                response=ResponseInfo(
                    status=response.status,
                    headers=response.headers,
                    json=None,
                    text=body,
                ),
                request_url=request.url,
                location="not implemented",
            )

        if not (200 <= response.status < 300):
            error = self.parse_error_from_response(request, response, body)
            raise error

        if not isinstance(body, dict):
            response_info = ResponseInfo(
                status=response.status,
                headers=response.headers,
                json=None,
                text=body,
            )
            raise UnexpectedResponseContentTypeError(
                response=response_info, expected="JSON", returned=type(body).__name__
            )

        return body

    def _update_state_from_response_headers(self, response: TransportResponse):
        www_claim = response.headers.get("x-ig-set-www-claim")
        if www_claim is not None:
            self.state.local_data.www_claim = www_claim

    def parse_error_from_response(
        self,
        request: HttpRequest,
        response: TransportResponse,
        data: dict | str,
    ) -> WebClientError:
        status = response.status

        if isinstance(data, dict):
            response_info = ResponseInfo(
                status=response.status,
                headers=response.headers,
                json=data,
                text=None,
            )

            message = data.get("message", "")
            if status == 400:
                if "checkpoint_required" in message:
                    return CheckpointRequiredError(
                        response=response_info,
                        checkpoint_data=CheckpointRequiredErrorData.from_dict(data),
                    )
                return BadRequestError(response=response_info)

        else:
            response_info = ResponseInfo(
                status=response.status,
                headers=response.headers,
                json=None,
                text=data,
            )
        if status == 429:
            return TooManyRequestsError(response=response_info)

        return InstagramResponseError(response=response_info)

    async def execute(
        self,
        method: HttpMethod,
        url: str,
        data=None,
        params=None,
        extra_headers=None,
    ) -> dict:
        headers = self.headers.api_headers()

        if method == "POST":
            headers["Origin"] = "https://www.instagram.com"  # Не используется для GET запросов
            headers["Content-type"] = "application/x-www-form-urlencoded"

            if self.state.local_data.ajax_hash:
                headers["X-Instagram-Ajax"] = self.state.local_data.ajax_hash

        if extra_headers:
            headers.update(extra_headers)

        return await self._execute_request(
            HttpRequest(method=method, url=url, headers=headers, data=data, params=params)
        )
