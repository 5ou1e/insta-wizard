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
from insta_wizard.mobile.responses.bloks.youth_regulation_delete_pregent import (
    BloksYouthRegulationDeletePregentResponse,
)


@dataclass(slots=True)
class BloksYouthRegulationDeletePregent(Command[BloksYouthRegulationDeletePregentResponse]):
    pass


class BloksYouthRegulationDeletePregentHandler(
    CommandHandler[
        BloksYouthRegulationDeletePregent,
        BloksYouthRegulationDeletePregentResponse,
    ]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: BloksYouthRegulationDeletePregent,
    ) -> BloksYouthRegulationDeletePregentResponse:
        data = {
            "params": dumps(
                {
                    "client_input_params": {"lois_settings": {"lois_token": ""}},
                    "server_params": {
                        "is_from_logged_out": 0,
                        "layered_homepage_experiment_group": None,
                        "device_id": self.state.device.android_id,
                        "waterfall_id": self.state.local_data.waterfall_id,
                        "INTERNAL__latency_qpl_instance_id": 105559132700037.0,
                        "flow_info": dumps(
                            {
                                "flow_name": "new_to_family_ig_youth_reg",
                                "flow_type": "ntf",
                            }
                        ),
                        "is_platform_login": 0,
                        "INTERNAL__latency_qpl_marker_id": self.state.version_info.qpl_marker_id,
                        "reg_info": dumps(
                            {
                                "first_name": None,
                                "last_name": None,
                                "full_name": None,
                                "contactpoint": None,
                                "ar_contactpoint": None,
                                "contactpoint_type": None,
                                "is_using_unified_cp": None,
                                "unified_cp_screen_variant": None,
                                "is_cp_auto_confirmed": False,
                                "is_cp_auto_confirmable": False,
                                "confirmation_code": None,
                                "birthday": None,
                                "birthday_derived_from_age": None,
                                "did_use_age": None,
                                "gender": None,
                                "use_custom_gender": None,
                                "custom_gender": None,
                                "encrypted_password": None,
                                "username": None,
                                "username_prefill": None,
                                "fb_conf_source": None,
                                "device_id": None,
                                "ig4a_qe_device_id": None,
                                "family_device_id": None,
                                "user_id": None,
                                "safetynet_token": None,
                                "safetynet_response": None,
                                "machine_id": None,
                                "profile_photo": None,
                                "profile_photo_id": None,
                                "profile_photo_upload_id": None,
                                "avatar": None,
                                "email_oauth_token_no_contact_perm": None,
                                "email_oauth_token": None,
                                "email_oauth_tokens": None,
                                "should_skip_two_step_conf": None,
                                "openid_tokens_for_testing": None,
                                "encrypted_msisdn": None,
                                "encrypted_msisdn_for_safetynet": None,
                                "cached_headers_safetynet_info": None,
                                "should_skip_headers_safetynet": None,
                                "headers_last_infra_flow_id": None,
                                "headers_last_infra_flow_id_safetynet": None,
                                "headers_flow_id": None,
                                "was_headers_prefill_available": None,
                                "sso_enabled": None,
                                "existing_accounts": None,
                                "used_ig_birthday": None,
                                "sync_info": None,
                                "create_new_to_app_account": None,
                                "skip_session_info": None,
                                "ck_error": None,
                                "ck_id": None,
                                "ck_nonce": None,
                                "should_save_password": None,
                                "horizon_synced_username": None,
                                "fb_access_token": None,
                                "horizon_synced_profile_pic": None,
                                "is_identity_synced": False,
                                "is_msplit_reg": None,
                                "is_spectra_reg": None,
                                "spectra_reg_token": None,
                                "spectra_reg_guardian_id": None,
                                "user_id_of_msplit_creator": None,
                                "msplit_creator_nonce": None,
                                "dma_data_combination_consent_given": None,
                                "xapp_accounts": None,
                                "fb_device_id": None,
                                "fb_machine_id": None,
                                "ig_device_id": None,
                                "ig_machine_id": None,
                                "should_skip_nta_upsell": None,
                                "big_blue_token": None,
                                "skip_sync_step_nta": None,
                                "caa_reg_flow_source": None,
                                "ig_authorization_token": None,
                                "full_sheet_flow": False,
                                "crypted_user_id": None,
                                "is_caa_perf_enabled": False,
                                "is_preform": True,
                                "ignore_suma_check": False,
                                "dismissed_login_upsell_with_cna": False,
                                "ignore_existing_login": False,
                                "ignore_existing_login_from_suma": False,
                                "ignore_existing_login_after_errors": False,
                                "suggested_first_name": None,
                                "suggested_last_name": None,
                                "suggested_full_name": None,
                                "frl_authorization_token": None,
                                "post_form_errors": None,
                                "skip_step_without_errors": False,
                                "existing_account_exact_match_checked": False,
                                "existing_account_fuzzy_match_checked": False,
                                "email_oauth_exists": False,
                                "confirmation_code_send_error": None,
                                "is_too_young": False,
                                "source_account_type": None,
                                "whatsapp_installed_on_client": False,
                                "confirmation_medium": None,
                                "source_credentials_type": None,
                                "source_cuid": None,
                                "source_account_reg_info": None,
                                "soap_creation_source": None,
                                "source_account_type_to_reg_info": None,
                                "registration_flow_id": "",
                                "should_skip_youth_tos": False,
                                "is_youth_regulation_flow_complete": False,
                                "is_on_cold_start": False,
                                "email_prefilled": False,
                                "cp_confirmed_by_auto_conf": False,
                                "auto_conf_info": None,
                                "in_sowa_experiment": False,
                                "youth_regulation_config": None,
                                "conf_allow_back_nav_after_change_cp": None,
                                "conf_bouncing_cliff_screen_type": None,
                                "conf_show_bouncing_cliff": None,
                                "eligible_to_flash_call_in_ig4a": False,
                                "flash_call_permissions_status": None,
                                "attestation_result": None,
                                "request_data_and_challenge_nonce_string": None,
                                "confirmed_cp_and_code": None,
                                "notification_callback_id": None,
                                "reg_suma_state": 0,
                                "is_msplit_neutral_choice": False,
                                "msg_previous_cp": None,
                                "ntp_import_source_info": None,
                                "youth_consent_decision_time": None,
                                "should_show_spi_before_conf": True,
                                "google_oauth_account": None,
                                "is_reg_request_from_ig_suma": False,
                                "device_emails": None,
                                "is_toa_reg": False,
                                "is_threads_public": False,
                                "spc_import_flow": False,
                                "caa_play_integrity_attestation_result": None,
                                "client_known_key_hash": None,
                                "flash_call_provider": None,
                                "spc_birthday_input": False,
                                "failed_birthday_year_count": None,
                                "user_presented_medium_source": None,
                                "user_opted_out_of_ntp": None,
                                "is_from_registration_reminder": False,
                                "show_youth_reg_in_ig_spc": False,
                                "fb_suma_combined_landing_candidate_variant": "control",
                                "fb_suma_is_high_confidence": None,
                                "screen_visited": [],
                                "fb_email_login_upsell_skip_suma_post_tos": False,
                                "fb_suma_is_from_email_login_upsell": False,
                                "fb_suma_is_from_phone_login_upsell": False,
                                "fb_suma_login_upsell_skipped_warmup": False,
                                "fb_suma_login_upsell_show_list_cell_link": False,
                                "should_prefill_cp_in_ar": None,
                                "ig_partially_created_account_user_id": None,
                                "ig_partially_created_account_nonce": None,
                                "ig_partially_created_account_nonce_expiry": None,
                                "has_seen_suma_landing_page_pre_conf": False,
                                "has_seen_suma_candidate_page_pre_conf": False,
                                "suma_on_conf_threshold": -1,
                                "is_keyboard_autofocus": None,
                                "pp_to_nux_eligible": False,
                                "should_show_error_msg": True,
                                "welcome_ar_entrypoint": "control",
                                "th_profile_photo_token": None,
                                "attempted_silent_auth_in_fb": False,
                            }
                        ),
                        "family_device_id": self.state.device.phone_id,
                        "offline_experiment_group": self.state.version_info.offline_experiment_group,
                        "access_flow_version": "F2_FLOW",
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
            uri=constants.BLOKS_YOUTH_REGULATION_DELETE_PREGENT_URI,
            data=data,
            extra_headers={
                "X-Bloks-Prism-Button-Version": "INDIGO_PRIMARY_BORDERED_SECONDARY",
            },
        )
        return cast(BloksYouthRegulationDeletePregentResponse, res)
