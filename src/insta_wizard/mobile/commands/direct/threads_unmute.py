from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.threads_unmute import (
    DirectV2ThreadsUnmuteResponse,
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
class DirectV2ThreadsUnmute(Command[DirectV2ThreadsUnmuteResponse]):
    thread_id: str


class DirectV2ThreadsUnmuteHandler(
    CommandHandler[DirectV2ThreadsUnmute, DirectV2ThreadsUnmuteResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2ThreadsUnmute) -> DirectV2ThreadsUnmuteResponse:
        payload = {
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_UNMUTE_URI.format(thread_id=command.thread_id),
            data=payload,
        )
        return cast(DirectV2ThreadsUnmuteResponse, resp)
