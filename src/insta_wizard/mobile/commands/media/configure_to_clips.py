from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import utc_offset_from_timezone
from insta_wizard.common.utils import dumps
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import Command, CommandHandler
from insta_wizard.mobile.common.mobile_requester import MobileRequester
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.exceptions import MediaNeedsReuploadError
from insta_wizard.mobile.models.state import MobileClientState
from insta_wizard.mobile.responses.media.configure_clips import MediaConfigureToClipsResponse


@dataclass(slots=True, kw_only=True)
class MediaConfigureToClips(Command[MediaConfigureToClipsResponse]):
    """Publish uploaded video as a Reel (Clip)."""

    upload_id: str
    width: int
    height: int
    duration_ms: int
    caption: str = ""
    share_to_feed: bool = True
    audio_muted: bool = False


class MediaConfigureToClipsHandler(
    CommandHandler[MediaConfigureToClips, MediaConfigureToClipsResponse]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: MediaConfigureToClips) -> MediaConfigureToClipsResponse:
        duration_s = command.duration_ms / 1000
        data: dict = {
            "upload_id": command.upload_id,
            "caption": command.caption,
            "source_type": "4",
            "filter_type": "0",
            "timezone_offset": str(utc_offset_from_timezone(self.state.device.timezone)),
            "media_folder": "ScreenRecorder",
            "clips_share_preview_to_feed": "1" if command.share_to_feed else "0",
            "_uid": self.state.local_data.user_id,
            "device_id": self.state.device.android_id,
            "_uuid": self.state.device.device_id,
            "device": dumps(
                {
                    "android_version": self.state.device.os_api_level,
                    "android_release": self.state.device.os_version,
                    "manufacturer": self.state.device.manufacturer,
                    "model": self.state.device.model,
                }
            ),
            "length": duration_s,
            "clips": [{"length": duration_s, "source_type": "4"}],
            "extra": {"source_width": command.width, "source_height": command.height},
            "audio_muted": command.audio_muted,
            "poster_frame_index": 70,
        }

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.MEDIA_CONFIGURE_TO_CLIPS_URI,
            data=build_signed_body(data),
            params={"video": "1"},
        )
        if resp.get("message") == "media_needs_reupload":
            raise MediaNeedsReuploadError()

        return cast(MediaConfigureToClipsResponse, resp)
