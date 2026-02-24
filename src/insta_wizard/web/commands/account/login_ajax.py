from dataclasses import dataclass
from typing import cast

from insta_wizard.web.commands._responses.account.login_ajax import (
    AccountsLoginAjaxResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import (
    WebApiRequester,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class AccountsLoginAjax(Command[AccountsLoginAjaxResult]):
    """Авторизоваться в аккаунт с помощью логина и пароля"""

    username: str
    enc_password: str
    jazoest: str


class AccountsLoginAjaxHandler(CommandHandler[AccountsLoginAjax, AccountsLoginAjaxResult]):
    def __init__(
        self,
        api_requester: WebApiRequester,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: AccountsLoginAjax) -> AccountsLoginAjaxResult:

        data = {
            "enc_password": command.enc_password,
            "caaF2DebugGroup": 0,
            "isPrivacyPortalReq": "false",
            "loginAttemptSubmissionCount": 0,
            "optIntoOneTap": "false",
            "queryParams": {},
            "trustedDeviceRecords": {},
            "username": command.username,
            "jazoest": command.jazoest,
        }

        # Also works with "https://i.instagram.com/api/v1/web/accounts/login/ajax/",
        resp = await self.api_requester.execute(
            method="POST",
            url=constants.WEB_ACCOUNTS_LOGIN_AJAX_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com",
            },
        )
        return cast(AccountsLoginAjaxResult, resp)
