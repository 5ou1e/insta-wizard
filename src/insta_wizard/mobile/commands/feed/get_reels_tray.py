from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import (
    generate_uuid_v4_string,
    utc_offset_from_timezone,
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
from insta_wizard.mobile.responses.feed.reels_tray import (
    FeedGetReelsTrayResponse,
)


@dataclass(slots=True)
class FeedGetReelsTray(Command[FeedGetReelsTrayResponse]):
    reason: str = "cold_start"
    page_size: str = "50"


class FeedGetReelsTrayHandler(CommandHandler[FeedGetReelsTray, FeedGetReelsTrayResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: FeedGetReelsTray) -> FeedGetReelsTrayResponse:
        payload = {
            "reason": command.reason,
            "timezone_offset": str(utc_offset_from_timezone(self.state.device.timezone)),
            "tray_session_id": generate_uuid_v4_string(),
            "request_id": generate_uuid_v4_string(),
            "_uuid": self.state.device.device_id,
            "page_size": command.page_size,
        }

        res = await self.api.call_api(
            method="POST",
            uri=constants.FEED_REELS_TRAY_URI,
            data=payload,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
            extra_headers={
                "x-ig-salt-ids": "220140399,332020310,974466465,974460658",
                "Priority": "u=0",
            },
        )
        return cast(FeedGetReelsTrayResponse, res)
