from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.media.media_comments import MediaCommentsResponse
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class MediaComments(Command[MediaCommentsResponse]):
    """Get comments for a media post"""

    media_id: str
    min_id: str = None
    max_id: str = None


class MediaCommentsHandler(CommandHandler[MediaComments, MediaCommentsResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: MediaComments) -> MediaCommentsResponse:
        params = {
            "can_support_threading": "true",
            "permalink_enabled": "false",
        }
        if command.min_id:
            params["min_id"] = command.min_id
        if command.max_id:
            params["max_id"] = command.max_id

        resp = await self.api.call_api(
            method="GET",
            uri=constants.MEDIA_COMMENTS_URI.format(media_id=command.media_id),
            params=params,
        )

        return cast(MediaCommentsResponse, resp)
