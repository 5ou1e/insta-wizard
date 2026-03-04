from dataclasses import dataclass
from typing import TypedDict, cast

from insta_wizard.common.generators import utc_offset_from_timezone
from insta_wizard.common.utils import dumps
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import Command, CommandHandler
from insta_wizard.mobile.common.mobile_requester import MobileRequester
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.exceptions import MediaNeedsReuploadError, TranscodeNotFinishedYetError
from insta_wizard.mobile.models.state import MobileClientState


class MediaUploadFinishResponse(TypedDict):
    pass


@dataclass(slots=True, kw_only=True)
class MediaUploadFinish(Command[MediaUploadFinishResponse]):
    upload_id: str
    source_type: str
    video: bool = False
    duration_ms: int | None = None  # required when video=True


class MediaUploadFinishHandler(CommandHandler[MediaUploadFinish, MediaUploadFinishResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: MediaUploadFinish) -> MediaUploadFinishResponse:
        data = {
            "upload_id": command.upload_id,
            "source_type": command.source_type,
            "_uid": self.state.local_data.user_id,
            "device_id": self.state.device.android_id,
            "_uuid": self.state.device.device_id,
            "timezone_offset": str(utc_offset_from_timezone(self.state.device.timezone)),
            "device": dumps(
                {
                    "android_version": self.state.device.os_api_level,
                    "android_release": self.state.device.os_version,
                    "manufacturer": self.state.device.manufacturer,
                    "model": self.state.device.model,
                }
            ),
            "length": command.duration_ms / 1000,
        }

        params = {"video": "1"} if command.video else None

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.MEDIA_UPLOAD_FINISH_URI,
            data=build_signed_body(data),
            params=params,
            extra_headers={
                "retry_context": dumps(
                    {
                        "num_step_auto_retry": 0,
                        "num_reupload": 0,
                        "num_step_manual_retry": 0,
                    }
                )
            },
        )
        if resp.get("message") == "media_needs_reupload":
            raise MediaNeedsReuploadError()
        if "Transcode not finished yet" in resp.get("message", ""):
            raise TranscodeNotFinishedYetError()

        return cast(MediaUploadFinishResponse, resp)
