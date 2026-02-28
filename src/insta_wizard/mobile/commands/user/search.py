from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import (
    utc_offset_from_timezone,
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
from insta_wizard.mobile.responses.user.search_users import UserSearchResponse


@dataclass(slots=True)
class UserSearch(Command[UserSearchResponse]):
    query: str
    count: int = 30


class UserSearchHandler(CommandHandler[UserSearch, UserSearchResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: UserSearch) -> UserSearchResponse:
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
        return cast(UserSearchResponse, data)
