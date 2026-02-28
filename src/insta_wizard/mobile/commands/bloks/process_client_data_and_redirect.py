from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import (
    generate_uuid_v4_string,
)
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
from insta_wizard.mobile.responses.bloks.process_client_data_and_redirect import (
    BloksProcessClientDataAndRedirectBApiResponse,
)


@dataclass(slots=True)
class BloksProcessClientDataAndRedirectBApi(Command[BloksProcessClientDataAndRedirectBApiResponse]):
    waterfall_id: str


class BloksProcessClientDataAndRedirectBApiHandler(
    CommandHandler[
        BloksProcessClientDataAndRedirectBApi,
        BloksProcessClientDataAndRedirectBApiResponse,
    ]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: BloksProcessClientDataAndRedirectBApi,
    ) -> BloksProcessClientDataAndRedirectBApiResponse:
        data = {
            "params": dumps(
                {
                    "is_from_logged_out": False,
                    "logged_out_user": "",
                    "qpl_join_id": generate_uuid_v4_string(),
                    "family_device_id": False,
                    "device_id": self.state.device.android_id,
                    "offline_experiment_group": self.state.version_info.offline_experiment_group,
                    "waterfall_id": command.waterfall_id,
                    "logout_source": "",
                    "show_internal_settings": False,
                    "last_auto_login_time": 0,
                    "disable_auto_login": False,
                    "qe_device_id": self.state.device.device_id,
                    "is_from_logged_in_switcher": False,
                    "switcher_logged_in_uid": "",
                    "account_list": [],
                    "blocked_uid": [],
                    "INTERNAL_INFRA_THEME": "THREE_C",
                    "launched_url": "",
                    "sim_phone_numbers": [],
                    "is_from_registration_reminder": False,
                }
            ),
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
            uri=constants.BLOKS_PROCESS_CLIENT_DATA_AND_REDIRECT_URI,
            data=data,
            extra_headers={
                "X-Bloks-Prism-Button-Version": "CONTROL",
            },
        )
        return cast(BloksProcessClientDataAndRedirectBApiResponse, res)
