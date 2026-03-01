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
from insta_wizard.mobile.responses.user.web_profile_info import (
    UserWebProfileInfoResponse,
)


@dataclass(slots=True)
class UserWebProfileInfo(Command[UserWebProfileInfoResponse]):
    """Get user info by username (webprofileinfo)"""

    username: str


class UserWebProfileInfoHandler(CommandHandler[UserWebProfileInfo, UserWebProfileInfoResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self._state = state

    async def __call__(self, command: UserWebProfileInfo) -> UserWebProfileInfoResponse:
        # И так и так работает

        data = await self.requester.call_api(
            method="GET",
            uri=constants.USERS_WEB_PROFILE_INFO,
            params={"username": command.username},
        )

        # data = await self.requester.call_web_api(
        #     method="GET",
        #     uri=constants.USERS_WEB_PROFILE_INFO,
        #     params={"username": command.username},
        # )

        return cast(UserWebProfileInfoResponse, data)
