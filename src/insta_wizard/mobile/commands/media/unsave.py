from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.responses.media.unsave import MediaUnsaveResponse


@dataclass(slots=True)
class MediaUnsave(Command[MediaUnsaveResponse]):
    """Unsave the media"""

    media_id: str


class MediaUnsaveHandler(CommandHandler[MediaUnsave, MediaUnsaveResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: MediaUnsave) -> MediaUnsaveResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "radio_type": self.state.radio_type,
            **({"_uid": self.state.local_data.user_id} if self.state.local_data.user_id else {}),
        }

        data = build_signed_body(payload)
        resp = await self.api.call_api(
            method="POST",
            uri=constants.MEDIA_UNSAVE_URI.format(media_id=command.media_id),
            data=data,
        )
        return cast(MediaUnsaveResponse, resp)
