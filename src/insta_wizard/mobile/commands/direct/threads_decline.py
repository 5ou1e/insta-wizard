from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.responses.direct.threads_decline import (
    DirectV2ThreadsDeclineResponse,
)


@dataclass(slots=True)
class DirectV2ThreadsDecline(Command[DirectV2ThreadsDeclineResponse]):
    thread_id: str


class DirectV2ThreadsDeclineHandler(
    CommandHandler[DirectV2ThreadsDecline, DirectV2ThreadsDeclineResponse]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: DirectV2ThreadsDecline) -> DirectV2ThreadsDeclineResponse:
        payload = {
            "_uuid": self.state.device.device_id,
        }

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.DIRECT_V2_GET_THREADS_DECLINE_URI.format(thread_id=command.thread_id),
            data=payload,
        )
        return cast(DirectV2ThreadsDeclineResponse, resp)
