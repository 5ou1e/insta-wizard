import gzip
from dataclasses import dataclass
from typing import cast
from urllib.parse import urlencode

from insta_wizard.common.generators import (
    current_timestamp_ms,
    generate_uuid_v4_string,
    utc_offset_from_timezone,
)
from insta_wizard.common.utils import dumps
from insta_wizard.mobile.commands._responses.feed.feed_timeline_i_api import (
    FeedTimelineIApiResponse,
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
class FeedTimelineIApi(Command[FeedTimelineIApiResponse]):
    pass


class FeedTimelineIApiHandler(CommandHandler[FeedTimelineIApi, FeedTimelineIApiResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: FeedTimelineIApi) -> FeedTimelineIApiResponse:
        current_timestamp = current_timestamp_ms()
        session_id = generate_uuid_v4_string()

        data = {
            "has_camera_permission": "0",
            "feed_view_info": dumps(
                [
                    {
                        "media_id": "3703054020150160348_61713625421",
                        "version": 24,
                        "media_pct": 0.8782353,
                        "time_info": {
                            "10": 686,
                            "25": 686,
                            "50": 686,
                            "75": 686,
                        },
                        "was_share_tapped": False,
                        "client_position": 0,
                        "author_id": "61713625421",
                        "product_type": "clips",
                        "media_type": "2",
                    }
                ]
            ),
            "organic_realtime_information": dumps(
                [
                    {
                        "item_id": "3703054020150160348",
                        "item_type": 1,
                        "session_id": session_id,
                        "container_module": "feed_timeline",
                        "multi_ads_type": 0,
                        "seen_states": [
                            {
                                "media_id": "3703054020150160348_61713625421",
                                "media_time_spent": [-1],
                                "impression_timestamp": current_timestamp - 150,
                                "media_percent_visible": -1.0,
                            }
                        ],
                    }
                ]
            ),
            "phone_id": self.state.device.phone_id,
            "max_id": "KCEAZaQ2_7UYYzN1VSJ2cfZjMxaOKDcMFwAA3Osh_wLkYzMWtLLA35hmRgIYEGNvbGRfc3RhcnRfZmV0Y2hCMiiJAgACvrFq8VNfMw12ROqWEWQzDmSjWu8-UTMQzEvvMUZhM5AbSmw86mEzEBXFvZ7oYDMWjig3DBcAAJe0SjmCdWIzGuzNJVquXzOeW8j91iKgMim-hjLI918zr3sGm7cSZDOxaYA_wZtOMzRDh2YItgMztQo0KWGLYzM1wzIk4PNjM7QzowoICVUzuMsi9Ck9UTPBdCFy68lgM8KWxBLmA2QzxAcy9iGKYDPNGT3_w9RjM1Mxyc-Ep2Iz29KlACoCZDPc6yH_AuRjM96vIHsZl1Qz3mc6XKUMYzNkRTzJ_RNiM2WkNv-1GGMz5CfKDPjyXzPwyL7dA-tjM3VVInZx9mMze9wzZxR2WjNW7viqig0A",
            "client_view_state_media_list": dumps(
                [
                    {"id": "3703054020150160348_61713625421", "type": 0},
                    {"id": "25341232451094", "type": 161},
                    {"id": "3703074285802378613_61713625421", "type": 49},
                    {"id": "3702830488578597989_195284417", "type": 0},
                ]
            ),
            "reason": "pagination",
            "battery_level": self.state.device.battery_level,
            "timezone_offset": str(utc_offset_from_timezone(self.state.device.timezone)),
            "client_recorded_request_time_ms": current_timestamp,
            "device_id": self.state.device.device_id,
            "request_id": generate_uuid_v4_string(),
            "is_pull_to_refresh": "0",
            "_uuid": self.state.device.device_id,
            "push_disabled": "true",
            "is_charging": "1" if self.state.device.is_charging else "0",
            "is_dark_mode": "0",
            "will_sound_on": "0",
            "session_id": session_id,
            "bloks_versioning_id": self.state.version_info.bloks_version_id,
        }

        encoded = urlencode(data).encode("utf-8")
        payload = gzip.compress(encoded)

        res = await self.api.call_api(
            method="POST",
            uri=constants.FEED_TIMELINE_URI,
            data=payload,
            client_endpoint="feed_timeline",
            extra_headers={
                "Content-Encoding": "gzip",
                "Priority": "u=0",
                "x-cm-bandwidth-kbps": "1876.105",
                "x-cm-latency": "3.666",
                "x-fb": "1",
                "x-ads-opt-out": "0",
            },
        )
        return cast(FeedTimelineIApiResponse, res)
