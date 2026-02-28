from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.media.comment_bulk_delete import MediaCommentBulkDeleteResponse
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
class MediaCommentBulkDelete(Command[MediaCommentBulkDeleteResponse]):
    """Delete comments on media"""

    media_id: str
    comment_ids: list[str]


class MediaCommentBulkDeleteHandler(
    CommandHandler[MediaCommentBulkDelete, MediaCommentBulkDeleteResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: MediaCommentBulkDelete) -> MediaCommentBulkDeleteResponse:

        payload = {
            "_uuid": self.state.device.device_id,
            "radio_type": self.state.radio_type,
            "comment_ids_to_delete": ",".join([str(pk) for pk in command.comment_ids]),
        }
        data = build_signed_body(payload)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.MEDIA_COMMENT_BULK_DELETE_URI.format(media_id=command.media_id),
            data=data,
        )

        return cast(MediaCommentBulkDeleteResponse, resp)
