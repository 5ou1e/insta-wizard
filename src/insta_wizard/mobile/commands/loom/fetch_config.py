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
from insta_wizard.mobile.responses.loom.loom_fetch_config import (
    LoomFetchConfigResponse,
)


@dataclass(slots=True)
class LoomFetchConfig(Command[LoomFetchConfigResponse]):
    pass


class LoomFetchConfigHandler(CommandHandler[LoomFetchConfig, LoomFetchConfigResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: LoomFetchConfig) -> LoomFetchConfigResponse:
        resp = await self.api.call_b_api(
            method="GET",
            uri=constants.LOOM_FETCH_CONFIG_URI,
        )
        return cast(LoomFetchConfigResponse, resp)
