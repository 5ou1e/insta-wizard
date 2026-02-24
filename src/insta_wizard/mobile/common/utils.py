import urllib

from insta_wizard.common.utils import dumps
from insta_wizard.mobile.models.android_device_info import (
    AndroidDeviceInfo,
)
from insta_wizard.mobile.models.version import InstagramAppVersionInfo


def instagram_android_user_agent_from_android_device_info(
    device: AndroidDeviceInfo,
    version_info: InstagramAppVersionInfo,
) -> str:
    return (
        f"Instagram {version_info.app_version} "
        f"Android ({device.os_api_level}/{device.os_version}; "
        f"{device.dpi}dpi; {device.resolution}; "
        f"{device.manufacturer}/{device.brand}; {device.model}; "
        f"{device.device}; {device.cpu}; {device.locale}; "
        f"{version_info.version_code})"
    )


def device_languages_from_device_locale(locale: str) -> str:
    system_locale = locale.replace("_", "-")
    keyboard_locale = "en-US"
    return dumps(
        {
            "system_languages": system_locale,
            "keyboard_language": keyboard_locale,
        }
    )


def build_signed_body(data: dict):
    """
    Returns "signed_body=SIGNATURE.test"
    """
    data_str = dumps(data)
    return f"signed_body=SIGNATURE.{urllib.parse.quote_plus(data_str)}"


def build_signed_body_value(data_json: str) -> str:
    return f"SIGNATURE.{data_json}"


def build_graphql_payload(
    friendly_name: str,
    client_doc_id: str,
    variables: dict,
    locale: str = "user",
) -> dict[str, str]:
    return {
        "method": "post",
        "pretty": "false",
        "format": "json",
        "server_timestamps": "true",
        "locale": locale,
        "purpose": "fetch",
        "fb_api_req_friendly_name": friendly_name,
        "client_doc_id": client_doc_id,
        "enable_canonical_naming": "true",
        "enable_canonical_variable_overrides": "true",
        "enable_canonical_naming_ambiguous_type_prefixing": "true",
        "variables": dumps(variables),
    }
