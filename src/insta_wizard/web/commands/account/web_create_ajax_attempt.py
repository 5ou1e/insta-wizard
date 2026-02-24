from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.common.password_encrypter import PasswordEncrypter
from insta_wizard.web.commands._responses.account.web_create_ajax_attempt import (
    WebCreateAjaxAttemptResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class WebCreateAjaxAttempt(Command[WebCreateAjaxAttemptResult]):
    """Send account registration attempt request"""

    username: str
    password: str
    first_name: str
    phone_number: str


class WebCreateAjaxAttemptHandler(CommandHandler[WebCreateAjaxAttempt, WebCreateAjaxAttemptResult]):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: WebCreateAjaxAttempt) -> WebCreateAjaxAttemptResult:
        self.state.csrftoken_guard()
        self.state.machine_id_guard()
        self.state.encryption_info_guard()

        jazoest = generate_jazoest(self.state.csrftoken)

        enc_password = PasswordEncrypter.encrypt(
            password=command.password,
            encryption_info=self.state.encryption_info,
            prefix="PWD_INSTAGRAM_BROWSER",
        )

        data = {
            "enc_password": enc_password,
            "failed_birthday_year_count": "{}",
            "first_name": command.first_name,
            "phone_number": command.phone_number,
            "username": command.username,
            "client_id": self.state.mid,
            "seamless_login_enabled": 1,
            "opt_into_one_tap": "false",
            "use_new_suggested_user_name": "true",
            "jazoest": jazoest,
        }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.WEB_ACCOUNTS_WEB_CREATE_AJAX_ATTEMPT_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com/accounts/emailsignup/",
            },
        )
        return cast(WebCreateAjaxAttemptResult, resp)
