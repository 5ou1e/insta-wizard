from dataclasses import dataclass
from typing import cast

from insta_wizard.web.commands._responses.comments.comments_unlike import (
    CommentsUnlikeResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import WebApiRequester
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class CommentsUnlike(Command[CommentsUnlikeResult]):
    """Unlike a comment on a media post"""

    comment_id: str  # 17873106636540219


class CommentsUnlikeHandler(CommandHandler[CommentsUnlike, CommentsUnlikeResult]):
    def __init__(
        self,
        api_requester: WebApiRequester,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: CommentsUnlike) -> CommentsUnlikeResult:
        self.state.csrftoken_guard()
        return cast(
            CommentsUnlikeResult,
            await self.api_requester.execute(
                method="POST",
                url=constants.COMMENTS_UNLIKE_URL.format(comment_id=command.comment_id),
            ),
        )
