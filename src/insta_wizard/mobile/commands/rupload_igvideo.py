import random
import time
from dataclasses import dataclass
from uuid import uuid4

from insta_wizard.common.transport.models import HttpRequest
from insta_wizard.common.utils import dumps
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class RuploadIgvideo(Command[str]):
    video_bytes: bytes
    duration_ms: int
    width: int
    height: int
    upload_id: str = ""
    to_album: bool = False
    for_story: bool = False
    for_clips: bool = False


class RuploadIgvideoHandler(CommandHandler[RuploadIgvideo, str]):
    def __init__(
        self,
        requester: MobileRequester,
        state: MobileClientState,
    ) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: RuploadIgvideo) -> str:
        upload_id = command.upload_id or str(int(time.time() * 1000))
        video_waterfall_id = str(uuid4())

        upload_name = f"{upload_id}_0_{random.randint(1000000000, 9999999999)}"

        rupload_params: dict = {
            "retry_context": dumps(
                {
                    "num_step_auto_retry": 0,
                    "num_reupload": 0,
                    "num_step_manual_retry": 0,
                }
            ),
            "media_type": "2",
            "xsharing_user_ids": "[]",
            "upload_id": upload_id,
            "upload_media_duration_ms": str(command.duration_ms),
            "upload_media_width": str(command.width),
            "upload_media_height": str(command.height),
        }
        if command.to_album:
            rupload_params["is_sidecar"] = "1"
        if command.for_story:
            rupload_params["extract_cover_frame"] = "1"
            rupload_params["content_tags"] = "has-overlay"
            rupload_params["for_album"] = "1"
        if command.for_clips:
            rupload_params["is_clips_video"] = "1"

        video_len = str(len(command.video_bytes))

        url = constants.RUPLOAD_IGVIDEO_URL.format(name=upload_name)

        base_headers = {
            "Accept-Encoding": "gzip",
            "X-Instagram-Rupload-Params": dumps(rupload_params),
            "x_fb_video_waterfall_id": video_waterfall_id,
            "X-Entity-Type": "video/mp4",
            "X-Fb-Friendly-Name": "undefined:media-upload",
            "X-Ig-Connection-Type": self.state.device.connection_type,
            "X-Ig-Capabilities": self.state.version_info.capabilities,
            "X-Ig-App-Id": self.state.version_info.app_id,
        }

        # Step 1: GET — register upload with Instagram, receive starting offset
        get_headers = self.requester.api_headers()
        get_headers.update(base_headers)

        init_resp = await self.requester.call(
            HttpRequest(method="GET", url=url, headers=get_headers)
        )
        offset = str(init_resp.get("offset", 0))

        # Step 2: POST — send video bytes
        post_headers = self.requester.api_headers()
        post_headers.update(base_headers)
        post_headers.update(
            {
                "Content-Type": "application/octet-stream",
                "Content-Length": video_len,
                "Offset": offset,
                "X-Entity-Length": video_len,
                "X-Entity-Name": upload_name,
                "Priority": "u=6, i",
            }
        )

        await self.requester.call(
            HttpRequest(
                method="POST",
                url=url,
                headers=post_headers,
                data=command.video_bytes,
            )
        )

        return upload_id
