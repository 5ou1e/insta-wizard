from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.threads_approve import (
    DirectV2ThreadsApproveResponse,
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
class DirectV2ThreadsApprove(Command[DirectV2ThreadsApproveResponse]):
    thread_id: str


class DirectV2ThreadsApproveHandler(
    CommandHandler[DirectV2ThreadsApprove, DirectV2ThreadsApproveResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2ThreadsApprove) -> DirectV2ThreadsApproveResponse:
        payload = {
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_GET_THREADS_APPROVE_URI.format(thread_id=command.thread_id),
            data=payload,
        )
        return cast(DirectV2ThreadsApproveResponse, resp)
