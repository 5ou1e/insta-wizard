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
from insta_wizard.mobile.responses.direct.threads_leave import DirectV2ThreadsLeaveResponse


@dataclass(slots=True)
class DirectV2ThreadsLeave(Command[DirectV2ThreadsLeaveResponse]):
    thread_id: str


class DirectV2ThreadsLeaveHandler(
    CommandHandler[DirectV2ThreadsLeave, DirectV2ThreadsLeaveResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2ThreadsLeave) -> DirectV2ThreadsLeaveResponse:
        payload = {
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_LEAVE_URI.format(thread_id=command.thread_id),
            data=payload,
        )
        return cast(DirectV2ThreadsLeaveResponse, resp)
