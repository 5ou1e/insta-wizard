from dataclasses import dataclass
from typing import cast, TypedDict


from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import (
    WebApiRequester,
)
from insta_wizard.web.models.state import WebClientState

class AccountsLogoutAjaxResult(TypedDict):
    pass

@dataclass(slots=True)
class AccountsLogoutAjax(Command[AccountsLogoutAjaxResult]):
    """Logout of account"""
    jazoest: str


class AccountsLogoutAjaxHandler(CommandHandler[AccountsLogoutAjax, AccountsLogoutAjaxResult]):
    def __init__(
        self,
        api_requester: WebApiRequester,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: AccountsLogoutAjax) -> AccountsLogoutAjaxResult:
        user_id = self.state.local_data.get_cookie("ds_user_id")
        data = {
            "one_tap_app_login": "0",
            **({"user_id": user_id} if user_id else {}),
            "jazoest": command.jazoest,
        }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.WEB_ACCOUNTS_LOGOUT_AJAX_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com",
            },
        )
        return cast(AccountsLogoutAjaxResult, resp)
