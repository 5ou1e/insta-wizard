from dataclasses import dataclass
from typing import TypedDict, cast

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


class AccountSendVerifyEmailResponse(TypedDict):
    pass


@dataclass(slots=True)
class AccountSendVerifyEmail(Command[AccountSendVerifyEmailResponse]):
    """Request code to Email for account registration"""

    email: str
    waterfall_id: str


class AccountSendVerifyEmailHandler(
    CommandHandler[AccountSendVerifyEmail, AccountSendVerifyEmailResponse]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: AccountSendVerifyEmail) -> AccountSendVerifyEmailResponse:
        data = {
            "phone_id": self.state.device.phone_id,
            "device_id": self.state.device.android_id,
            "email": command.email,
            "waterfall_id": command.waterfall_id,
            "auto_confirm_only": "false",
        }
        payload = build_signed_body(data)

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.ACCOUNTS_SEND_VERIFY_EMAIL_URI,
            data=payload,
        )
        return cast(AccountSendVerifyEmailResponse, resp)
