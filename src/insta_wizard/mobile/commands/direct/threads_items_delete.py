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
from insta_wizard.mobile.responses.direct.threads_items_delete import (
    DirectV2ThreadsItemsDeleteResponse,
)


@dataclass(slots=True)
class DirectV2ThreadsItemsDelete(Command[DirectV2ThreadsItemsDeleteResponse]):
    thread_id: str
    item_id: str
    send_attribution: str = "inbox"
    original_message_client_context: str | None = None  # 6996896716330331747


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
            "is_shh_mode": "0",
            "send_attribution": command.send_attribution,
            "_uuid": self.state.device.device_id,
            **(
                {"original_message_client_context": "6996896716330331747"}
                if command.original_message_client_context
                else {}
            ),
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_ITEMS_DELETE_URI.format(
                thread_id=command.thread_id, item_id=command.item_id
            ),
            data=payload,
        )
        return cast(DirectV2ThreadsItemsDeleteResponse, resp)
