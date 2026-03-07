from dataclasses import dataclass

from insta_wizard.common.generators import generate_waterfall_id
from insta_wizard.common.interfaces import EmailCodeSignupProvider
from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.common.utils import current_datetime
from insta_wizard.mobile.commands.account.check_confirmation_code import (
    AccountCheckConfirmationCode,
)
from insta_wizard.mobile.commands.account.create import AccountCreate
from insta_wizard.mobile.commands.account.send_verify_email import AccountSendVerifyEmail
from insta_wizard.mobile.commands.account.username_suggestions import (
    AccountUsernameSuggestions,
)
from insta_wizard.mobile.commands.consent.get_signup_config import (
    ConsentGetSignupConfig,
)
from insta_wizard.mobile.common.command import (
    Command,
    CommandBus,
    CommandHandler,
)
from insta_wizard.mobile.exceptions import RegistrationError
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class RegisterAccountEmailFlowResult:
    created_user: dict
    email: str


@dataclass(slots=True)
class RegisterAccountEmailFlow(Command[RegisterAccountEmailFlowResult]):
    """Register an account using the code from the Email"""

    username: str
    password: str
    first_name: str
    day: int
    month: int
    year: int

    email_code_provider: EmailCodeSignupProvider


class RegisterAccountEmailFlowHandler(
    CommandHandler[RegisterAccountEmailFlow, RegisterAccountEmailFlowResult]
):
    def __init__(
        self,
        state: MobileClientState,
        bus: CommandBus,
        logger: InstagramClientLogger,
    ) -> None:
        self.state = state
        self.bus = bus
        self.logger = logger

    async def __call__(
        self,
        command: RegisterAccountEmailFlow,
    ) -> RegisterAccountEmailFlowResult:
        username = command.username
        password = command.password
        first_name = command.first_name
        day = command.day
        month = command.month
        year = command.year

        waterfall_id = generate_waterfall_id()

        self.logger.info("Requesting SignupConfig...")
        signup_config = await self.bus.execute(ConsentGetSignupConfig())
        tos_version = signup_config["tos_version"]

        email = await command.email_code_provider.provide_email()

        # Skip this request to avoid TooManyRequestError

        # self.logger.info("Checking availability of the email address...")
        # try:
        #     email_check = await self.bus.execute(
        #         UsersCheckEmail(email=email, waterfall_id=waterfall_id)
        #     )
        #     if email_check.get("status") != "ok":
        #         raise RegistrationError(
        #             msg=f"Probably email is not valid, response={email_check}"
        #         )
        # except BadRequestError as e:
        #     if e.response.json.get("error_type") == "missing_parameters":
        #         raise RegistrationError(
        #             msg=f"Email is not valid, response={e.response.json}"
        #         )
        #     raise e

        from_datetime = current_datetime()

        self.logger.info("Requesting SMS with code...")
        code_send = await self.bus.execute(
            AccountSendVerifyEmail(email=email, waterfall_id=waterfall_id)
        )
        if code_send.get("status") != "ok":
            raise RegistrationError(msg=f"Instagram didn't send the code, response={code_send}")
        if not code_send.get("email_sent"):
            raise RegistrationError(msg=f"Instagram didn't send the code, response={code_send}")

        code = await command.email_code_provider.provide_code(
            email=email, from_datetime=from_datetime
        )

        self.logger.info("Sending the code for verification...")
        code_validation = await self.bus.execute(
            AccountCheckConfirmationCode(
                email=email,
                code=code,
                waterfall_id=waterfall_id,
            )
        )
        if code_validation.get("status") != "ok":
            if code_validation.get("error_type") == "invalid_nonce":
                raise RegistrationError(msg=f"Invalid code, response={code_validation}")
            raise RegistrationError(
                msg=f"Unknown error while code submitting, response={code_validation}"
            )
        signup_code = code_validation.get("signup_code")
        if signup_code is None:
            raise RegistrationError(
                msg=f"Can't parse signup_code from response, response={code_validation}"
            )

        await self.bus.execute(
            AccountUsernameSuggestions(username=username, waterfall_id=waterfall_id)
        )

        self.logger.info("Sending a registration request...")
        creation_result = await self.bus.execute(
            AccountCreate(
                username=username,
                password=password,
                first_name=first_name,
                signup_code=signup_code,  # noqa
                email=email,
                day=day,
                month=month,
                year=year,
                tos_version=tos_version,
                waterfall_id=waterfall_id,
            )
        )
        created_user = creation_result.get("created_user", {})
        if created_user:
            self.logger.info(f"Registration success! created_user={created_user}")
            return RegisterAccountEmailFlowResult(
                created_user=created_user,
                email=email,
            )

        raise RegistrationError(
            msg=f"Unknown response for creation request, response={creation_result}"
        )
