from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import dumps
from insta_wizard.mobile.commands._responses.bloks.send_login_request import (
    BloksSendLoginRequestResponse,
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
class BloksSendLoginRequest(Command[BloksSendLoginRequestResponse]):
    """Авторизоваться в аккаунт с помощью логина и пароля"""

    username: str
    enc_password: str
    login_attempt_count: int = 0


class BloksSendLoginRequestHandler(
    CommandHandler[BloksSendLoginRequest, BloksSendLoginRequestResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: BloksSendLoginRequest) -> BloksSendLoginRequestResponse:
        params = {
            "client_input_params": {
                "sim_phones": [],
                "aymh_accounts": [],
                "secure_family_device_id": "",
                "has_granted_read_contacts_permissions": 0,
                "auth_secure_device_id": "",
                "has_whatsapp_installed": 0,
                "password": command.enc_password,
                "sso_token_map_json_string": "",
                "block_store_machine_id": "",
                "ig_vetted_device_nonces": "",
                "cloud_trust_token": None,
                "event_flow": "login_manual",
                "password_contains_non_ascii": "false",
                "client_known_key_hash": "",
                "encrypted_msisdn": "",
                "has_granted_read_phone_permissions": 0,
                "app_manager_id": "",
                "should_show_nested_nta_from_aymh": 1,
                "device_id": self.state.device.android_id,
                "login_attempt_count": command.login_attempt_count,
                "machine_id": self.state.local_data.mid,
                "flash_call_permission_status": {
                    "READ_PHONE_STATE": "DENIED",
                    "READ_CALL_LOG": "DENIED",
                    "ANSWER_PHONE_CALLS": "DENIED",
                },
                "accounts_list": [],
                "family_device_id": self.state.device.phone_id,
                "fb_ig_device_id": [],
                "device_emails": [],
                "try_num": 1,
                "lois_settings": {"lois_token": ""},
                "event_step": "home_page",
                "headers_infra_flow_id": "",
                "openid_tokens": {},
                "contact_point": command.username,
            },
            "server_params": {
                "should_trigger_override_login_2fa_action": 0,
                "is_vanilla_password_page_empty_password": 0,
                "is_from_logged_out": 0,
                "should_trigger_override_login_success_action": 0,
                "login_credential_type": "none",
                "server_login_source": "login",
                "waterfall_id": self.state.local_data.waterfall_id,
                "two_step_login_type": "one_step_login",
                "login_source": "Login",
                "is_platform_login": 0,
                "INTERNAL__latency_qpl_marker_id": 36707139,
                "is_from_aymh": 0,
                "offline_experiment_group": self.state.version_info.offline_experiment_group,
                "is_from_landing_page": 0,
                "password_text_input_id": "hqg4g8:68",
                "is_from_empty_password": 0,
                "is_from_msplit_fallback": 0,
                "ar_event_source": "login_home_page",
                "qe_device_id": self.state.device.device_id,
                "username_text_input_id": "hqg4g8:67",
                "layered_homepage_experiment_group": "Deploy: Not in Experiment",
                "device_id": self.state.device.android_id,
                "INTERNAL__latency_qpl_instance_id": 107234727200302.0,
                "reg_flow_source": "aymh_single_profile_native_integration_point",
                "is_caa_perf_enabled": 1,
                "credential_type": "password",
                "is_from_password_entry_page": 0,
                "caller": "gslr",
                "family_device_id": self.state.device.phone_id,
                "is_from_assistive_id": 0,
                "access_flow_version": "pre_mt_behavior",
                "is_from_logged_in_switcher": 0,
            },
        }

        bk_client_context = {
            "bloks_version": self.state.version_info.bloks_version_id,
            "styles_id": "instagram",
        }

        data = {
            "params": dumps(params),
            "bk_client_context": dumps(bk_client_context),
            "bloks_versioning_id": self.state.version_info.bloks_version_id,
        }

        res = await self.api.call_api(
            method="POST",
            uri=constants.BLOKS_SEND_LOGIN_REQUEST_URI,
            data=data,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(BloksSendLoginRequestResponse, res)
