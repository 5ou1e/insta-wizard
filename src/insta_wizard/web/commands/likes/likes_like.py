from dataclasses import dataclass
from typing import cast

from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import WebApiRequester
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.likes.likes_like import (
    LikesLikeResponse,
)


@dataclass(slots=True)
class LikesLike(Command[LikesLikeResponse]):
    """Like a media post"""

    media_id: str  # 17873106636540219


class LikesLikeHandler(CommandHandler[LikesLike, LikesLikeResponse]):
    def __init__(
        self,
        api_requester: WebApiRequester,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: LikesLike) -> LikesLikeResponse:
        self.state.csrftoken_guard()
        return cast(
            LikesLikeResponse,
            await self.api_requester.execute(
                method="POST",
                url=constants.LIKES_LIKE_URL.format(media_id=command.media_id),
            ),
        )
