import time
from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import Command, CommandHandler
from insta_wizard.mobile.common.mobile_requester import MobileRequester
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.models.state import MobileClientState
from insta_wizard.mobile.responses.media.configure_sidecar import (
    MediaConfigureSidecarResponse,
)


@dataclass(slots=True)
class SidecarChild:
    upload_id: str
    width: int
    height: int
    duration_ms: int | None = None  # None = photo item, int = video item


@dataclass(slots=True, kw_only=True)
class MediaConfigureSidecar(Command[MediaConfigureSidecarResponse]):
    """Publish a carousel (album) of uploaded media items."""

    children: list[SidecarChild]
    caption: str = ""


class MediaConfigureSidecarHandler(
    CommandHandler[MediaConfigureSidecar, MediaConfigureSidecarResponse]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: MediaConfigureSidecar) -> MediaConfigureSidecarResponse:
        children_metadata = []
        for child in command.children:
            if child.duration_ms is not None:
                duration_s = child.duration_ms / 1000
                children_metadata.append(
                    {
                        "upload_id": child.upload_id,
                        "source_type": "4",
                        "length": duration_s,
                        "clips": [{"length": duration_s, "source_type": "4"}],
                        "poster_frame_index": 0,
                        "audio_muted": False,
                        "filter_type": "0",
                    }
                )
            else:
                children_metadata.append(
                    {
                        "upload_id": child.upload_id,
                        "source_type": "4",
                        "edits": {
                            "crop_original_size": [child.width, child.height],
                            "crop_center": [0.0, -0.0],
                            "crop_zoom": 1.0,
                        },
                    }
                )

        data: dict = {
            "client_sidecar_id": str(int(time.time() * 1000)),
            "caption": command.caption,
            "upload_id": command.children[0].upload_id,
            "children_metadata": children_metadata,
            "_uid": self.state.local_data.user_id,
            "device_id": self.state.device.android_id,
            "_uuid": self.state.device.device_id,
        }

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.MEDIA_CONFIGURE_SIDECAR_URI,
            data=build_signed_body(data),
        )
        return cast(MediaConfigureSidecarResponse, resp)
