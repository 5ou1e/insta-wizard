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
from insta_wizard.mobile.responses.account.account_update_profile_name import (
    AccountUpdateProfileNameResponse,
)


@dataclass(slots=True)
class AccountUpdateProfileName(Command[AccountUpdateProfileNameResponse]):
    """Update account profile name"""

    first_name: str


class AccountUpdateProfileNameHandler(
    CommandHandler[AccountUpdateProfileName, AccountUpdateProfileNameResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: AccountUpdateProfileName) -> AccountUpdateProfileNameResponse:
        data = {
            "first_name": command.first_name,
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_UPDATE_PROFILE_NAME_URI,
            data=data,
            client_endpoint="EditFullNameFragment:profile_edit_full_name",
        )
        return cast(AccountUpdateProfileNameResponse, resp)
