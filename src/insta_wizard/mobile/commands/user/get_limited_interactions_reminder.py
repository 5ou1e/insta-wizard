from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import (
    dumps,
)
from insta_wizard.mobile.commands._responses.user.get_limited_interactions_reminder import (
    UserGetLimitedInteractionsReminderResponse,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.common.utils import (
    build_signed_body_value,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class UserGetLimitedInteractionsReminder(Command[UserGetLimitedInteractionsReminderResponse]):
    pass


class UserGetLimitedInteractionsReminderHandler(
    CommandHandler[
        UserGetLimitedInteractionsReminder,
        UserGetLimitedInteractionsReminderResponse,
    ]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self._api = api
        self._state = state

    async def __call__(
        self,
        command: UserGetLimitedInteractionsReminder,
    ) -> UserGetLimitedInteractionsReminderResponse:
        params = {"signed_body": build_signed_body_value(dumps({}))}

        data = await self._api.call_api(
            method="GET",
            uri=constants.USERS_GET_LIMITED_INTERACTIONS_REMINDER_URI,
            params=params,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
            extra_headers={
                "x-ig-nav-chain": (
                    "com.bloks.www.caa.login.login_homepage:"
                    "com.bloks.www.caa.login.login_homepage:1:button:1755922723.851::,"
                    "com.bloks.www.caa.login.login_homepage:"
                    "com.bloks.www.caa.login.login_homepage:2:button:1755922727.92::"
                ),
            },
        )
        return cast(UserGetLimitedInteractionsReminderResponse, data)
