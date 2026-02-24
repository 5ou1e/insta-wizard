from __future__ import annotations

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
from insta_wizard.web.common.headers_factory import (
    WebClientHeadersFactory,
)
from insta_wizard.web.exceptions import (
    InstagramResponseError,
    NetworkError,
    NotFoundError,
    TooManyRequestsError,
    WebClientError,
)
from insta_wizard.web.models.state import WebClientState


class WebNavigator:
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

    async def _execute_request(self, request: HttpRequest) -> str:
        try:
            response = await self.transport.send(request)
        except (TransportTimeoutError, TransportNetworkError) as e:
            raise NetworkError(message=str(e)) from e
        body = response.content.decode("utf-8")

        self.logger.response(resp=response, body=body)

        if response.status != 200:
            error = self.parse_error_from_response(request, response, body)
            raise error

        return body

    def parse_error_from_response(
        self,
        request: HttpRequest,
        response: TransportResponse,
        data: dict | str,
    ) -> WebClientError:
        status = response.status

        response_info = ResponseInfo(
            status=response.status,
            headers=response.headers,
            json=None,
            text=data,
        )

        if status == 404:
            return NotFoundError(response=response_info, request_url=request.url)
        if status == 429:
            return TooManyRequestsError(response=response_info)

        return InstagramResponseError(response=response_info)

    async def navigate(
        self,
        url: str,
        method: HttpMethod = "GET",
        data=None,
        params=None,
        extra_headers=None,
    ) -> str:
        headers = self.headers.navigation_headers()
        if extra_headers:
            headers.update(extra_headers)

        return await self._execute_request(
            HttpRequest(
                method=method,
                url=url,
                headers=headers,
                data=data,
                params=params,
            )
        )
