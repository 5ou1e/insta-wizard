from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import (
    generate_uuid_v4_string,
)
from insta_wizard.mobile.commands._responses.direct.inbox import (
    DirectV2InboxResponse,
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
class DirectV2Inbox(Command[DirectV2InboxResponse]):
    limit: int = 15
    thread_message_limit: int = 5
    visual_message_return_type: str = "unseen"
    fetch_reason: str = "initial_snapshot"


class DirectV2InboxHandler(CommandHandler[DirectV2Inbox, DirectV2InboxResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2Inbox) -> DirectV2InboxResponse:
        params = {
            "visual_message_return_type": command.visual_message_return_type,
            "igd_request_log_tracking_id": generate_uuid_v4_string(),
            "no_pending_badge": "true",
            "thread_message_limit": command.thread_message_limit,
            "persistentBadging": "true",
            "limit": command.limit,
            "is_prefetching": "false",
            "push_disabled": "true",
            "fetch_reason": command.fetch_reason,
        }

        resp = await self.api.call_api(
            method="GET",
            uri=constants.DIRECT_V2_INBOX_URI,
            params=params,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(DirectV2InboxResponse, resp)
