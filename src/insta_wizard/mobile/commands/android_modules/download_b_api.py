from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.android_modules.download_b_api import (
    AndroidModulesDownloadResponse,
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
class AndroidModulesDownload(Command[AndroidModulesDownloadResponse]):
    pass


class AndroidModulesDownloadHandler(
    CommandHandler[AndroidModulesDownload, AndroidModulesDownloadResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: AndroidModulesDownload,
    ) -> AndroidModulesDownloadResponse:
        data = {
            "_uid": self.state.local_data.user_id,
            "_uuid": self.state.device.device_id,
            "hashes": [
                "50b2a8f3ac5fec83e70988463fb695adb29d10e9fef26d61724ff39bebf5b6e9",
                "59508dd222b8bb6a0af90331f016f9632f8147c91a2a6767dfb36d504a0f7679",
            ],
        }

        payload = build_signed_body(data)

        resp = await self.api.call_b_api(
            method="POST",
            uri=constants.ANDROID_MODULES_DOWNLOAD_URI,
            data=payload,
        )
        return cast(AndroidModulesDownloadResponse, resp)
