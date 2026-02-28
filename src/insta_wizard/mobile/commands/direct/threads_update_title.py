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
from insta_wizard.mobile.responses.direct.threads_update_title import (
    DirectV2ThreadsUpdateTitleResponse,
)


@dataclass(slots=True)
class DirectV2ThreadsUpdateTitle(Command[DirectV2ThreadsUpdateTitleResponse]):
    thread_id: str
    title: str


class DirectV2ThreadsUpdateTitleHandler(
    CommandHandler[DirectV2ThreadsUpdateTitle, DirectV2ThreadsUpdateTitleResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2ThreadsUpdateTitle
    ) -> DirectV2ThreadsUpdateTitleResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "title": command.title,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_UPDATE_TITLE_URI.format(thread_id=command.thread_id),
            data=payload,
        )
        return cast(DirectV2ThreadsUpdateTitleResponse, resp)
