from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.friendships.friendships_show_many import (
    FriendshipsShowManyResponse,
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
class FriendshipsShowMany(Command[FriendshipsShowManyResponse]):
    """Get friendship status for multiple users"""

    user_ids: list[str | int]


class FriendshipsShowManyHandler(CommandHandler[FriendshipsShowMany, FriendshipsShowManyResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: FriendshipsShowMany) -> FriendshipsShowManyResponse:
        data = {
            "user_ids": ",".join(map(str, command.user_ids)),
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.FRIENDSHIPS_SHOW_MANY_URI,
            data=data,
        )
        return cast(FriendshipsShowManyResponse, resp)
