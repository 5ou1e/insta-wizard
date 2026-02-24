from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.web.commands._responses.friendships.follow import (
    FriendshipsFollowResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class FriendshipsFollow(Command[FriendshipsFollowResult]):
    """Follow a user"""

    user_id: str


class FriendshipsFollowHandler(CommandHandler[FriendshipsFollow, FriendshipsFollowResult]):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: FriendshipsFollow) -> FriendshipsFollowResult:
        self.state.csrftoken_guard()

        data = {}

        # jazoest = generate_jazoest(csrftoken)
        # data = {
        #     "container_module": "profile",
        #     "nav_chain": "PolarisOneTapAfterLoginRoot:OneTapUpsellPage:1:via_cold_start,PolarisFeedRoot:feedPage:2:unexpected,PolarisProfilePostsTabRoot:profilePage:3:unexpected,PolarisProfilePostsTabRoot:profilePage:4:unexpected",
        #     "user_id": str(user_id),
        #     "jazoest": jazoest,
        # }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.FRIENDSHIPS_FOLLOW_URL.format(user_id=command.user_id),
            data=data,
        )
        return cast(FriendshipsFollowResult, resp)
