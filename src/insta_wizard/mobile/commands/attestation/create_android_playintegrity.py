from dataclasses import dataclass
from typing import cast

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
from insta_wizard.mobile.responses.attestation.create_android_playintegrity import (
    AttestationCreateAndroidPlayIntegrityResponse,
)


@dataclass(slots=True)
class AttestationCreateAndroidPlayIntegrity(Command[AttestationCreateAndroidPlayIntegrityResponse]):
    pass


class AttestationCreateAndroidPlayIntegrityHandler(
    CommandHandler[
        AttestationCreateAndroidPlayIntegrity,
        AttestationCreateAndroidPlayIntegrityResponse,
    ]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(
        self,
        command: AttestationCreateAndroidPlayIntegrity,
    ) -> AttestationCreateAndroidPlayIntegrityResponse:
        data = {"app_scoped_device_id": self.state.device.device_id}

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.ATTESTATION_CREATE_ANDROID_PLAYINTEGRITY_URI,
            data=data,
        )
        return cast(AttestationCreateAndroidPlayIntegrityResponse, resp)
