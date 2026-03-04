from dataclasses import dataclass

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
from insta_wizard.mobile.responses.user.check_username import UsersCheckUsernameResponse


@dataclass(slots=True)
class UsersCheckUsername(Command[UsersCheckUsernameResponse]):
    """Check username availability"""

    username: str


class UsersCheckUsernameHandler(CommandHandler[UsersCheckUsername, UsersCheckUsernameResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: UsersCheckUsername) -> UsersCheckUsernameResponse:
        data = {"username": command.username}
        resp = await self.requester.call_api(
            method="POST",
            data=data,
            uri=constants.USERS_CHECK_USERNAME_URI,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return resp
