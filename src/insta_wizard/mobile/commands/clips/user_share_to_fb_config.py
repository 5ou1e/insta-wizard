from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import dumps
from insta_wizard.mobile.commands._responses.clips.share_to_fb_config import (
    ClipsUserShareToFbConfigResponse,
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
class ClipsUserShareToFbConfig(Command[ClipsUserShareToFbConfigResponse]):
    pass


class ClipsUserShareToFbConfigHandler(
    CommandHandler[ClipsUserShareToFbConfig, ClipsUserShareToFbConfigResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: ClipsUserShareToFbConfig) -> ClipsUserShareToFbConfigResponse:
        device_status = {
            "hw_av1_dec": False,
            "hw_vp9_dec": True,
            "hw_avc_dec": True,
            "10bit_hw_av1_dec": False,
            "10bit_hw_vp9_dec": False,
            "is_hlg_supported": False,
            "chip_vendor": "mediatek",
            "chip_name": "mt6789v/cd",
            "core_count": 8,
            "max_ghz_sum": 16.4,
            "min_ghz_sum": 4.45,
        }
        params = {"device_status": dumps(device_status)}

        resp = await self.api.call_api(
            method="GET",
            uri=constants.CLIPS_USER_SHARE_TO_FB_CONFIG_URI,
            params=params,
            client_endpoint="feed_timeline",
        )
        return cast(ClipsUserShareToFbConfigResponse, resp)
