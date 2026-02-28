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
from insta_wizard.mobile.responses.direct.threads_broadcast_text import (
    DirectV2ThreadsBroadcastTextResponse,
)


@dataclass(kw_only=True, slots=True)
class DirectV2ThreadsBroadcastText(Command[DirectV2ThreadsBroadcastTextResponse]):
    """Send a text message to users"""

    recipient_users: list[str]  # list of user-ids
    text: str  # text of message to send for users
    action: str = "send_item"
    send_attribution: str = "message_button"
    client_context: str = None  # 7431661993834281722


class DirectV2ThreadsBroadcastTextHandler(
    CommandHandler[DirectV2ThreadsBroadcastText, DirectV2ThreadsBroadcastTextResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2ThreadsBroadcastText
    ) -> DirectV2ThreadsBroadcastTextResponse:
        payload = {
            "recipient_users": dumps(
                [
                    command.recipient_users,
                ]
            ),
            "is_written_with_ai": "0",
            "action": command.action,
            "is_x_transport_forward": "false",
            "is_shh_mode": "0",
            "send_silently": "false",
            "send_attribution": command.send_attribution,
            **({"client_context": command.client_context} if command.client_context else {}),
            "text": command.text,
            "device_id": self.state.device.android_id,
            **({"mutation_token": command.client_context} if command.client_context else {}),
            "_uuid": self.state.device.device_id,
            # 'nav_chain': 'ExploreFragment:explore_popular:32:main_search:1771846253.383::3802610947101736477:1771846253.383,ClipsViewerFragment:clips_viewer:33:explore_popular_default_unit:1771846261.908:::1771846261.908,AudioPageFragment:audio_page:34:button:1771846266.306:::1771846266.306,ClipsViewerFragment:clips_viewer:35:audio_page:1771846274.524:::1771846274.524,UserDetailFragment:profile:36:button:1771846276.541:::1771846276.541,ClipsProfileTabFragment:clips_profile:37:button:1771846278.13:::1771846286.139,DirectThreadFragment:direct_thread:39:message_button:1771846287.427:::1771846287.427,DirectThreadFragment:direct_thread:40:button:1771846287.760:::1771846287.760',
            # 'ai_assistant_extras': dumps(
            #     {
            #         'thread_session_id': '0f0e98a9-4660-4c4e-b936-c3d364d410b5',
            #         'location_extras': None,
            #         'prompt_type': 'THREADVIEW_USER_INPUT_PROMPT',
            #         'enable_web_scraping': True,
            #     }
            # ),
            **({"offline_threading_id": command.client_context} if command.client_context else {}),
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_BROADCAST_TEXT_URI,
            data=payload,
            client_endpoint="DirectThreadFragment:direct_thread",
        )
        return cast(DirectV2ThreadsBroadcastTextResponse, resp)
