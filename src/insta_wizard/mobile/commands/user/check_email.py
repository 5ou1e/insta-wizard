from dataclasses import dataclass
from typing import TypedDict

from insta_wizard.common.generators import generate_uuid_v4_string
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


class UsersCheckEmailResponse(TypedDict):
    pass


@dataclass(slots=True)
class UsersCheckEmail(Command[UsersCheckEmailResponse]):
    """Check email address availability"""

    email: str
    waterfall_id: str


class UsersCheckEmailHandler(CommandHandler[UsersCheckEmail, UsersCheckEmailResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: UsersCheckEmail) -> UsersCheckEmailResponse:
        payload = {
            "android_device_id": self.state.device.android_id,
            "login_nonce_map": "{}",
            "login_nonces": "[]",
            "email": command.email,
            "qe_id": generate_uuid_v4_string(),
            "waterfall_id": command.waterfall_id,
        }
        data = build_signed_body(payload)

        resp = await self.requester.call_api(
            method="POST",
            data=data,
            uri=constants.USERS_CHECK_EMAIL_URI,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return resp
