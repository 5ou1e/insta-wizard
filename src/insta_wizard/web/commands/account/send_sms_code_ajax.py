from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.commands._responses.account.send_sms_code_ajax import (
    SendSignupSmsCodeAjaxResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class SendSignupSmsCodeAjax(Command[SendSignupSmsCodeAjaxResult]):
    """Отправить код из смс при регистрации"""

    phone_number: str
    captcha_token: str | None = None


class SendSignupSmsCodeAjaxHandler(
    CommandHandler[SendSignupSmsCodeAjax, SendSignupSmsCodeAjaxResult]
):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: SendSignupSmsCodeAjax) -> SendSignupSmsCodeAjaxResult:
        self.state.csrftoken_guard()
        self.state.machine_id_guard()

        jazoest = generate_jazoest(self.state.csrftoken)

        data = {
            "client_id": self.state.mid,
            "phone_number": command.phone_number,
            "jazoest": jazoest,
        }
        if command.captcha_token is not None:
            data["captcha_token"] = command.captcha_token

        # Response example: {"sms_sent":false,"require_captcha":true,"status":"ok"}
        resp = await self.api_requester.execute(
            method="POST",
            url=constants.ACCOUNTS_SEND_SIGNUP_SMS_CODE_AJAX_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com/accounts/emailsignup/",
            },
        )
        return cast(SendSignupSmsCodeAjaxResult, resp)
