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
from insta_wizard.mobile.responses.direct.threads_delete_items_locally import (
    DirectV2ThreadsDeleteItemsLocallyResponse,
)


@dataclass(slots=True)
class DirectV2ThreadsDeleteItemsLocally(Command[DirectV2ThreadsDeleteItemsLocallyResponse]):
    thread_id: str
    item_ids: list[str]
    original_message_client_context: str | None = None  # 6996896716330331747


class DirectV2ThreadsDeleteItemsLocallyHandler(
    CommandHandler[DirectV2ThreadsDeleteItemsLocally, DirectV2ThreadsDeleteItemsLocallyResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2ThreadsDeleteItemsLocally
    ) -> DirectV2ThreadsDeleteItemsLocallyResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            **(
                {"original_message_client_context": "6996896716330331747"}
                if command.original_message_client_context
                else {}
            ),
            "item_ids": dumps(command.item_ids),
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_DELETE_ITEMS_LOCALLY_URI.format(
                thread_id=command.thread_id
            ),
            data=payload,
        )
        return cast(DirectV2ThreadsDeleteItemsLocallyResponse, resp)
