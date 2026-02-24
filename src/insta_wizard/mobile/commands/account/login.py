from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.common.password_encrypter import (
    PasswordEncrypter,
)
from insta_wizard.mobile.commands._responses.account.account_login import (
    AccountLoginResponse,
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
class AccountLogin(Command[AccountLoginResponse]):
    """Отправить запрос на авторизацию в аккаунт с помощью логина и пароля"""

    username: str
    password: str


class AccountLoginHandler(CommandHandler[AccountLogin, AccountLoginResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: AccountLogin) -> AccountLoginResponse:
        enc_password = PasswordEncrypter.encrypt_v0(command.password)

        country_code = 1
        data = {
            "jazoest": generate_jazoest(self.state.device.phone_id),
            "country_codes": f'[{{"country_code":"{country_code}","source":["default"]}}]',
            "phone_id": self.state.device.phone_id,
            "enc_password": enc_password,
            "username": command.username,
            "adid": self.state.device.adid,
            "guid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "google_tokens": "[]",
            "login_attempt_count": "0",
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_LOGIN_URI,
            data=data,
        )
        return cast(AccountLoginResponse, resp)
