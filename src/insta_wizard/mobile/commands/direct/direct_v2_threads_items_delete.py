from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.direct_v2_threads_items_delete import (
    DirectV2ThreadsItemsDeleteResponse,
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
class DirectV2ThreadsItemsDelete(Command[DirectV2ThreadsItemsDeleteResponse]):
    thread_id: str
    item_id: str


class DirectV2ThreadsItemsDeleteHandler(
    CommandHandler[DirectV2ThreadsItemsDelete, DirectV2ThreadsItemsDeleteResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2ThreadsItemsDelete
    ) -> DirectV2ThreadsItemsDeleteResponse:
        payload = {
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_ITEMS_DELETE_URI.format(
                thread_id=command.thread_id, item_id=command.item_id
            ),
            data=payload,
        )
        return cast(DirectV2ThreadsItemsDeleteResponse, resp)
