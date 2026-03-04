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
from insta_wizard.mobile.responses.account.account_send_signup_sms_code import (
    AccountSendSignupSmsCodeResponse,
)


@dataclass(slots=True)
class AccountSendSignupSmsCode(Command[AccountSendSignupSmsCodeResponse]):
    """Request SMS code for account registration"""

    phone_number: str
    waterfall_id: str


class AccountSendSignupSmsCodeHandler(
    CommandHandler[AccountSendSignupSmsCode, AccountSendSignupSmsCodeResponse]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: AccountSendSignupSmsCode) -> AccountSendSignupSmsCodeResponse:
        data = {
            "phone_id": self.state.device.phone_id,
            "phone_number": str(command.phone_number),
            "guid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "android_build_type": "release",
            "waterfall_id": command.waterfall_id,
        }
        payload = build_signed_body(data)

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.ACCOUNTS_SEND_SIGNUP_SMS_CODE_URI,
            data=payload,
        )
        return cast(AccountSendSignupSmsCodeResponse, resp)
