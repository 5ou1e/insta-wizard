from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.get_presence_active_now import (
    DirectV2GetPresenceActiveNowResponse,
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
class DirectV2GetPresenceActiveNow(Command[DirectV2GetPresenceActiveNowResponse]):
    recent_thread_limit: int = 0
    suggested_followers_limit: int = 100


class DirectV2GetPresenceActiveNowHandler(
    CommandHandler[DirectV2GetPresenceActiveNow, DirectV2GetPresenceActiveNowResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2GetPresenceActiveNow
    ) -> DirectV2GetPresenceActiveNowResponse:
        params = {
            "recent_thread_limit": command.recent_thread_limit,
            "suggested_followers_limit": command.suggested_followers_limit,
        }

        resp = await self.api.call_api(
            method="GET",
            uri=constants.DIRECT_V2_GET_PRESENCE_ACTIVE_NOW_URI,
            params=params,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(DirectV2GetPresenceActiveNowResponse, resp)
