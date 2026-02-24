from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.commands._responses.friendships.destroy import (
    FriendshipsDestroyResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class FriendshipsDestroy(Command[FriendshipsDestroyResult]):
    """Подписаться на пользователя"""

    user_id: str


class FriendshipsDestroyHandler(CommandHandler[FriendshipsDestroy, FriendshipsDestroyResult]):
    def __init__(
        self,
        api_requester: Any,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: FriendshipsDestroy) -> FriendshipsDestroyResult:
        self.state.csrftoken_guard()

        data = {
            "container_module": "single_post",
            "nav_chain": "PolarisFeedRoot:feedPage:1:via_cold_start,PolarisProfilePostsTabRoot:profilePage:2:unexpected,PolarisPostModal:postPage:6:modalLink",
            "user_id": str(command.user_id),
            "jazoest": generate_jazoest(self.state.csrftoken),
        }

        return cast(
            FriendshipsDestroyResult,
            await self.api_requester.execute(
                method="POST",
                url=constants.FRIENDSHIPS_DESTROY_URL.format(user_id=command.user_id),
                data=data,
            ),
        )
