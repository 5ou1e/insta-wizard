from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.direct_v2_threads_decline_all import (
    DirectV2ThreadsDeclineAllResponse,
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
class DirectV2ThreadsDeclineAll(Command[DirectV2ThreadsDeclineAllResponse]):
    thread_ids: list[str]


class DirectV2ThreadsDeclineAllHandler(
    CommandHandler[DirectV2ThreadsDeclineAll, DirectV2ThreadsDeclineAllResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2ThreadsDeclineAll
    ) -> DirectV2ThreadsDeclineAllResponse:
        payload = {
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_GET_THREADS_DECLINE_ALL_URI,
            data=payload,
        )
        return cast(DirectV2ThreadsDeclineAllResponse, resp)
