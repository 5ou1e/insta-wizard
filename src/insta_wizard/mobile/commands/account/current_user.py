from dataclasses import dataclass

from insta_wizard.mobile.commands._responses.account.account_current_user import (
    AccountCurrentUserResponse,
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
class AccountCurrentUser(Command[AccountCurrentUserResponse]):
    """Получить информацию о текущем пользователе (требует авторизации)"""

    pass


class AccountCurrentUserHandler(CommandHandler[AccountCurrentUser, AccountCurrentUserResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: AccountCurrentUser) -> AccountCurrentUserResponse:
        resp = await self.api.call_api(
            method="GET",
            uri=constants.ACCOUNTS_CURRENT_USER_URI,
            params={"edit": "true"},
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return resp
