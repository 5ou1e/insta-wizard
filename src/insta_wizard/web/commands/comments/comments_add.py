from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.commands._responses.comments.comments_add import (
    CommentsAddResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import WebApiRequester
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class CommentsAdd(Command[CommentsAddResult]):
    """Add a comment to a media post"""

    media_id: str  # 3772108794026055709
    replied_to_comment_id: str  # comment_id 17925698052169518


class CommentsAddHandler(CommandHandler[CommentsAdd, CommentsAddResult]):
    def __init__(
        self,
        api_requester: WebApiRequester,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: CommentsAdd) -> CommentsAddResult:
        self.state.csrftoken_guard()

        data = {
            "comment_text": "profile",
        }
        if command.replied_to_comment_id:
            data["replied_to_comment_id"] = command.replied_to_comment_id

        data.update({"jazoest": generate_jazoest(self.state.csrftoken)})

        return cast(
            CommentsAddResult,
            await self.api_requester.execute(
                method="POST",
                url=constants.COMMENTS_ADD_URL.format(media_id=command.media_id),
                data=data,
            ),
        )
