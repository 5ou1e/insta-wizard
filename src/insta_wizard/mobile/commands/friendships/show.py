from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.friendships.friendships_show import (
    FriendshipsShowResponse,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class FriendshipsShow(Command[FriendshipsShowResponse]):
    """Get friendship status with a user"""

    user_id: list[str | int]


class FriendshipsShowHandler(CommandHandler[FriendshipsShow, FriendshipsShowResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: FriendshipsShow) -> FriendshipsShowResponse:
        resp = await self.api.call_api(
            method="GET",
            uri=constants.FRIENDSHIPS_SHOW_URI.format(user_id=command.user_id),
        )
        return cast(FriendshipsShowResponse, resp)
