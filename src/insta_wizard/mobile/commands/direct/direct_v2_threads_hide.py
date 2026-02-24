from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.direct_v2_threads_hide import (
    DirectV2ThreadsHideResponse,
)
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


@dataclass(slots=True)
class DirectV2ThreadsHide(Command[DirectV2ThreadsHideResponse]):
    thread_id: str


class DirectV2ThreadsHideHandler(CommandHandler[DirectV2ThreadsHide, DirectV2ThreadsHideResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2ThreadsHide) -> DirectV2ThreadsHideResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "use_unified_inbox": "true",
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_HIDE_URI.format(thread_id=command.thread_id),
            data=payload,
        )
        return cast(DirectV2ThreadsHideResponse, resp)
