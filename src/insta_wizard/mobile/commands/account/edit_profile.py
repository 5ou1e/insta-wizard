from dataclasses import dataclass
from typing import Literal, cast

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
from insta_wizard.mobile.responses.account.account_edit_profile import (
    AccountEditProfileResponse,
)


@dataclass(slots=True)
class AccountEditProfile(Command[AccountEditProfileResponse]):
    """Edit account info (requires authentication)"""

    username: str
    first_name: str | None
    biography: str | None
    external_url: str | None
    email: str
    phone_number: str | None
    gender: Literal[1, 2, 3]


class AccountEditProfileHandler(CommandHandler[AccountEditProfile, AccountEditProfileResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: AccountEditProfile) -> AccountEditProfileResponse:

        data = {
            "_uuid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "username": command.username,
            "gender": command.gender,
            "phone_number": command.phone_number or "",
            "first_name": command.first_name or "",
            "biography": command.biography or "",
            "external_url": command.external_url or "",
            "email": command.email,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_EDIT_PROFILE_URI,
            data=data,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(AccountEditProfileResponse, resp)
