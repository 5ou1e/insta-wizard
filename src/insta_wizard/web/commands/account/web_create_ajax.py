from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.common.password_encrypter import PasswordEncrypter
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.account.web_create_ajax import (
    WebCreateAjaxResponse,
)


@dataclass(slots=True)
class WebCreateAjax(Command[WebCreateAjaxResponse]):
    """Final account registration request"""

    username: str
    password: str
    first_name: str
    phone_number: str
    day: int
    month: int
    year: int
    sms_code: int | str


class WebCreateAjaxHandler(CommandHandler[WebCreateAjax, WebCreateAjaxResponse]):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: WebCreateAjax) -> WebCreateAjaxResponse:
        self.state.csrftoken_guard()
        self.state.machine_id_guard()
        self.state.encryption_info_guard()

        jazoest = generate_jazoest(self.state.csrftoken)

        enc_password = PasswordEncrypter.encrypt(
            password=command.password,
            encryption_info=self.state.encryption_info,
            prefix="PWD_INSTAGRAM_BROWSER",
        )

        # TODO extra_session_id - возможно тоже самое что x-web-sessionid
        data = {
            "enc_password": enc_password,
            "day": command.day,
            "failed_birthday_year_count": "{}",
            "first_name": command.first_name,
            "month": command.month,
            "phone_number": command.phone_number,
            "username": command.username,
            "year": command.year,
            "sms_code": command.sms_code,
            "client_id": self.state.mid,
            "seamless_login_enabled": 1,
            "tos_version": "row",
            "extra_session_id": "zd8xki:sy1uen:3131sz",
            "jazoest": jazoest,
        }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.WEB_ACCOUNTS_WEB_CREATE_AJAX_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com/accounts/emailsignup/",
            },
        )
        return cast(WebCreateAjaxResponse, resp)
