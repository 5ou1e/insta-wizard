from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import current_timestamp_str
from insta_wizard.common.utils import (
    dumps,
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
from insta_wizard.mobile.responses.launcher.launcher_mobile_config_b_api import (
    LauncherMobileConfigBApiResponse,
)


@dataclass(slots=True)
class LauncherMobileConfigBApi(Command[LauncherMobileConfigBApiResponse]):
    pass


class LauncherMobileConfigBApiHandler(
    CommandHandler[LauncherMobileConfigBApi, LauncherMobileConfigBApiResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: LauncherMobileConfigBApi) -> LauncherMobileConfigBApiResponse:
        data = {
            "bool_opt_policy": "0",
            "mobileconfigsessionless": "",
            "api_version": "10",
            "client_context": dumps(["opt,value_hash"]),
            "unit_type": "1",
            "use_case": "STANDARD",
            "query_hash": "464db3b19f7c9bc4be6a32adafb0d83c63c20ab88427123f500c5b1a15fb533c",
            "ts": current_timestamp_str(),
            "device_id": self.state.device.device_id,
            "fetch_mode": "CONFIG_SYNC_ONLY",
            "fetch_type": "ASYNC_FULL",
            "family_device_id": self.state.device.device_id.upper(),
        }

        payload = build_signed_body(data)

        uri = constants.LAUNCHER_MOBILE_CONFIG_URI
        resp = await self.api.call_b_api(
            method="POST",
            uri=uri,
            data=payload,
            client_endpoint="com.bloks.www.caa.login.save-credentials",
            extra_headers={"X-Fb-Friendly-Name": f"IgApi: {uri}/sessionless"},
        )
        return cast(LauncherMobileConfigBApiResponse, resp)
