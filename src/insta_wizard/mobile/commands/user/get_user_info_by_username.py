from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.user.user_info import (
    UserInfoResponse,
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
class UserUsernameInfo(Command[UserInfoResponse]):
    """Получить информацию о пользователе по его username"""

    username: str


class UserUsernameInfoHandler(CommandHandler[UserUsernameInfo, UserInfoResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self._api = api
        self._state = state

    async def __call__(self, command: UserUsernameInfo) -> UserInfoResponse:
        data = await self._api.call_api(
            method="GET",
            uri=constants.USERS_USERNAME_INFO_URI.format(username=command.username),
        )
        return cast(UserInfoResponse, data)
