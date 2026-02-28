from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import WebApiRequester
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.comments.comments_add import (
    CommentsAddResponse,
)


@dataclass(slots=True)
class CommentsAdd(Command[CommentsAddResponse]):
    """Add a comment to a media post"""

    media_id: str  # 3772108794026055709
    text: str
    replied_to_comment_id: str | None = None  # comment_id 17925698052169518


class CommentsAddHandler(CommandHandler[CommentsAdd, CommentsAddResponse]):
    def __init__(
        self,
        api_requester: WebApiRequester,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: CommentsAdd) -> CommentsAddResponse:
        self.state.csrftoken_guard()

        data = {
            "comment_text": command.text,
        }
        if command.replied_to_comment_id:
            data["replied_to_comment_id"] = command.replied_to_comment_id

        data.update({"jazoest": generate_jazoest(self.state.csrftoken)})

        return cast(
            CommentsAddResponse,
            await self.api_requester.execute(
                method="POST",
                url=constants.COMMENTS_ADD_URL.format(media_id=command.media_id),
                data=data,
            ),
        )
