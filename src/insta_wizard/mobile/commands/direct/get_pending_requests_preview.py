from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.get_pending_requests_preview import (
    DirectV2GetPendingRequestsPreviewResponse,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class DirectV2GetPendingRequestsPreview(Command[DirectV2GetPendingRequestsPreviewResponse]):
    pending_inbox_filters: list = None  # type: ignore[assignment]


class DirectV2GetPendingRequestsPreviewHandler(
    CommandHandler[
        DirectV2GetPendingRequestsPreview,
        DirectV2GetPendingRequestsPreviewResponse,
    ]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2GetPendingRequestsPreview
    ) -> DirectV2GetPendingRequestsPreviewResponse:
        pending = command.pending_inbox_filters if command.pending_inbox_filters is not None else []
        params = {"pending_inbox_filters": pending}
        resp = await self.api.call_api(
            method="GET",
            uri=constants.DIRECT_V2_GET_PENDING_REQUESTS_PREVIEW_URI,
            params=params,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(DirectV2GetPendingRequestsPreviewResponse, resp)
