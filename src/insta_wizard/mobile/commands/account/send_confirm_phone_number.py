from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.account.account_send_confirm_phone_number import (
    AccountSendConfirmPhoneNumberResponse,
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
class AccountSendConfirmPhoneNumber(Command[AccountSendConfirmPhoneNumberResponse]):
    """Установить аккаунту номер телефона и отправить код подтверждения"""

    phone_number: str


class AccountSendConfirmPhoneNumberHandler(
    CommandHandler[AccountSendConfirmPhoneNumber, AccountSendConfirmPhoneNumberResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: AccountSendConfirmPhoneNumber
    ) -> AccountSendConfirmPhoneNumberResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "phone_id": self.state.device.phone_id,
            "_uid": self.state.local_data.user_id or "",
            "guid": self.state.device.device_id,
            "android_build_type": "release",
            "send_source": "edit_profile",
            "phone_number": command.phone_number,
        }
        data = build_signed_body(payload)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_SEND_CONFIRM_PHONE_NUMBER_URI,
            data=data,
        )
        return cast(AccountSendConfirmPhoneNumberResponse, resp)
