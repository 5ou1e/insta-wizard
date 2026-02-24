from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.account.account_validate_signup_sms_code import (
    AccountValidateSignupSmsCodeResponse,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class AccountValidateSignupSmsCode(Command[AccountValidateSignupSmsCodeResponse]):
    """Отправить код полученный в смс при регистрации аккаунта"""

    phone_number: str
    code: int | str


class AccountValidateSignupSmsCodeHandler(
    CommandHandler[AccountValidateSignupSmsCode, AccountValidateSignupSmsCodeResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: AccountValidateSignupSmsCode,
    ) -> AccountValidateSignupSmsCodeResponse:
        data = {
            "verification_code": str(command.code),
            "phone_number": str(command.phone_number),
            "guid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "waterfall_id": self.state.local_data.waterfall_id,
        }
        payload = build_signed_body(data)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_VALIDATE_SIGNUP_SMS_CODE_URI,
            data=payload,
        )
        return cast(AccountValidateSignupSmsCodeResponse, resp)
