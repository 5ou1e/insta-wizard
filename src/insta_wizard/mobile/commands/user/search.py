from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import (
    utc_offset_from_timezone,
)
from insta_wizard.mobile.commands._responses.user.search_users import (
    UserSearchUsersResponse,
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
class UserSearchUsers(Command[UserSearchUsersResponse]):
    query: str
    count: int = 30


class UserSearchUsersHandler(CommandHandler[UserSearchUsers, UserSearchUsersResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: UserSearchUsers) -> UserSearchUsersResponse:
        params = {
            "timezone_offset": utc_offset_from_timezone(self.state.device.timezone),
            "q": command.query,
            "count": command.count,
        }

        data = await self.api.call_api(
            method="GET",
            uri=constants.USERS_SEARCH_URI,
            params=params,
        )
        return cast(UserSearchUsersResponse, data)
