from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.friendships.destroy import (
    FriendshipsDestroyResponse,
)


@dataclass(slots=True)
class FriendshipsDestroy(Command[FriendshipsDestroyResponse]):
    """Unfollow a user"""

    user_id: str


class FriendshipsDestroyHandler(CommandHandler[FriendshipsDestroy, FriendshipsDestroyResponse]):
    def __init__(
        self,
        api_requester: Any,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: FriendshipsDestroy) -> FriendshipsDestroyResponse:
        self.state.csrftoken_guard()

        data = {
            "container_module": "single_post",
            "nav_chain": "PolarisFeedRoot:feedPage:1:via_cold_start,PolarisProfilePostsTabRoot:profilePage:2:unexpected,PolarisPostModal:postPage:6:modalLink",
            "user_id": str(command.user_id),
            "jazoest": generate_jazoest(self.state.csrftoken),
        }

        return cast(
            FriendshipsDestroyResponse,
            await self.api_requester.execute(
                method="POST",
                url=constants.FRIENDSHIPS_DESTROY_URL.format(user_id=command.user_id),
                data=data,
            ),
        )
