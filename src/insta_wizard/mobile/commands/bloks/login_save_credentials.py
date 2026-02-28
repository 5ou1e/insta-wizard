from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import dumps
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
from insta_wizard.mobile.responses.bloks.login_save_credentials import (
    BloksLoginSaveCredentialsBApiResponse,
)


@dataclass(slots=True)
class BloksLoginSaveCredentialsBApi(Command[BloksLoginSaveCredentialsBApiResponse]):
    pass


class BloksLoginSaveCredentialsBApiHandler(
    CommandHandler[BloksLoginSaveCredentialsBApi, BloksLoginSaveCredentialsBApiResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: BloksLoginSaveCredentialsBApi,
    ) -> BloksLoginSaveCredentialsBApiResponse:
        data = {
            "qe_device_id": self.state.device.device_id,
            "offline_experiment_group": self.state.version_info.offline_experiment_group,
            "_uuid": self.state.device.device_id,
            "family_device_id": self.state.device.phone_id,
            "bk_client_context": dumps(
                {
                    "bloks_version": self.state.version_info.bloks_version_id,
                    "styles_id": "instagram",
                }
            ),
            "bloks_versioning_id": self.state.version_info.bloks_version_id,
        }

        res = await self.api.call_b_api(
            method="POST",
            uri=constants.BLOKS_LOGIN_SAVE_CREDENTIALS_URI,
            data=data,
            extra_headers={
                "X-Bloks-Prism-Button-Version": "CONTROL",
            },
        )
        return cast(BloksLoginSaveCredentialsBApiResponse, res)
