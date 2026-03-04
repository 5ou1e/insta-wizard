import base64
import os
import time
from dataclasses import dataclass
from typing import TypedDict, cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.common.password_encrypter import (
    PasswordEncrypter,
)
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


class AccountCreateResponse(TypedDict):
    pass


@dataclass(kw_only=True, slots=True)
class AccountCreate(Command[AccountCreateResponse]):
    username: str
    password: str
    first_name: str
    signup_code: str  # {'signup_code': 'W2FEqjYL', 'status': 'ok'}
    email: str
    day: int
    month: int
    year: int
    tos_version: str = "row"
    waterfall_id: str


class AccountCreateHandler(CommandHandler[AccountCreate, AccountCreateResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: AccountCreate) -> AccountCreateResponse:

        def generate_sn_nonce_1() -> str:
            # API sharp
            # $"{emailOrPhoneNumber}|{DateTimeHelper.ToUnixTime(DateTime.UtcNow)}|{Encoding.UTF8.GetString(b)}";
            b = os.urandom(24)
            ts = int(time.time())

            s = f"{command.email}|{ts}|{b.decode('utf-8', errors='replace')}"
            return base64.b64encode(s.encode("utf-8")).decode("ascii")

        sn_nonce = generate_sn_nonce_1()

        enc_password = PasswordEncrypter.encrypt_v0(command.password)

        data = {
            "jazoest": generate_jazoest(self.state.device.phone_id),
            "is_secondary_account_creation": "false",
            "tos_version": command.tos_version,
            "suggestedUsername": "",
            "do_not_auto_login_if_credentials_match": "true",
            "phone_id": self.state.device.phone_id,
            "enc_password": enc_password,
            "username": command.username,
            "first_name": command.first_name,
            "day": str(command.day),
            "adid": self.state.device.adid,
            "guid": self.state.device.device_id,
            "year": str(command.year),
            "device_id": self.state.device.android_id,
            "_uuid": self.state.device.device_id,
            "month": str(command.month),
            "email": command.email,
            "force_sign_up_code": command.signup_code,
            "waterfall_id": command.waterfall_id,
            "has_sms_consent": "true",
            "one_tap_opt_in": "true",
            "qs_stamp": "",
            "sn_nonce": sn_nonce,
            "sn_result": "GOOGLE_PLAY_UNAVAILABLE:SERVICE_INVALID",  # or "sn_result": "MLA" or "API_ERROR:+null" (API sharp) or "API_ERROR: class X.2mY:7: "
        }
        payload = build_signed_body(data)

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.ACCOUNTS_CREATE_URI,
            data=payload,
        )

        return cast(AccountCreateResponse, resp)
