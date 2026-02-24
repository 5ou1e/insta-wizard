from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.threads_items_seen import (
    DirectV2ThreadsItemsSeenResponse,
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
class DirectV2ThreadsItemsSeen(Command[DirectV2ThreadsItemsSeenResponse]):
    thread_id: str
    item_id: str


class DirectV2ThreadsItemsSeenHandler(
    CommandHandler[DirectV2ThreadsItemsSeen, DirectV2ThreadsItemsSeenResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2ThreadsItemsSeen) -> DirectV2ThreadsItemsSeenResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "use_unified_inbox": "true",
            "action": "mark_seen",
            "thread_id": command.thread_id,
            "item_id": command.item_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_ITEMS_SEEN_URI.format(
                thread_id=command.thread_id, item_id=command.item_id
            ),
            data=payload,
        )
        return cast(DirectV2ThreadsItemsSeenResponse, resp)
