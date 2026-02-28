from dataclasses import dataclass

from insta_wizard.mobile.commands._responses.user.info import (
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


@dataclass(slots=True, kw_only=True)
class UserInfo(Command[UserInfoResponse]):
    """Get user info by user_id"""

    user_id: str


class UserInfoHandler(CommandHandler[UserInfo, UserInfoResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self._api = api
        self._state = state

    async def __call__(self, command: UserInfo) -> UserInfoResponse:
        data = await self._api.call_api(
            method="GET",
            uri=constants.USERS_USER_INFO_URI.format(user_id=command.user_id),
            client_endpoint="feed_timeline",
        )
        return data
