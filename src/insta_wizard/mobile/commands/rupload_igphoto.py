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
class RuploadIgphoto(Command[str]):
    image_bytes: bytes
    upload_id: str = ""
    to_album: bool = False


class RuploadIgphotoHandler(CommandHandler[RuploadIgphoto, str]):
    def __init__(
        self,
        requester: MobileRequester,
        state: MobileClientState,
    ) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: RuploadIgphoto) -> str:
        upload_id = command.upload_id or str(int(time.time() * 1000))
        photo_waterfall_id = str(uuid4())

        upload_name = f"{upload_id}_0_{random.randint(1000000000, 9999999999)}"

        rupload_params: dict = {
            "retry_context": dumps(
                {
                    "num_step_auto_retry": 0,
                    "num_reupload": 0,
                    "num_step_manual_retry": 0,
                }
            ),
            "media_type": "1",
            "xsharing_user_ids": "[]",
            "upload_id": upload_id,
            "image_compression": dumps(
                {"lib_name": "moz", "lib_version": "3.1.m", "quality": "80"}
            ),
        }
        if command.to_album:
            rupload_params["is_sidecar"] = "1"

        photo_len = str(len(command.image_bytes))

        url = constants.RUPLOAD_IGPHOTO_URL.format(name=upload_name)

        headers = self.requester.api_headers()
        headers.update(
            {
                "Content-Type": "application/octet-stream",
                "Content-Length": photo_len,
                "Accept-Encoding": "gzip",
                "X-Instagram-Rupload-Params": dumps(rupload_params),
                "x_fb_photo_waterfall_id": photo_waterfall_id,
                "Offset": "0",
                "X-Entity-Length": photo_len,
                "X-Entity-Name": upload_name,
                "X-Entity-Type": "image/jpeg",
                "Priority": "u=6, i",
                "X-Fb-Friendly-Name": "undefined:media-upload",
            }
        )

        await self.requester.call(
            HttpRequest(
                method="POST",
                url=url,
                headers=headers,
                data=command.image_bytes,
            )
        )

        return upload_id
