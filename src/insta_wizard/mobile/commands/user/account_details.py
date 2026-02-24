from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.user.user_account_details import (
    UserAccountDetailsResponse,
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
class UserAccountDetails(Command[UserAccountDetailsResponse]):
    user_id: str | int


class UserAccountDetailsHandler(CommandHandler[UserAccountDetails, UserAccountDetailsResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self._api = api
        self._state = state

    async def __call__(self, command: UserAccountDetails) -> UserAccountDetailsResponse:
        data = await self._api.call_api(
            method="GET",
            uri=constants.USERS_ACCOUNT_DETAILS_URI.format(user_id=command.user_id),
        )
        return cast(UserAccountDetailsResponse, data)
