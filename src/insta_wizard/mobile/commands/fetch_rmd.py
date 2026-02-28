from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, cast

from yarl import URL

from insta_wizard.common.generators import uuid_v4_hex
from insta_wizard.common.transport.models import HttpRequest
from insta_wizard.common.utils import (
    dumps,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.requester import (
    RequestExecutor,
)
from insta_wizard.mobile.common.utils import (
    instagram_android_user_agent_from_android_device_info,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.models.version import (
    InstagramAppVersion,
)
from insta_wizard.mobile.responses.fetch_rmd import FetchRmdResponse


@dataclass(slots=True)
class FetchRmd(Command[FetchRmdResponse]):
    reason: Literal["SESSION_CHANGE", "APP_RESUME"] = "SESSION_CHANGE"


class FetchRmdHandler(CommandHandler[FetchRmd, FetchRmdResponse]):
    def __init__(
        self,
        request_executor: RequestExecutor,
        state: MobileClientState,
    ) -> None:
        self.request_executor = request_executor
        self.state = state

    async def __call__(self, command: FetchRmd) -> FetchRmdResponse:
        version_info = self.state.version_info

        headers = {
            "priority": "u=3, i",
            "x-fb-client-ip": "True",
            "x-fb-friendly-name": "rmd-mapfetcher",
            "x-fb-request-analytics-tags": dumps(
                {
                    "network_tags": {
                        "product": version_info.app_id,
                        "purpose": "none",
                        "retry_attempt": "0",
                    },
                    "application_tags": "rmd",
                }
            ),
            "x-fb-server-cluster": "True",
            "X-Ig-App-Id": version_info.app_id,
            "x-ig-capabilities": version_info.capabilities,
            "x-tigon-is-retry": "False",
            "accept-encoding": "zstd",
            "user-agent": instagram_android_user_agent_from_android_device_info(
                self.state.device,
                version_info,
            ),
            "x-fb-conn-uuid-client": uuid_v4_hex(),
            "x-fb-http-engine": "MNS/TCP",
            "X-Fb-Rmd": "state=URL_ELIGIBLE",
        }

        if version_info.version == InstagramAppVersion.V374:
            headers["x-fb-privacy-context"] = "4760009080727693"

        params = {
            "access_token": version_info.access_token,
            "rule_context": "instagram_prod",
            "net_iface": "Unknown",
            "reason": command.reason,
        }

        resp = await self.request_executor(
            HttpRequest(
                method="POST",
                url=URL(constants.BASE_INSTAGRAM_URL) / "rmd/",
                headers=headers,
                params=params,
            )
        )
        return cast(FetchRmdResponse, resp)
