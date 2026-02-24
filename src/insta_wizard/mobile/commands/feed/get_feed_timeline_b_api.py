import gzip
from dataclasses import dataclass
from typing import cast
from urllib.parse import urlencode

from insta_wizard.common.generators import (
    current_timestamp_ms,
    generate_uuid_v4_string,
    utc_offset_from_timezone,
)
from insta_wizard.mobile.commands._responses.feed.get_feed_timeline_b_api import (
    FeedGetFeedTimelineBApiResponse,
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
class FeedGetFeedTimelineBApi(Command[FeedGetFeedTimelineBApiResponse]):
    pass


class FeedGetFeedTimelineBApiHandler(
    CommandHandler[FeedGetFeedTimelineBApi, FeedGetFeedTimelineBApiResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: FeedGetFeedTimelineBApi) -> FeedGetFeedTimelineBApiResponse:
        data = {
            "has_camera_permission": "0",
            "feed_view_info": "[]",
            "phone_id": self.state.device.phone_id,
            "reason": "cold_start_fetch",
            "battery_level": self.state.device.battery_level,
            "timezone_offset": str(utc_offset_from_timezone(self.state.device.timezone)),
            "client_recorded_request_time_ms": current_timestamp_ms(),
            "device_id": self.state.device.device_id,
            "request_id": generate_uuid_v4_string(),
            "is_pull_to_refresh": "0",
            "_uuid": self.state.device.device_id,
            "push_disabled": "true",
            "is_charging": "1" if self.state.device.is_charging else "0",
            "is_dark_mode": "0",
            "will_sound_on": "0",
            "session_id": generate_uuid_v4_string(),
            "bloks_versioning_id": self.state.version_info.bloks_version_id,
        }

        payload = gzip.compress(urlencode(data).encode("utf-8"))

        res = await self.api.call_b_api(
            method="POST",
            uri=constants.FEED_TIMELINE_URI,
            data=payload,
            client_endpoint="feed_timeline",
            extra_headers={
                "Content-Encoding": "gzip",
                "X-Fb-Friendly-Name": f"IgApi: {constants.FEED_TIMELINE_URI}_tail",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "Priority": "u=0",
                "x-cm-bandwidth-kbps": "1876.105",
                "x-cm-latency": "3.666",
                "x-fb": "1",
                "x-ads-opt-out": "0",
            },
        )
        return cast(FeedGetFeedTimelineBApiResponse, res)
