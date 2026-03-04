from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.responses.account.account_validate_signup_sms_code import (
    AccountValidateSignupSmsCodeResponse,
)


@dataclass(slots=True)
class AccountValidateSignupSmsCode(Command[AccountValidateSignupSmsCodeResponse]):
    """Submit SMS verification code during account registration"""

    phone_number: str
    code: int | str
    waterfall_id: str


class AccountValidateSignupSmsCodeHandler(
    CommandHandler[AccountValidateSignupSmsCode, AccountValidateSignupSmsCodeResponse]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
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
            "waterfall_id": command.waterfall_id,
        }
        payload = build_signed_body(data)

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.ACCOUNTS_VALIDATE_SIGNUP_SMS_CODE_URI,
            data=payload,
        )
        return cast(AccountValidateSignupSmsCodeResponse, resp)
