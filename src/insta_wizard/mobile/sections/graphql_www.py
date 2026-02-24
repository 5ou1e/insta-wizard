from __future__ import annotations

import gzip
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlencode

from insta_wizard.common.generators import uuid_v4_hex
from insta_wizard.common.transport.models import HttpRequest
from insta_wizard.common.utils import (
    display_name_for_locale,
    dumps,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.headers_factory import (
    MobileClientHeadersFactory,
)
from insta_wizard.mobile.common.requesters.requester import (
    RequestExecutor,
)
from insta_wizard.mobile.common.utils import (
    build_graphql_payload,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


class GraphqlWWW:
    def __init__(
        self,
        state: MobileClientState,
        request_executor: RequestExecutor,
        headers: MobileClientHeadersFactory,
    ):
        self.state = state
        self.request_executor = request_executor
        self.headers = headers

    async def graphql_call(
        self,
        *,
        friendly_name: str,
        client_doc_id: str,
        root_field_name: str,
        variables: Mapping[str, Any] | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ):
        url = constants.GRAPHQL_WWW_URL

        headers = self.headers.graphql_headers()
        headers.update(
            {
                "X-Client-Doc-Id": client_doc_id,
                "X-Fb-Friendly-Name": friendly_name,
                "X-Root-Field-Name": root_field_name,
                "X-Graphql-Client-Library": "pando",
            }
        )

        payload_dict = build_graphql_payload(
            friendly_name=friendly_name,
            client_doc_id=client_doc_id,
            variables=dict(variables or {}),
        )

        data = payload_dict
        if variables:
            headers["content-encoding"] = "gzip"
            encoded = urlencode(payload_dict).encode("utf-8")
            data = gzip.compress(encoded)

        if extra_headers:
            headers.update(dict(extra_headers))

        return await self.request_executor(
            HttpRequest(
                method="POST",
                url=url,
                headers=headers,
                data=data,
            )
        )

    async def FxIgLinkageCacheQuery(self):
        return await self.graphql_call(
            friendly_name="FxIgLinkageCacheQuery",
            client_doc_id="11674382495679744485820947859",
            root_field_name="xe_client_cache_accounts",
            variables={
                "caller_name": "fx_product_foundation_client_FXOnline_client_cache",
            },
        )

    async def FxIgXavSwitcherBadgingDataQuery(self):
        return await self.graphql_call(
            friendly_name="FxIgXavSwitcherBadgingDataQuery",
            client_doc_id="83794259218148585413504099631",
            root_field_name="switcher_accounts_data",
            variables={
                "should_force_badge_refresh": False,
                "family_device_id": "",
                "caller_name": "fx_company_identity_switcher",
            },
        )

    async def FxIgFetaInfoQuery(self):
        return await self.graphql_call(
            friendly_name="FxIgFetaInfoQuery",
            client_doc_id="11424838746690953787234584958",
            root_field_name="fx_pf_feta_info",
            variables={},
        )

    async def IGSharedAccountsQuery(self):
        return await self.graphql_call(
            friendly_name="IGSharedAccountsQuery",
            client_doc_id="18737527476309823412641144201",
            root_field_name="me",
            variables={},
        )

    async def BasicAdsOptInQuery(self):
        return await self.graphql_call(
            friendly_name="BasicAdsOptInQuery",
            client_doc_id="33052919472135518510885263591",
            root_field_name="xfb_user_basic_ads_preferences",
            variables={},
        )

    async def AFSOptInQuery(self):
        return await self.graphql_call(
            friendly_name="AFSOptInQuery",
            client_doc_id="35850666251457231147855668495",
            root_field_name="AFSStatusGraphQLWrapper",
            variables={},
        )

    async def IGContentFilterDictionaryLookupQuery(self):
        return await self.graphql_call(
            friendly_name="IGContentFilterDictionaryLookupQuery",
            client_doc_id="20527889283312263939147305606",
            root_field_name="ig_content_filter_dictionary_lookup_query",
            variables={
                "service_ids": ["MUTED_WORDS"],
                "languages": ["nolang"],
            },
        )

    async def QuickPromotionSurfaceQueryV3(self):
        return await self.graphql_call(
            friendly_name="QuickPromotionSurfaceQueryV3",
            client_doc_id="40925026811885364213860968489",
            root_field_name="ig_quick_promotion_batch_fetch_root",
            variables={
                "trigger_context": {"context_data_tuples": []},
                "surface_triggers": [
                    {
                        "triggers": ["app_foreground", "session_start"],
                        "surface_id": "INSTAGRAM_FOR_ANDROID_LOGIN_INTERSTITIAL_QP",
                    }
                ],
                "scale": 3,
                "bloks_version": "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            },
            extra_headers={
                "x-ig-family-device-id": self.state.device.phone_id,
            },
        )

    async def IGPaginatedShareSheetQuery(self):
        return await self.graphql_call(
            friendly_name="IGPaginatedShareSheetQuery",
            client_doc_id="344505991810867181149711451826",
            root_field_name="get_paginated_ig_share_sheet_ranking_query",
            variables={
                "input": {
                    "views": ["reshare_share_sheet"],
                    "ibc_share_sheet_params": {"size": 3, "position": 5},
                    "page_max_id": None,
                    "count_per_page": 150,
                }
            },
        )

    async def GenAINuxConsentStatusQuery(self):
        return await self.graphql_call(
            friendly_name="GenAINuxConsentStatusQuery",
            client_doc_id="22964137455619044644239243163",
            root_field_name="xfb_messenger_gen_ai_nux_consent_status_query",
            variables={},
        )

    async def IGFXAccessLibrarySSOAndRegFlagQuery(self):
        return await self.graphql_call(
            friendly_name="IGFXAccessLibrarySSOAndRegFlagQuery",
            client_doc_id="2245869636858707557133739912",
            root_field_name="fx_waffle_wfs_and_nta_eligibility",
            variables={},
        )

    async def ZeroDayLanguageSignalUpload(self):
        languages = [
            {"locale": "en_us", "display_name": "English (US)"},
        ]
        if self.state.device.locale != "en_US":
            d_loc = self.state.device.locale
            languages.append(
                {"locale": d_loc.lower(), "display_name": display_name_for_locale(d_loc)}
            )

        return await self.graphql_call(
            friendly_name="ZeroDayLanguageSignalUpload",
            client_doc_id="421504111017775862006551019971",
            root_field_name="xfb_post_new_user_day_zero_language_signal",
            variables={
                "input_methods": [
                    {
                        "name": "com.samsung.android.honeyboard/.service.HoneyBoardService",
                        "languages": languages,
                    }
                ],
                "current_language": {
                    "locale": "en_us",
                    "display_name": "English (US)",
                },
            },
        )

    async def HasAvatarQuery(self):
        return await self.graphql_call(
            friendly_name="HasAvatarQuery",
            client_doc_id="176575339113814643398381488942",
            root_field_name="viewer",
            variables={},
        )

    async def IGFxLinkedAccountsQuery(self):
        return await self.graphql_call(
            friendly_name="IGFxLinkedAccountsQuery",
            client_doc_id="43230821013683556483393399494",
            root_field_name="fx_linked_accounts",
            variables={},
        )

    async def CrosspostingUnifiedConfigsQuery(self):
        return await self.graphql_call(
            friendly_name="CrosspostingUnifiedConfigsQuery",
            client_doc_id="216179630710424327622729278241",
            root_field_name="xcxp_unified_crossposting_configs_root",
            variables={
                "configs_request": {
                    "source_app": "IG",
                    "crosspost_app_surface_list": [
                        {
                            "source_surface": "STORY",
                            "destination_surface": "STORY",
                            "destination_app": "FB",
                        },
                        {
                            "source_surface": "FEED",
                            "destination_surface": "FEED",
                            "destination_app": "FB",
                        },
                        {
                            "source_surface": "REELS",
                            "destination_surface": "REELS",
                            "destination_app": "FB",
                        },
                    ],
                }
            },
        )

    async def FxIgConnectedServicesInfoQuery(self):
        return await self.graphql_call(
            friendly_name="FxIgConnectedServicesInfoQuery",
            client_doc_id="2163151994804975974238986080",
            root_field_name="fx_service_cache",
            variables={
                "service_names": ["CROSS_POSTING_SETTING"],
                "custom_partner_params": [
                    {"value": "FB", "key": "CROSSPOSTING_DESTINATION_APP"},
                    {"value": "", "key": "CROSSPOSTING_SHARE_TO_SURFACE"},
                    {
                        "value": "true",
                        "key": "OVERRIDE_USER_VALIDATION_WITH_CXP_ELIGIBILITY_RULE",
                    },
                ],
                "client_caller_name": "ig_android_service_cache_crossposting_setting",
                "caller_name": "fx_product_foundation_client_FXOnline_client_cache",
            },
        )

    async def SyncCXPNoticeStateMutation(self):
        return await self.graphql_call(
            friendly_name="SyncCXPNoticeStateMutation",
            client_doc_id="14088097634272511800572157181",
            root_field_name="xcxp_sync_notice_state",
            variables={
                "client_states": [
                    {
                        "variant": "BOTTOMSHEET_AUDIENCE_CHANGE_FEED",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_MIGRATION_FEED_WAVE2",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_MIGRATION_STORIES_WAVE2",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_REEL_CCP_MIGRATION_FEED",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_REEL_CCP_MIGRATION_STORY",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_STORY_REEL_CCP_MIGRATION_FEED",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_FEED_REEL_CCP_MIGRATION_STORY",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_UNIFIED_STORIES_FEED",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_UNLINKED_USER_FEED",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_XAR_REELS",
                        "sequence_number": 2,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "DIALOG_FEED",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "DIALOG_STORY",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "TOOLTIP_AUTOSHARE_FEED",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "TOOLTIP_CURRENTLY_SHARING_FEED",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "TOOLTIP_NUX_STORIES",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "TOOLTIP_PAGE_SHARE_FEED",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "TOOLTIP_SHORTCUT_DESTINATION_PICKER_NOT_SHARING_STORIES",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                    {
                        "variant": "TOOLTIP_SHORTCUT_DESTINATION_PICKER_STORIES",
                        "sequence_number": 0,
                        "last_impression_time": 1755922784,
                        "impression_count": 0,
                    },
                    {
                        "variant": "BOTTOMSHEET_CCP_REELS_THREADS_FIRST_TOGGLE_CLICK",
                        "sequence_number": 0,
                        "last_impression_time": 0,
                        "impression_count": 0,
                    },
                ]
            },
        )

    async def CXPFbStoriesCurrentPrivacyQuery(self):  # noqa
        return await self.graphql_call(
            friendly_name="CXPFbStoriesCurrentPrivacyQuery",
            client_doc_id="320625293115518493869044192773",
            root_field_name="xcxp_fb_stories_current_privacy",
            variables={},
        )

    async def IGBloksAppRootQuery_challenge_redirect_async(self, challenge_context: Any):
        # это можно выполнять аналогично через https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.ig.challenge.redirect.async/

        return await self.graphql_call(
            friendly_name="IGBloksAppRootQuery-com.bloks.www.ig.challenge.redirect.async",
            client_doc_id="356548512611661350451296799798",
            root_field_name="bloks_action",
            variables={
                "params": {
                    "params": dumps(
                        {
                            "get_challenge": "true",
                            "fb_family_device_id": self.state.device.phone_id,
                            "challenge_context": challenge_context,
                        }
                    ),
                    "bloks_versioning_id": self.state.version_info.bloks_version_id,
                    "infra_params": {"device_id": self.state.device.device_id},
                    "app_id": "com.bloks.www.ig.challenge.redirect.async",
                },
                "bk_context": {
                    "is_flipper_enabled": False,
                    "theme_params": [],
                    "debug_tooling_metadata_token": None,
                },
            },
            extra_headers={
                "X-Fb-Appnetsession-Sid": uuid_v4_hex(),
                "X-Graphql-Request-Purpose": "fetch",
            },
        )

    async def IGBloksAppRootQuery_scraping_warning_dismiss(
        self,
        marker_id: int,
        instance_id: int,
    ):  # noqa
        variables = {
            "params": {
                "params": dumps(
                    {
                        "params": dumps(
                            {
                                "client_input_params": {},
                                "server_params": {
                                    "INTERNAL__latency_qpl_marker_id": marker_id,
                                    "INTERNAL__latency_qpl_instance_id": instance_id,
                                },
                            }
                        )
                    }
                ),
                "bloks_versioning_id": self.state.version_info.bloks_version_id,
                "infra_params": {"device_id": self.state.device.device_id},
                "app_id": "com.bloks.www.ig.challenge.scraping_warning.dismiss",
            },
            "bk_context": {
                "is_flipper_enabled": False,
                "theme_params": [],
                "debug_tooling_metadata_token": None,
            },
        }

        return await self.graphql_call(
            friendly_name="IGBloksAppRootQuery-com.bloks.www.ig.challenge.scraping_warning.dismiss",
            client_doc_id="356548512611661350451296799798",
            root_field_name="bloks_action",
            variables=variables,
            extra_headers={
                "X-Fb-Appnetsession-Sid": uuid_v4_hex(),
                "X-Graphql-Request-Purpose": "fetch",
            },
        )
