from dataclasses import dataclass
from typing import cast

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
from insta_wizard.mobile.responses.write_supported_capabilities import (
    CreativesWriteSupportedCapabilitiesResponse,
)


@dataclass(slots=True)
class CreativesWriteSupportedCapabilities(Command[CreativesWriteSupportedCapabilitiesResponse]):
    pass


class CreativesWriteSupportedCapabilitiesHandler(
    CommandHandler[
        CreativesWriteSupportedCapabilities,
        CreativesWriteSupportedCapabilitiesResponse,
    ]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: CreativesWriteSupportedCapabilities,
    ) -> CreativesWriteSupportedCapabilitiesResponse:
        data = {
            "supported_capabilities_new": '[{"name":"SUPPORTED_SDK_VERSIONS","value":"149.0,150.0,151.0,152.0,153.0,154.0,155.0,156.0,157.0,158.0,159.0,160.0,161.0,162.0,163.0,164.0,165.0,166.0,167.0,168.0,169.0,170.0,171.0,172.0,173.0,174.0,175.0,176.0,177.0,178.0,179.0,180.0,181.0,182.0,183.0,184.0,185.0,186.0,187.0,188.0,189.0,190.0,191.0"},{"name":"SUPPORTED_BETA_SDK_VERSIONS","value":"182.0-beta,183.0-beta,184.0-beta,185.0-beta,186.0-beta,187.0-beta,188.0-beta,189.0-beta,190.0-beta,191.0-beta,192.0-beta,193.0-beta,194.0-beta,195.0-beta,196.0-beta,197.0-beta,198.0-beta,199.0-beta,200.0-beta,201.0-beta"},{"name":"FACE_TRACKER_VERSION","value":"14"},{"name":"segmentation","value":"segmentation_enabled"},{"name":"COMPRESSION","value":"ETC2_COMPRESSION"},{"name":"world_tracker","value":"world_tracker_enabled"},{"name":"gyroscope","value":"gyroscope_enabled"}]',
            "_uid": self.state.local_data.user_id,
            "_uuid": self.state.device.device_id,
        }

        payload = build_signed_body(data)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.CREATIVES_WRITE_SUPPORTED_CAPABILITIES_URI,
            data=payload,
            client_endpoint="feed_timeline",
            extra_headers={
                "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            },
        )
        return cast(CreativesWriteSupportedCapabilitiesResponse, resp)
