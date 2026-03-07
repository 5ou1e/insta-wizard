from dataclasses import dataclass

from insta_wizard.common.generators import generate_waterfall_id
from insta_wizard.common.interfaces import Number, PhoneSmsCodeProvider
from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.mobile.commands.account.create_validated import (
    AccountCreateValidated,
)
from insta_wizard.mobile.commands.account.send_signup_sms_code import (
    AccountSendSignupSmsCode,
)
from insta_wizard.mobile.commands.account.username_suggestions import (
    AccountUsernameSuggestions,
)
from insta_wizard.mobile.commands.account.validate_signup_sms_code import (
    AccountValidateSignupSmsCode,
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
class RegisterAccountSMSFlowResult:
    created_user: dict
    number: str | Number


@dataclass(slots=True)
class RegisterAccountSMSFlow(Command[RegisterAccountSMSFlowResult]):
    """Register an account via SMS (phone number)"""

    username: str
    password: str
    first_name: str
    day: int
    month: int
    year: int

    phone_code_provider: PhoneSmsCodeProvider


class RegisterAccountSMSFlowHandler(
    CommandHandler[RegisterAccountSMSFlow, RegisterAccountSMSFlowResult]
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
        command: RegisterAccountSMSFlow,
    ) -> RegisterAccountSMSFlowResult:
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

        source_number = await command.phone_code_provider.provide_number()
        if isinstance(source_number, str):
            phone_number = source_number
        else:
            phone_number = source_number.number

        self.logger.info("Checking availability of the number...")

        # Skip this request to avoid TooManyRequestError
        # try:
        #     number_check = await self.bus.execute(
        #         AccountCheckPhoneNumber(phone_number=phone_number)
        #     )
        #     if number_check.get("status") != "ok":
        #         raise RegistrationError(
        #             msg=f"Probably phone number is not valid, response={number_check}"
        #         )
        # except BadRequestError as e:
        #     if e.response.json.get("error_type") == "missing_parameters":
        #         raise RegistrationError(
        #             msg=f"Phone number is not valid, response={e.response.json}"
        #         )
        #     raise e

        self.logger.info("Requesting SMS with code...")
        code_send = await self.bus.execute(
            AccountSendSignupSmsCode(phone_number=phone_number, waterfall_id=waterfall_id)
        )
        if code_send.get("status") != "ok":
            raise RegistrationError(msg=f"Instagram didn't send the code, response={code_send}")

        code = await command.phone_code_provider.provide_code()

        self.logger.info("Sending the code for verification...")
        code_validation = await self.bus.execute(
            AccountValidateSignupSmsCode(
                phone_number=phone_number, code=code, waterfall_id=waterfall_id
            )
        )
        if code_validation.get("status") != "ok":
            if code_validation.get("error_type") == "invalid_nonce":
                raise RegistrationError(msg=f"Invalid code, response={code_validation}")
            raise RegistrationError(
                msg=f"Unknown error while code submitting, response={code_validation}"
            )

        await self.bus.execute(
            AccountUsernameSuggestions(username=username, waterfall_id=waterfall_id)
        )

        self.logger.info("Sending a registration request...")
        creation_result = await self.bus.execute(
            AccountCreateValidated(
                username=username,
                password=password,
                first_name=first_name,
                code=code,
                phone_number=phone_number,
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
            return RegisterAccountSMSFlowResult(
                created_user=created_user,
                number=source_number,
            )

        raise RegistrationError(
            msg=f"Unknown response for creation request, response={creation_result}"
        )
