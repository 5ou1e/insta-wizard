from __future__ import annotations

import asyncio

import orjson
from yarl import URL

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
    TransportResponse,
    ResponseInfo,
)
from insta_wizard.common.utils import (
    auth_data_from_authorization_header,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.headers_factory import (
    MobileClientHeadersFactory,
)
from insta_wizard.mobile.exceptions import (
    BadRequestError,
    ChallengeRequiredError,
    FeedbackRequiredError,
    InstagramBackend572Error,
    InstagramResponseError,
    LoginRequiredError,
    MethodNotAllowedError,
    MobileClientError,
    NetworkError,
    NotFoundError,
    OopsAnErrorOccurred,
    PayloadReturnedIsNullError,
    TooManyRequestsError,
    UnauthorizedError,
    UnexpectedResponseContentTypeError,
    NodeTaoSystemExceptionError,
)
from insta_wizard.mobile.models.challenge import (
    ChallengeRequiredData,
    FeedbackRequiredData,
)
from insta_wizard.mobile.models.state import MobileClientState

HEADER_MAPPINGS = {
    "ig-set-password-encryption-key-id": "public_key_id",
    "ig-set-password-encryption-pub-key": "public_key",
    "ig-set-x-mid": "mid",
    "ig-set-ig-u-ds-user-id": "user_id",
    "ig-set-ig-u-shbid": "shbid",
    "ig-set-ig-u-shbts": "shbts",
    "ig-set-ig-u-rur": "rur",
    "ig-set-ig-u-ig-direct-region-hint": "direct_region_hint",
    "ig-set-csrftoken": "csrftoken",
}


class ApiRequestExecutor:
    def __init__(
        self,
        client_state: MobileClientState,
        transport: HttpTransport,
        logger: InstagramClientLogger,
    ):
        self.state = client_state
        self.transport = transport
        self.logger = logger
        self.headers = MobileClientHeadersFactory(
            state=self.state,
        )

    def _build_api_request(
        self,
        method: HttpMethod,
        uri: str,
        data: dict | bytes | None = None,
        params: dict | None = None,
        extra_headers: dict | None = None,
        friendly_name: str | None = None,
        client_endpoint: str | None = None,
        b_api: bool = False,
        web_api: bool = False,
    ) -> HttpRequest:
        if b_api:
            url = URL(constants.INSTAGRAM_API_B_V1_URL) / uri
        else:
            url = URL(constants.INSTAGRAM_API_V1_URL) / uri

        if web_api:
            url = URL("https://www.instagram.com/api/v1") / uri

        headers = self.headers.api_headers()

        if friendly_name is not None:
            headers.update({"X-Fb-Friendly-Name": friendly_name})
        else:
            headers.update({"X-Fb-Friendly-Name": f"IgApi: {uri}"})

        if client_endpoint is not None:
            headers.update({"X-Ig-Client-Endpoint": client_endpoint})
        else:
            headers.update({"X-Ig-Client-Endpoint": "unknown"})

        if method == "POST":
            headers.update(
                {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                }
            )

        if extra_headers:
            headers.update(extra_headers)

        return HttpRequest(
            method=method,
            url=url,
            data=data,
            headers=headers,
            params=params,
        )

    async def call_web_api(
        self,
        method: HttpMethod,
        uri: str,
        data: dict | bytes | None = None,
        params: dict | None = None,
        extra_headers: dict | None = None,
        friendly_name: str | None = None,
        client_endpoint: str | None = None,
    ):
        request = self._build_api_request(
            method=method,
            uri=uri,
            data=data,
            params=params,
            extra_headers=extra_headers,
            friendly_name=friendly_name,
            client_endpoint=client_endpoint,
            web_api=True,
        )

        return await self._execute_request(request=request)

    async def call_api(
        self,
        method: HttpMethod,
        uri: str,
        data: dict | bytes | None = None,
        params: dict | None = None,
        extra_headers: dict | None = None,
        friendly_name: str | None = None,
        client_endpoint: str | None = None,
    ):
        return await self._execute_request(
            self._build_api_request(
                method=method,
                uri=uri,
                data=data,
                params=params,
                extra_headers=extra_headers,
                friendly_name=friendly_name,
                client_endpoint=client_endpoint,
            )
        )

    async def call_b_api(
        self,
        method: HttpMethod,
        uri: str,
        data: dict | bytes | None = None,
        params: dict | None = None,
        extra_headers: dict | None = None,
        friendly_name: str | None = None,
        client_endpoint: str | None = None,
    ):
        return await self._execute_request(
            self._build_api_request(
                method=method,
                uri=uri,
                data=data,
                params=params,
                extra_headers=extra_headers,
                friendly_name=friendly_name,
                client_endpoint=client_endpoint,
                b_api=True,
            )
        )

    async def _execute_request(self, request: HttpRequest) -> dict:
        response, elapsed_ms = await self._send(request)
        data = self._parse_response_body(response)

        self.logger.response(response, data)

        self._update_state_from_response_headers(response)
        self.state.increment_request_stats(
            len(response.content) if response.content else 0,
            elapsed_ms,
        )

        if response.status != 200:
            error = self.parse_error_from_response(request, response, data)
            raise error

        if not isinstance(data, dict):
            response_info = ResponseInfo(
                status=response.status,
                headers=response.headers,
                json=None,
                text=data,
            )
            raise UnexpectedResponseContentTypeError(
                response=response_info, expected="JSON", returned=type(data).__name__
            )

        return data

    async def _send(
        self,
        request: HttpRequest,
    ) -> tuple[TransportResponse, int]:
        start = asyncio.get_event_loop().time()
        try:
            resp = await self.transport.send(request)
            elapsed_ms = int((asyncio.get_event_loop().time() - start) * 1000)
            return resp, elapsed_ms

        except (TransportTimeoutError, TransportNetworkError) as e:
            raise NetworkError(message=str(e)) from e

    def _parse_response_body(self, response: TransportResponse) -> dict | str:
        content = response.content
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

    def _update_state_from_response_headers(self, response: TransportResponse):
        for header_name, attr_name in HEADER_MAPPINGS.items():
            if header_name not in response.headers:
                continue

            header_value = response.headers.get(header_name)
            setattr(self.state.local_data, attr_name, header_value)

        authorization_header = response.headers.get("ig-set-authorization")

        # Когда инстаграм сбрасывает куку, он присылает такую "Bearer IGT:2:"
        if isinstance(authorization_header, str):
            authorization_data = auth_data_from_authorization_header(authorization_header)
            self.state.local_data.set_authorization_data(authorization_data)

    def parse_error_from_response(
        self,
        request: HttpRequest,
        response: TransportResponse,
        body: dict | str,
    ) -> MobileClientError:
        status = response.status

        if isinstance(body, dict):
            response_info = ResponseInfo(
                status=response.status,
                headers=response.headers,
                json=body,
                text=None,
            )

            message = body.get("message", "").lower()

            if status == 400:
                if "challenge_required" in message:
                    challenge_data = body.get("challenge", {})
                    return ChallengeRequiredError(
                        challenge_data=ChallengeRequiredData.model_validate(challenge_data),
                        response_json=body,
                    )
                if "feedback_required" in message:
                    return FeedbackRequiredError(
                        data=FeedbackRequiredData(
                            feedback_title=body.get("feedback_title"),
                            feedback_url=body.get("feedback_url"),
                        ),
                        response=response_info,
                    )
                if "NodeTaoSystemException" in message:
                    return NodeTaoSystemExceptionError(response=response_info)

                return BadRequestError(response=response_info)

            if status == 401:
                return UnauthorizedError(response=response_info)

            if status == 403:
                if "login_required" in message:
                    return LoginRequiredError(response=response_info)
                return InstagramResponseError(response=response_info)

            if status == 404:
                if "payload returned is null" in message:
                    return PayloadReturnedIsNullError(response=response_info)
                return NotFoundError(response=response_info)

            if status == 429:
                return TooManyRequestsError(response=response_info)

            return InstagramResponseError(response=response_info)

        response_info = ResponseInfo(
            status=response.status,
            headers=response.headers,
            json=None,
            text=body,
        )

        if "oops, an error occurred" in body.lower():
            return OopsAnErrorOccurred(response=response_info)

        if status == 404:
            return NotFoundError(response=response_info)
        if status == 405:
            return MethodNotAllowedError(response=response_info)
        if status == 429:
            return TooManyRequestsError(response=response_info)
        if status == 572:
            return InstagramBackend572Error(response=response_info)

        return InstagramResponseError(response=response_info)
