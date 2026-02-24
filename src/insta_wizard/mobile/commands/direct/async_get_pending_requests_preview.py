from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.async_get_pending_requests_preview import (
    DirectV2AsyncGetPendingRequestsPreviewResponse,
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
class DirectV2AsyncGetPendingRequestsPreview(
    Command[DirectV2AsyncGetPendingRequestsPreviewResponse]
):
    pass


class DirectV2AsyncGetPendingRequestsPreviewHandler(
    CommandHandler[
        DirectV2AsyncGetPendingRequestsPreview,
        DirectV2AsyncGetPendingRequestsPreviewResponse,
    ]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: DirectV2AsyncGetPendingRequestsPreview,
    ) -> DirectV2AsyncGetPendingRequestsPreviewResponse:
        resp = await self.api.call_api(
            method="GET",
            uri=constants.DIRECT_V2_ASYNC_GET_PENDING_REQUESTS_PREVIEW_URI,
            params={"pending_inbox_filters": "[]"},
            client_endpoint="feed_timeline",
            extra_headers={
                "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            },
        )
        return cast(DirectV2AsyncGetPendingRequestsPreviewResponse, resp)
