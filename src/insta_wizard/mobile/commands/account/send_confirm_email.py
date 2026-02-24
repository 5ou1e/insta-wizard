from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.account.account_send_confirm_email import (
    AccountSendConfirmEmailResponse,
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
class AccountSendConfirmEmail(Command[AccountSendConfirmEmailResponse]):
    """Установить эл.адрес аккаунту и отправить ссылку подтверждения"""

    email: str


class AccountSendConfirmEmailHandler(
    CommandHandler[AccountSendConfirmEmail, AccountSendConfirmEmailResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: AccountSendConfirmEmail) -> AccountSendConfirmEmailResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "phone_id": self.state.device.phone_id,
            "_uid": self.state.local_data.user_id or "",
            "guid": self.state.device.device_id,
            "send_source": "personal_information",
            "email": command.email,
        }
        data = build_signed_body(payload)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_SEND_CONFIRM_EMAIL_URI,
            data=data,
        )
        return cast(AccountSendConfirmEmailResponse, resp)
