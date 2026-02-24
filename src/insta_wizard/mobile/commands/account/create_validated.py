import base64
import os
import time
from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.common.password_encrypter import (
    PasswordEncrypter,
)
from insta_wizard.mobile.commands._responses.account.account_create_validated import (
    AccountCreateValidatedResponse,
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
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class AccountCreateValidated(Command[AccountCreateValidatedResponse]):
    username: str
    password: str
    first_name: str
    code: int | str
    phone_number: str
    day: int
    month: int
    year: int
    tos_version: str = "row"


class AccountCreateValidatedHandler(
    CommandHandler[AccountCreateValidated, AccountCreateValidatedResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: AccountCreateValidated) -> AccountCreateValidatedResponse:
        enc_password = PasswordEncrypter.encrypt_v0(command.password)

        def generate_sn_nonce_1() -> str:
            # API sharp
            # $"{emailOrPhoneNumber}|{DateTimeHelper.ToUnixTime(DateTime.UtcNow)}|{Encoding.UTF8.GetString(b)}";
            b = os.urandom(24)
            ts = int(time.time())

            s = f"{command.phone_number}|{ts}|{b.decode('utf-8', errors='replace')}"
            return base64.b64encode(s.encode("utf-8")).decode("ascii")

        def generate_sn_nonce_2() -> str:
            # aiograpi
            timestamp = str(int(time.time()))
            nonce = f'{command.phone_number}|{timestamp}|\xb9F"\x8c\xa2I\xaaz|\xf6xz\x86\x92\x91Y\xa5\xaa#f*o%\x7f'
            sn_nonce = base64.encodebytes(nonce.encode()).decode().strip()
            return sn_nonce

        sn_nonce = generate_sn_nonce_1()

        enc_password = PasswordEncrypter.encrypt_v0(command.password)
        data = {
            "jazoest": generate_jazoest(self.state.device.phone_id),
            "is_secondary_account_creation": "false",
            "tos_version": command.tos_version,
            "suggestedUsername": "",
            "verification_code": str(command.code),
            "do_not_auto_login_if_credentials_match": "true",
            "phone_id": self.state.device.phone_id,
            "enc_password": enc_password,
            "phone_number": str(command.phone_number),
            "username": command.username,
            "first_name": command.first_name,
            "day": str(command.day),
            "adid": self.state.device.adid,
            "guid": self.state.device.device_id,
            "year": str(command.year),
            "device_id": self.state.device.android_id,
            "_uuid": self.state.device.device_id,
            "month": str(command.month),
            "force_sign_up_code": "",
            "waterfall_id": self.state.local_data.waterfall_id,
            "has_sms_consent": "true",
            "one_tap_opt_in": "true",
            "qs_stamp": "",  # not send in aiograpi for sms-reg flow
            # "_csrftoken": self.token,  # C#
            "sn_nonce": sn_nonce,
            "sn_result": "GOOGLE_PLAY_UNAVAILABLE:SERVICE_INVALID",  # or "sn_result": "MLA" or "API_ERROR:+null" (API sharp) or "API_ERROR: class X.2mY:7: "
        }
        payload = build_signed_body(data)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_CREATE_VALIDATED_URI,
            data=payload,
        )

        return cast(AccountCreateValidatedResponse, resp)
