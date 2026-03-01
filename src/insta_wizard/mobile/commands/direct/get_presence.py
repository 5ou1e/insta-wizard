from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.responses.direct.get_presence import (
    DirectV2GetPresenceResponse,
)


@dataclass(slots=True)
class DirectV2GetPresence(Command[DirectV2GetPresenceResponse]):
    suggested_followers_limit: str | None = None  # "100"


class DirectV2GetPresenceHandler(CommandHandler[DirectV2GetPresence, DirectV2GetPresenceResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: DirectV2GetPresence) -> DirectV2GetPresenceResponse:
        params = {}
        if command.suggested_followers_limit is not None:
            params["suggested_followers_limit"] = command.suggested_followers_limit

        resp = await self.requester.call_api(
            method="GET",
            uri=constants.DIRECT_V2_GET_PRESENCE_URI,
            params=params,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(DirectV2GetPresenceResponse, resp)
