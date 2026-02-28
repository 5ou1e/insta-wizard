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
from insta_wizard.mobile.responses.direct.threads_hide import DirectV2ThreadsHideResponse


@dataclass(slots=True)
class DirectV2ThreadsHide(Command[DirectV2ThreadsHideResponse]):
    thread_id: str
    should_move_future_requests_to_spam: bool = False


class DirectV2ThreadsHideHandler(CommandHandler[DirectV2ThreadsHide, DirectV2ThreadsHideResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2ThreadsHide) -> DirectV2ThreadsHideResponse:
        payload = {
            "should_move_future_requests_to_spam": "true"
            if command.should_move_future_requests_to_spam
            else "false",
            "use_unified_inbox": "true",
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_HIDE_URI.format(thread_id=command.thread_id),
            data=payload,
        )
        return cast(DirectV2ThreadsHideResponse, resp)
