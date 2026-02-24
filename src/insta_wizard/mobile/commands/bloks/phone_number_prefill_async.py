from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import dumps
from insta_wizard.mobile.commands._responses.bloks.phone_number_prefill_async import (
    BloksPhoneNumberPrefillAsyncResponse,
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
class BloksPhoneNumberPrefillAsync(Command[BloksPhoneNumberPrefillAsyncResponse]):
    pass


class BloksPhoneNumberPrefillAsyncHandler(
    CommandHandler[BloksPhoneNumberPrefillAsync, BloksPhoneNumberPrefillAsyncResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: BloksPhoneNumberPrefillAsync
    ) -> BloksPhoneNumberPrefillAsyncResponse:
        data = {
            "params": dumps(
                {
                    "client_input_params": {
                        "user_name_field_text": "",
                        "lois_settings": {"lois_token": ""},
                        "phone_number": None,
                    },
                    "server_params": {
                        "is_from_logged_out": 0,
                        "layered_homepage_experiment_group": None,
                        "device_id": self.state.device.android_id,
                        "waterfall_id": self.state.local_data.waterfall_id,
                        "INTERNAL__latency_qpl_instance_id": 111393086300282.0,
                        "source": "prefill_login_form",
                        "is_platform_login": 0,
                        "INTERNAL__latency_qpl_marker_id": self.state.version_info.qpl_marker_id,
                        "family_device_id": self.state.device.phone_id,
                        "offline_experiment_group": self.state.version_info.offline_experiment_group,
                        "access_flow_version": "pre_mt_behavior",
                        "is_from_logged_in_switcher": 0,
                        "qe_device_id": self.state.device.device_id,
                    },
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

        res = await self.api.call_api(
            method="POST",
            uri=constants.BLOKS_PHONE_NUMBER_PREFILL_ASYNC_URI,
            data=data,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
            extra_headers={
                "X-Bloks-Prism-Button-Version": "CONTROL",
            },
        )
        return cast(BloksPhoneNumberPrefillAsyncResponse, res)
