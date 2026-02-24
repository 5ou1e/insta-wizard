from dataclasses import dataclass
from typing import cast

from insta_wizard.web.commands._responses.comments.comments_like import (
    CommentsLikeResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import WebApiRequester
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class CommentsLike(Command[CommentsLikeResult]):
    """Поставить лайк на комментарий к публикации"""

    comment_id: str  # 17873106636540219


class CommentsLikeHandler(CommandHandler[CommentsLike, CommentsLikeResult]):
    def __init__(
        self,
        api_requester: WebApiRequester,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: CommentsLike) -> CommentsLikeResult:
        self.state.csrftoken_guard()
        return cast(
            CommentsLikeResult,
            await self.api_requester.execute(
                method="POST",
                url=constants.COMMENTS_LIKE_URL.format(comment_id=command.comment_id),
            ),
        )
