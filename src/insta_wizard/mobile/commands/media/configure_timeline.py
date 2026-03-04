from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import Command, CommandHandler
from insta_wizard.mobile.common.mobile_requester import MobileRequester
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.exceptions import MediaNeedsReuploadError
from insta_wizard.mobile.models.state import MobileClientState
from insta_wizard.mobile.responses.media.configure_timeline import (
    MediaConfigureResponse,
)


@dataclass(slots=True, kw_only=True)
class MediaConfigure(Command[MediaConfigureResponse]):
    """Publish uploaded media to the timeline feed."""

    upload_id: str
    width: int
    height: int
    caption: str = ""
    video: bool = False
    duration_ms: int | None = None  # required when video=True


class MediaConfigureHandler(CommandHandler[MediaConfigure, MediaConfigureResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: MediaConfigure) -> MediaConfigureResponse:
        base: dict = {
            "upload_id": command.upload_id,
            "caption": command.caption,
            "source_type": "4",
            "extra": {
                "source_width": command.width,
                "source_height": command.height,
            },
            "_uid": self.state.local_data.user_id,
            "device_id": self.state.device.android_id,
            "_uuid": self.state.device.device_id,
        }

        if command.video:
            duration_s = command.duration_ms / 1000 if command.duration_ms else 0
            data = {
                **base,
                "filter_type": "0",
                "poster_frame_index": 0,
                "audio_muted": False,
                "length": duration_s,
                "clips": [{"length": duration_s, "source_type": "4"}],
            }
        else:
            data = {
                **base,
                "edits": {
                    "crop_original_size": [command.width, command.height],
                    "crop_center": [0.0, -0.0],
                    "crop_zoom": 1.0,
                },
            }

        params = {"video": "1"} if command.video else None

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.MEDIA_CONFIGURE_URI,
            data=build_signed_body(data),
            params=params,
        )
        if resp.get("message") == "media_needs_reupload":
            raise MediaNeedsReuploadError()

        return cast(MediaConfigureResponse, resp)
