from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import (
    generate_uuid_v4_string,
)
from insta_wizard.mobile.commands._responses.friendships.friendships_user_followers import (
    FriendshipsUserFollowersResponse,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.exceptions import (
    MobileClientError,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class FriendshipsUserFollowers(Command[FriendshipsUserFollowersResponse]):
    """Get user followers (supports search via query parameter)"""

    user_id: str
    query: str | None = None
    max_id: int | None = None


class FriendshipsUserFollowersHandler(
    CommandHandler[FriendshipsUserFollowers, FriendshipsUserFollowersResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: FriendshipsUserFollowers) -> FriendshipsUserFollowersResponse:
        params = {
            "rank_token": generate_uuid_v4_string(),
        }
        if command.max_id:
            params["max_id"] = (str(command.max_id),)

        if command.query:
            params.update(
                {
                    "search_surface": "follow_list_page",
                    "query": command.query,
                    "enable_groups": "true",
                }
            )

        resp = await self.api.call_api(
            method="GET",
            uri=constants.FRIENDSHIPS_USER_FOLLOWERS_URI.format(user_id=command.user_id),
            params=params,
        )

        if resp.get("status") == "ok":
            return cast(FriendshipsUserFollowersResponse, resp)

        raise MobileClientError()
