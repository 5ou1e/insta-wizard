from __future__ import annotations

import asyncio

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
    HttpRequest,
    TransportResponse,
    ResponseInfo,
)
from insta_wizard.common.utils import (
    auth_data_from_authorization_header,
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
    UnexpectedResponseContentTypeError,
    NodeTaoSystemExceptionError,
)
from insta_wizard.mobile.models.challenge import (
    ChallengeRequiredData,
    FeedbackRequiredData,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)

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


class RequestExecutor:
    def __init__(
        self,
        client_state: MobileClientState,
        transport: HttpTransport,
        logger: InstagramClientLogger,
    ):
        self._client_state = client_state
        self._transport = transport
        self.logger = logger

    async def __call__(self, request: HttpRequest) -> dict:
        response, elapsed_ms = await self._execute(request)
        data = self._parse_response_body(response.content)

        self.logger.response(response, data)

        self._update_state_from_response_headers(response)
        self._client_state.increment_request_stats(
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

    async def _execute(
        self,
        request: HttpRequest,
    ) -> tuple[TransportResponse, int]:
        start = asyncio.get_event_loop().time()
        try:
            resp = await self._transport.send(request)
            elapsed_ms = int((asyncio.get_event_loop().time() - start) * 1000)
            return resp, elapsed_ms

        except (TransportTimeoutError, TransportNetworkError) as e:
            raise NetworkError(message=str(e)) from e

    def _parse_response_body(self, content: bytes) -> dict | str:
        if not content:
            return ""

        try:
            return orjson.loads(content)
        except Exception as e:
            self.logger.warning(f"Ответ не в формате JSON: {e}")
            return content.decode("utf-8", errors="replace")

    def _update_state_from_response_headers(self, response: TransportResponse):
        for header_name, attr_name in HEADER_MAPPINGS.items():
            if header_name not in response.headers:
                continue

            header_value = response.headers.get(header_name)
            setattr(self._client_state.local_data, attr_name, header_value)

        authorization_header = response.headers.get("ig-set-authorization")

        # Когда инстаграм сбрасывает куку, он присылает такую "Bearer IGT:2:"
        if isinstance(authorization_header, str):
            authorization_data = auth_data_from_authorization_header(authorization_header)
            self._client_state.local_data.set_authorization_data(authorization_data)

    def parse_error_from_response(
        self,
        request: HttpRequest,
        response: TransportResponse,
        data: dict | str,
    ) -> MobileClientError:
        status = response.status

        if isinstance(data, dict):
            response_info = ResponseInfo(
                status=response.status,
                headers=response.headers,
                json=data,
                text=None,
            )

            message = data.get("message", "").lower()

            if status == 400:
                if "challenge_required" in message:
                    challenge_data = data.get("challenge", {})
                    return ChallengeRequiredError(
                        challenge_data=ChallengeRequiredData.model_validate(challenge_data),
                        response_json=data,
                    )
                if "feedback_required" in message:
                    return FeedbackRequiredError(
                        data=FeedbackRequiredData(
                            feedback_title=data.get("feedback_title"),
                            feedback_url=data.get("feedback_url"),
                        ),
                        response=response_info,
                    )
                if "NodeTaoSystemException" in message:
                    return NodeTaoSystemExceptionError(response=response_info)

                return BadRequestError(response=response_info)

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
            text=data,
        )

        if "oops, an error occurred" in data.lower():
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
