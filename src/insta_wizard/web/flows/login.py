from dataclasses import dataclass
from typing import TypeAlias

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.common.password_encrypter import PasswordEncrypter
from insta_wizard.web.commands.account.login_ajax import (
    AccountsLoginAjax,
)
from insta_wizard.web.common.command import (
    Command,
    CommandBus,
    CommandHandler,
)
from insta_wizard.web.common.state_initializer import (
    StateInitializer,
)
from insta_wizard.web.exceptions import (
    BadRequestError,
    LoginBadPasswordError,
)
from insta_wizard.web.models.state import WebClientState

LoginResult: TypeAlias = None


@dataclass(slots=True)
class Login(Command[LoginResult]):
    """Log in to account using username and password"""

    username: str
    password: str


class LoginHandler(CommandHandler[Login, LoginResult]):
    def __init__(
        self, state: WebClientState, initializer: StateInitializer, bus: CommandBus
    ) -> None:
        self.state = state
        self.initializer = initializer
        self.bus = bus

    async def __call__(self, command: Login) -> LoginResult:
        self.state.local_data.clear_cookies(["sessionid", "ds_user_id"])

        await self.initializer()

        self.state.csrftoken_guard()
        self.state.encryption_info_guard()

        enc_password = PasswordEncrypter.encrypt(
            password=command.password,
            encryption_info=self.state.encryption_info,
            prefix="PWD_INSTAGRAM_BROWSER",
        )

        jazoest = generate_jazoest(self.state.csrftoken)

        try:
            response = await self.bus.execute(
                AccountsLoginAjax(
                    username=command.username,
                    enc_password=enc_password,
                    jazoest=jazoest,
                )
            )
            if response.get("authenticated", False):
                return
            else:
                # status 200 - {"user":true,"authenticated":false,"status":"ok"}
                # raise UnknownLoginError(response_json=response)
                raise LoginBadPasswordError(response_json=response)

        except BadRequestError as e:
            # status 400
            response = e.response.json
            if "UserInvalidCredentials" in response.get("error_type", ""):
                raise LoginBadPasswordError(response_json=response)
            raise e
