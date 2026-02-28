from dataclasses import dataclass
from typing import cast

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
from insta_wizard.mobile.responses.direct.has_interop_upgraded import (
    DirectV2HasInteropUpgradedResponse,
)


@dataclass(slots=True)
class DirectV2HasInteropUpgraded(Command[DirectV2HasInteropUpgradedResponse]):
    pass


class DirectV2HasInteropUpgradedHandler(
    CommandHandler[DirectV2HasInteropUpgraded, DirectV2HasInteropUpgradedResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2HasInteropUpgraded
    ) -> DirectV2HasInteropUpgradedResponse:
        resp = await self.api.call_api(
            method="GET",
            uri=constants.DIRECT_V2_HAS_INTEROP_UPGRADED,
            client_endpoint="feed_timeline",
            extra_headers={
                "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            },
        )
        return cast(DirectV2HasInteropUpgradedResponse, resp)
