from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.attestation.create_android_keystore_b_api import (
    AttestationCreateAndroidKeystoreResponse,
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
class AttestationCreateAndroidKeystore(Command[AttestationCreateAndroidKeystoreResponse]):
    key_hash: str | None = None


class AttestationCreateAndroidKeystoreHandler(
    CommandHandler[
        AttestationCreateAndroidKeystore,
        AttestationCreateAndroidKeystoreResponse,
    ]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: AttestationCreateAndroidKeystore,
    ) -> AttestationCreateAndroidKeystoreResponse:
        data = {
            "app_scoped_device_id": self.state.device.device_id,
            "key_hash": command.key_hash or "",
        }

        resp = await self.api.call_b_api(
            method="POST",
            uri=constants.ATTESTATION_CREATE_ANDROID_KEYSTORE_URI,
            data=data,
        )
        return cast(AttestationCreateAndroidKeystoreResponse, resp)
