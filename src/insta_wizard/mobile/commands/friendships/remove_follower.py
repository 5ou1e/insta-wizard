from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.friendships.friendships_remove_follower import (
    FriendshipsRemoveFollowerResponse,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.exceptions import (
    NotFoundError,
    UserIdNotFound,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class FriendshipsRemoveFollower(Command[FriendshipsRemoveFollowerResponse]):
    """Remove a user from your followers"""

    user_id: str


class FriendshipsRemoveFollowerHandler(
    CommandHandler[FriendshipsRemoveFollower, FriendshipsRemoveFollowerResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: FriendshipsRemoveFollower
    ) -> FriendshipsRemoveFollowerResponse:
        data = {
            "_uid": self.state.local_data.user_id,
            "device_id": self.state.device.android_id,
            "_uuid": self.state.device.device_id,
            "radio_type": self.state.radio_type,
            "user_id": str(command.user_id),
            "include_follow_friction_check": "1",
        }

        payload = build_signed_body(data)

        try:
            resp = await self.api.call_api(
                method="POST",
                uri=constants.FRIENDSHIPS_REMOVE_FOLLOWER_URI.format(user_id=command.user_id),
                data=payload,
                client_endpoint="following",
                extra_headers={
                    "X-Bloks-Prism-Button-Version": "INDIGO_PRIMARY_BORDERED_SECONDARY",
                },
            )
        except NotFoundError as e:
            raise UserIdNotFound() from e

        return cast(FriendshipsRemoveFollowerResponse, resp)
