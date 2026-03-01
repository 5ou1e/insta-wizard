from dataclasses import dataclass
from typing import TypedDict, cast

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


class AccountsLogoutResponse(TypedDict):
    pass


@dataclass(slots=True)
class AccountsLogout(Command[AccountsLogoutResponse]):
    """Logout of account"""

    pass


class AccountsLogoutHandler(CommandHandler[AccountsLogout, AccountsLogoutResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: AccountsLogout) -> AccountsLogoutResponse:

        data = {
            "one_tap_app_login": True,
        }

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.ACCOUNTS_LOGOUT_URI,
            data=data,
        )
        return cast(AccountsLogoutResponse, resp)
