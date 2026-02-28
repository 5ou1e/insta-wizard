from dataclasses import dataclass

from insta_wizard.mobile.commands._responses.user.check_username import (
    UsersCheckUsernameResponse,
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
class UsersCheckUsername(Command[UsersCheckUsernameResponse]):
    """Check username availability"""

    username: str


class UsersCheckUsernameHandler(CommandHandler[UsersCheckUsername, UsersCheckUsernameResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: UsersCheckUsername) -> UsersCheckUsernameResponse:
        data = {"username": command.username}
        resp = await self.api.call_api(
            method="POST",
            data=data,
            uri=constants.USERS_CHECK_USERNAME,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return resp
