from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import dumps
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
from insta_wizard.mobile.responses.direct.threads_approve_multiple import (
    DirectV2ThreadsApproveMultipleResponse,
)


@dataclass(slots=True)
class DirectV2ThreadsApproveMultiple(Command[DirectV2ThreadsApproveMultipleResponse]):
    thread_ids: list[str]


class DirectV2ThreadsApproveMultipleHandler(
    CommandHandler[DirectV2ThreadsApproveMultiple, DirectV2ThreadsApproveMultipleResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2ThreadsApproveMultiple
    ) -> DirectV2ThreadsApproveMultipleResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "thread_ids": dumps(command.thread_ids),
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_GET_THREADS_APPROVE_MULTIPLE_URI,
            data=payload,
        )
        return cast(DirectV2ThreadsApproveMultipleResponse, resp)
