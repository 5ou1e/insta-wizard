from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.account.account_check_phone_number import (
    AccountCheckPhoneNumberResponse,
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
class AccountCheckPhoneNumber(Command[AccountCheckPhoneNumberResponse]):
    """Check if phone number is available"""

    phone_number: str


class AccountCheckPhoneNumberHandler(
    CommandHandler[AccountCheckPhoneNumber, AccountCheckPhoneNumberResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: AccountCheckPhoneNumber) -> AccountCheckPhoneNumberResponse:
        data = {
            "phone_id": self.state.device.phone_id,
            "login_nonce_map": "{}",
            "phone_number": str(command.phone_number),
            "guid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "prefill_shown": "False",
        }
        payload = build_signed_body(data)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_CHECK_PHONE_NUMBER_URI,
            data=payload,
        )
        return cast(AccountCheckPhoneNumberResponse, resp)
