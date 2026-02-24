import random
from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.media.media_comment_unlike import (
    MediaCommentUnlikeResponse,
)
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


@dataclass(slots=True)
class MediaCommentUnlike(Command[MediaCommentUnlikeResponse]):
    """Unlike a comment"""

    comment_id: int


class MediaCommentUnlikeHandler(CommandHandler[MediaCommentUnlike, MediaCommentUnlikeResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: MediaCommentUnlike) -> MediaCommentUnlikeResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "radio_type": self.state.radio_type,
            "is_carousel_bumped_post": "false",
            "container_module": "feed_contextual_self_profile",
            "feed_position": str(random.randint(0, 6)),
        }
        data = build_signed_body(payload)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.MEDIA_COMMENT_UNLIKE_URI.format(comment_id=command.comment_id),
            data=data,
        )

        return cast(MediaCommentUnlikeResponse, resp)
