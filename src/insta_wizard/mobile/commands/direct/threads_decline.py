from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.threads_decline import (
    DirectV2ThreadsDeclineResponse,
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
class DirectV2ThreadsDecline(Command[DirectV2ThreadsDeclineResponse]):
    thread_id: str


class DirectV2ThreadsDeclineHandler(
    CommandHandler[DirectV2ThreadsDecline, DirectV2ThreadsDeclineResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2ThreadsDecline) -> DirectV2ThreadsDeclineResponse:
        payload = {
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_GET_THREADS_DECLINE_URI.format(thread_id=command.thread_id),
            data=payload,
        )
        return cast(DirectV2ThreadsDeclineResponse, resp)
