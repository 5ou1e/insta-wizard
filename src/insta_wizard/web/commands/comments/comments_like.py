from dataclasses import dataclass
from typing import cast

from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import WebApiRequester
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.comments.comments_like import (
    CommentsLikeResponse,
)


@dataclass(slots=True)
class CommentsLike(Command[CommentsLikeResponse]):
    """Like a comment on a media post"""

    comment_id: str  # 17873106636540219


class CommentsLikeHandler(CommandHandler[CommentsLike, CommentsLikeResponse]):
    def __init__(
        self,
        api_requester: WebApiRequester,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: CommentsLike) -> CommentsLikeResponse:
        self.state.csrftoken_guard()
        return cast(
            CommentsLikeResponse,
            await self.api_requester.execute(
                method="POST",
                url=constants.COMMENTS_LIKE_URL.format(comment_id=command.comment_id),
            ),
        )
