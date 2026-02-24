from dataclasses import dataclass
from typing import cast

from insta_wizard.web.commands._responses.likes.likes_unlike import (
    LikesUnlikeResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import WebApiRequester
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class LikesUnlike(Command[LikesUnlikeResult]):
    """Unlike a media post"""

    media_id: str  # 17873106636540219


class LikesUnlikeHandler(CommandHandler[LikesUnlike, LikesUnlikeResult]):
    def __init__(
        self,
        api_requester: WebApiRequester,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: LikesUnlike) -> LikesUnlikeResult:
        self.state.csrftoken_guard()
        return cast(
            LikesUnlikeResult,
            await self.api_requester.execute(
                method="POST",
                url=constants.LIKES_UNLIKE_URL.format(media_id=command.media_id),
            ),
        )
