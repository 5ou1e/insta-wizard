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
from insta_wizard.mobile.responses.direct.threads_broadcast_reaction import (
    DirectV2ThreadsBroadcastReactionResponse,
)


@dataclass(kw_only=True, slots=True)
class DirectV2ThreadsBroadcastReaction(Command[DirectV2ThreadsBroadcastReactionResponse]):
    thread_ids: list[str]
    item_id: str
    item_type: str = "reaction"
    reaction_type: str  # "like"
    action: str = "send_item"
    send_attribution: str = "inbox"
    client_context: str | None = None  # "7431661286508464288"
    emoji: str | None = None  # "❤"
    reaction_action_source: str  # "emoji_tray"
    original_message_client_context: str | None = None  # "7431427378949483296"
    node_type: str = "item"
    reaction_status: str = "created"


class DirectV2ThreadsBroadcastReactionHandler(
    CommandHandler[DirectV2ThreadsBroadcastReaction, DirectV2ThreadsBroadcastReactionResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2ThreadsBroadcastReaction
    ) -> DirectV2ThreadsBroadcastReactionResponse:
        payload = {
            "item_type": command.item_type,
            "reaction_type": command.reaction_type,
            "action": command.action,
            "is_shh_mode": "0",
            "thread_ids": dumps(command.thread_ids),
            "send_attribution": command.send_attribution,
            **({"client_context": command.client_context} if command.client_context else {}),
            "super_react_type": "none",
            "reaction_action_source": command.reaction_action_source,
            "device_id": self.state.device.android_id,
            **({"mutation_token": command.client_context} if command.client_context else {}),
            "_uuid": self.state.device.device_id,
            **({"emoji": command.emoji} if command.emoji else {}),
            # "nav_chain": "MainFeedFragment:feed_timeline:1:cold_start:1771845553.719:::1771845621.645,DirectInboxFragment:direct_inbox:4:on_launch_direct_inbox:1771845625.629:::1771846107.982,DirectThreadFragment:direct_thread:21:inbox:1771846111.521:::1771846111.521,DirectThreadFragment:direct_thread:22:button:1771846111.998:::1771846121.288",
            "node_type": command.node_type,
            **(
                {"original_message_client_context": command.original_message_client_context}
                if command.original_message_client_context
                else {}
            ),
            **({"offline_threading_id": command.client_context} if command.client_context else {}),
            "reaction_status": command.reaction_status,
            "item_id": command.item_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_BROADCAST_REACTION_URI,
            data=payload,
            client_endpoint="DirectThreadFragment:direct_thread",
        )
        return cast(DirectV2ThreadsBroadcastReactionResponse, resp)
