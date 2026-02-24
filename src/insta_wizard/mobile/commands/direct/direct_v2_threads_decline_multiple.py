from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import dumps
from insta_wizard.mobile.commands._responses.direct.direct_v2_threads_decline_multiple import (
    DirectV2ThreadsDeclineMultipleResponse,
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
class DirectV2ThreadsDeclineMultiple(Command[DirectV2ThreadsDeclineMultipleResponse]):
    thread_ids: list[str]


class DirectV2ThreadsDeclineMultipleHandler(
    CommandHandler[DirectV2ThreadsDeclineMultiple, DirectV2ThreadsDeclineMultipleResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2ThreadsDeclineMultiple
    ) -> DirectV2ThreadsDeclineMultipleResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "thread_ids": dumps(command.thread_ids),
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_GET_THREADS_DECLINE_MULTIPLE_URI,
            data=payload,
        )
        return cast(DirectV2ThreadsDeclineMultipleResponse, resp)
