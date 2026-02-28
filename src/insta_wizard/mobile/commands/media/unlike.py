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
from insta_wizard.mobile.responses.media.unlike import MediaUnlikeResponse


@dataclass(slots=True)
class MediaUnlike(Command[MediaUnlikeResponse]):
    """Unike the media"""

    media_id: str


class MediaUnlikeHandler(CommandHandler[MediaUnlike, MediaUnlikeResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: MediaUnlike) -> MediaUnlikeResponse:
        payload = {
            # "module_name": ...,
            "media_id": command.media_id,
            "_uuid": self.state.device.device_id,
            "radio_type": self.state.radio_type,
            "inventory_source": "media_or_ad",
            "container_module": "feed_timeline",
        }

        data = build_signed_body(payload)
        resp = await self.api.call_api(
            method="POST",
            uri=constants.MEDIA_UNLIKE_URI.format(media_id=command.media_id),
            data=data,
        )
        return cast(MediaUnlikeResponse, resp)
