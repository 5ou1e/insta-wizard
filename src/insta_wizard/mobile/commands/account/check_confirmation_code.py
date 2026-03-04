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


class AccountCheckConfirmationCodeResponse(TypedDict):
    pass


@dataclass(slots=True)
class AccountCheckConfirmationCode(Command[AccountCheckConfirmationCodeResponse]):
    """Submit Email verification code during account registration"""

    email: str
    code: int | str
    waterfall_id: str


class AccountCheckConfirmationCodeHandler(
    CommandHandler[AccountCheckConfirmationCode, AccountCheckConfirmationCodeResponse]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(
        self,
        command: AccountCheckConfirmationCode,
    ) -> AccountCheckConfirmationCodeResponse:
        data = {
            "code": command.code,
            "device_id": self.state.device.android_id,
            "email": command.email,
            "waterfall_id": command.waterfall_id,
        }
        payload = build_signed_body(data)

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.ACCOUNTS_CHECK_CONFIRMATION_CODE_URI,
            data=payload,
        )
        return cast(AccountCheckConfirmationCodeResponse, resp)
