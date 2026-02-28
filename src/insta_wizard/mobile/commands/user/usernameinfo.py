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
from insta_wizard.mobile.responses.user.usernameinfo import UserUsernameInfoResponse


@dataclass(slots=True)
class UserUsernameInfo(Command[UserUsernameInfoResponse]):
    """Get user info by username"""

    username: str


class UserUsernameInfoHandler(CommandHandler[UserUsernameInfo, UserUsernameInfoResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self._api = api
        self._state = state

    async def __call__(self, command: UserUsernameInfo) -> UserUsernameInfoResponse:
        data = await self._api.call_api(
            method="GET",
            uri=constants.USERS_USERNAME_INFO_URI.format(username=command.username),
        )
        return cast(UserUsernameInfoResponse, data)
