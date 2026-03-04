import time
from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import dumps
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import Command, CommandHandler
from insta_wizard.mobile.common.mobile_requester import MobileRequester
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.models.state import MobileClientState
from insta_wizard.mobile.responses.media.configure_to_story import (
    MediaConfigureToStoryResponse,
)


@dataclass(slots=True, kw_only=True)
class MediaConfigureToStory(Command[MediaConfigureToStoryResponse]):
    """Publish uploaded media to stories."""

    upload_id: str
    video: bool = False
    duration_ms: int | None = None  # required when video=True
    width: int | None = None
    height: int | None = None


class MediaConfigureToStoryHandler(
    CommandHandler[MediaConfigureToStory, MediaConfigureToStoryResponse]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: MediaConfigureToStory) -> MediaConfigureToStoryResponse:
        timestamp = int(time.time())
        data: dict = {
            "upload_id": command.upload_id,
            "source_type": "3",
            "configure_mode": "1",
            "_uid": self.state.local_data.user_id,
            "device_id": self.state.device.android_id,
            "_uuid": self.state.device.device_id,
            "client_timestamp": str(timestamp),
            "client_shared_at": str(timestamp - 5),
        }

        if command.video:
            duration = command.duration_ms / 1000 if command.duration_ms is not None else 0.0
            data["video_result"] = ""
            data["audio_muted"] = "0"
            data["length"] = str(duration)
            data["capture_type"] = "normal"
            data["original_media_type"] = "video"
            data["creation_surface"] = "camera"
            data["camera_position"] = "back"
            data["poster_frame_index"] = "0"
            data["clips"] = dumps(
                [{"length": duration, "source_type": "3", "camera_position": "back"}]
            )
            if command.width is not None and command.height is not None:
                data["media_transformation_info"] = dumps(
                    {
                        "width": str(command.width),
                        "height": str(command.height),
                        "x_transform": "0",
                        "y_transform": "0",
                        "zoom": "1.0",
                        "rotation": "0.0",
                        "background_coverage": "0.0",
                    }
                )

        params = {"video": "1"} if command.video else None

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.MEDIA_CONFIGURE_TO_STORY_URI,
            data=build_signed_body(data),
            params=params,
        )
        if resp.get("message") == "media_needs_reupload":
            raise MediaNeedsReuploadError()

        return cast(MediaConfigureToStoryResponse, resp)
