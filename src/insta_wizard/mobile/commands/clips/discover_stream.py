from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import (
    generate_uuid_v4_string,
)
from insta_wizard.mobile.commands._responses.clips.discover_stream import (
    ClipsDiscoverStreamResponse,
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
class ClipsDiscoverStream(Command[ClipsDiscoverStreamResponse]):
    pass


class ClipsDiscoverStreamHandler(CommandHandler[ClipsDiscoverStream, ClipsDiscoverStreamResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: ClipsDiscoverStream) -> ClipsDiscoverStreamResponse:
        payload = {
            "seen_reels": "[]",
            "client_flashcache_size": "0",
            "enable_mixed_media_chaining": "true",
            "device_status": "{}",
            "should_refetch_chaining_media": "false",
            "_uuid": self.state.device.device_id,
            "prefetch_trigger_type": "cold_start",
            "viewer_session_id": generate_uuid_v4_string(),
            "server_driven_cache_config": '{"serve_from_server_cache":true,"cohort_to_ttl_map":"","serve_on_foreground_prefetch":"true","serve_on_background_prefetch":"true","meta":""}',
            "container_module": "clips_viewer_clips_tab",
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.CLIPS_DISCOVER_STREAM_URI,
            data=payload,
            client_endpoint="feed_timeline",
            extra_headers={
                "x-ig-prefetch-request": "foreground",
            },
        )
        return cast(ClipsDiscoverStreamResponse, resp)
