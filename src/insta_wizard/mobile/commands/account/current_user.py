from dataclasses import dataclass

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
from insta_wizard.mobile.responses.account.account_current_user import (
    AccountCurrentUserResponse,
)


@dataclass(slots=True)
class AccountCurrentUser(Command[AccountCurrentUserResponse]):
    """Get current user info (requires authentication)"""

    pass


class AccountCurrentUserHandler(CommandHandler[AccountCurrentUser, AccountCurrentUserResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: AccountCurrentUser) -> AccountCurrentUserResponse:
        resp = await self.requester.call_api(
            method="GET",
            uri=constants.ACCOUNTS_CURRENT_USER_URI,
            params={"edit": "true"},
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return resp
