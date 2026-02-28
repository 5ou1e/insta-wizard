from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.responses.zr_dual_tokens import ZrDualTokensResponse


@dataclass(slots=True)
class ZrDualTokens(Command[ZrDualTokensResponse]):
    fetch_reason: str = "token_expired"


class ZrDualTokensHandler(CommandHandler[ZrDualTokens, ZrDualTokensResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: ZrDualTokens) -> ZrDualTokensResponse:
        data = {
            "normal_token_hash": "",
            "device_id": self.state.device.android_id,
            "_uuid": self.state.device.device_id,
            "custom_device_id": self.state.device.device_id,
            "fetch_reason": command.fetch_reason,
        }

        resp = await self.api.call_b_api(
            method="POST",
            uri=constants.ZR_DUAL_TOKENS_URI,
            data=data,
        )
        return cast(ZrDualTokensResponse, resp)
