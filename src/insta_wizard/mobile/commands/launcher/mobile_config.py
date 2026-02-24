from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import current_timestamp_str
from insta_wizard.common.utils import (
    dumps,
)
from insta_wizard.mobile.commands._responses.launcher.launcher_mobile_config import (
    LauncherMobileConfigResponse,
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
class LauncherMobileConfig(Command[LauncherMobileConfigResponse]):
    pass


class LauncherMobileConfigHandler(
    CommandHandler[LauncherMobileConfig, LauncherMobileConfigResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: LauncherMobileConfig) -> LauncherMobileConfigResponse:
        data = {
            "bool_opt_policy": "0",
            "mobileconfig": "",
            "api_version": "3",
            "client_context": dumps(["opt,value_hash"]),
            "unit_type": "2",
            "use_case": "STANDARD",
            "query_hash": "afbf25f577b10c6784e55995f46fac65b39623739edd37210e7b39e830c28026",
            "ts": current_timestamp_str(),
            "_uid": self.state.local_data.user_id,
            "device_id": self.state.device.device_id,
            "_uuid": self.state.device.device_id,
            "fetch_mode": "CONFIG_SYNC_ONLY",
            "fetch_type": "ASYNC_FULL",
            "request_data_query_hash": "afbf25f577b10c6784e55995f46fac65b39623739edd37210e7b39e830c28026",
        }

        payload = build_signed_body(data)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.LAUNCHER_MOBILE_CONFIG_URI,
            data=payload,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(LauncherMobileConfigResponse, resp)
