from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.commands._responses.friendships.create import (
    FriendshipsCreateResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class FriendshipsCreate(Command[FriendshipsCreateResult]):
    """Подписаться на пользователя"""

    user_id: str


class FriendshipsCreateHandler(CommandHandler[FriendshipsCreate, FriendshipsCreateResult]):
    def __init__(
        self,
        api_requester: Any,
        state: WebClientState,
    ) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: FriendshipsCreate) -> FriendshipsCreateResult:
        self.state.csrftoken_guard()

        jazoest = generate_jazoest(self.state.csrftoken)

        data = {
            "container_module": "profile",
            "nav_chain": "PolarisOneTapAfterLoginRoot:OneTapUpsellPage:1:via_cold_start,PolarisFeedRoot:feedPage:2:unexpected,PolarisProfilePostsTabRoot:profilePage:3:unexpected,PolarisProfilePostsTabRoot:profilePage:4:unexpected",
            "user_id": str(command.user_id),
            "jazoest": jazoest,
        }

        return cast(
            FriendshipsCreateResult,
            await self.api_requester.execute(
                method="POST",
                url=constants.FRIENDSHIPS_CREATE_URL.format(user_id=command.user_id),
                data=data,
            ),
        )
