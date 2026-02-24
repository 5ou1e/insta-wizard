from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.account.account_security_info import (
    AccountSecurityInfoResponse,
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
class AccountSecurityInfo(Command[AccountSecurityInfoResponse]):
    pass


class AccountSecurityInfoHandler(CommandHandler[AccountSecurityInfo, AccountSecurityInfoResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: AccountSecurityInfo) -> AccountSecurityInfoResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
        }
        data = build_signed_body(payload)
        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_SECURITY_INFO_URI,
            data=data,
        )

        return cast(AccountSecurityInfoResponse, resp)
