from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.responses.friendships.friendships_show import (
    FriendshipsShowResponse,
)


@dataclass(slots=True)
class FriendshipsShow(Command[FriendshipsShowResponse]):
    """Get friendship status with a user"""

    user_id: str


class FriendshipsShowHandler(CommandHandler[FriendshipsShow, FriendshipsShowResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: FriendshipsShow) -> FriendshipsShowResponse:
        resp = await self.requester.call_api(
            method="GET",
            uri=constants.FRIENDSHIPS_SHOW_URI.format(user_id=command.user_id),
        )
        return cast(FriendshipsShowResponse, resp)
