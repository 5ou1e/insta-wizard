from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import gen_user_breadcrumb, generate_uuid_v4_string
from insta_wizard.mobile.commands._responses.media.media_comment import MediaCommentResponse
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
class MediaComment(Command[MediaCommentResponse]):
    """Post a comment on a media"""

    media_id: str
    comment_text: str
    replied_to_comment_id: str | None = None


class MediaCommentHandler(CommandHandler[MediaComment, MediaCommentResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: MediaComment) -> MediaCommentResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "radio_type": self.state.radio_type,
            "delivery_class": "organic",
            "feed_position": "0",
            "container_module": "self_comments_v2_feed_contextual_self_profile",
            "user_breadcrumb": gen_user_breadcrumb(len(command.comment_text)),
            "idempotence_token": generate_uuid_v4_string(),
            "comment_text": command.comment_text,
        }
        if command.replied_to_comment_id:
            payload["replied_to_comment_id"] = command.replied_to_comment_id

        data = build_signed_body(payload)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.MEDIA_COMMENT_URI.format(media_id=command.media_id),
            data=data,
        )

        return cast(MediaCommentResponse, resp)
