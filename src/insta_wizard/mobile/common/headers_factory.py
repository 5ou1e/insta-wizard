from insta_wizard.common.generators import (
    timestamp_with_ms_str,
    utc_offset_from_timezone,
    uuid_v4_hex,
)
from insta_wizard.common.utils import (
    dumps,
    locale_code_to_bcp47,
)
from insta_wizard.mobile.common.utils import (
    device_languages_from_device_locale,
    instagram_android_user_agent_from_android_device_info,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.models.version import (
    InstagramAppVersion,
)


class MobileClientHeadersFactory:
    def __init__(
        self,
        state: MobileClientState,
    ):
        self.state = state

    def api_headers(
        self,
    ) -> dict[str, str]:
        """Базовые заголовки api запросов"""

        device = self.state.device
        version_info = self.state.version_info
        local_data = self.state.local_data

        accept_language = f"{locale_code_to_bcp47(device.locale)}, en-US"
        device_locale = f"{device.locale.replace('-', '_')}"

        bandwidth_metrics = local_data.bandwidth_metrics

        headers = {
            "Accept-Encoding": "zstd",
            "Accept-Language": accept_language,
            "X-Ig-App-Locale": device_locale,
            "X-Ig-Mapped-Locale": device_locale,
            "X-Ig-Device-Locale": device_locale,
            "X-Ig-App-Id": version_info.app_id,
            "X-Ig-Capabilities": version_info.capabilities,
            "X-Ig-Connection-Type": device.connection_type,
            "X-Fb-Client-Ip": "True",
            "X-Fb-Server-Cluster": "True",
            "X-Fb-Connection-Type": device.connection_type,
            "X-Fb-Http-Engine": "MNS/TCP",
            "X-Tigon-Is-Retry": "False",
            "X-Fb-Conn-Uuid-Client": uuid_v4_hex(),
            "X-Ig-Device-Id": device.device_id,
            "X-Pigeon-Session-Id": local_data.pigeon_session_id,
            "X-Ig-Bandwidth-Speed-Kbps": f"{bandwidth_metrics['bandwidth_speed_kbps']:.3f}",
            "X-Ig-Bandwidth-Totalbytes-B": str(bandwidth_metrics["bandwidth_totalbytes_b"]),
            "X-Ig-Bandwidth-Totaltime-Ms": str(bandwidth_metrics["bandwidth_totaltime_ms"]),
            "X-Ig-Android-Id": device.android_id,
            "X-Pigeon-Rawclienttime": timestamp_with_ms_str(),
            "X-Ig-Family-Device-Id": device.phone_id,
            "X-Ig-Device-Languages": device_languages_from_device_locale(device.locale),
            "X-Ig-Timezone-Offset": str(utc_offset_from_timezone(device.timezone)),
            "Priority": "u=3",
            "X-Fb-Rmd": "state=URL_ELIGIBLE",
            "X-Fb-Request-Analytics-Tags": dumps(
                {
                    "network_tags": {
                        "product": version_info.app_id,
                        "purpose": "fetch",
                        "surface": "undefined",
                        "request_category": "api",
                        "retry_attempt": "0",
                    }
                }
            ),
        }

        if local_data.user_id:
            headers["Ig-U-Ds-User-Id"] = local_data.user_id
        if local_data.authorization:
            headers["Authorization"] = local_data.authorization
        if local_data.rur:
            headers["Ig-U-Rur"] = local_data.rur

        if local_data.mid:
            headers["X-Mid"] = local_data.mid

        headers["Ig-Intended-User-Id"] = local_data.user_id if local_data.user_id else "0"
        headers["X-Ig-Www-Claim"] = local_data.www_claim if local_data.www_claim else "0"

        headers["User-Agent"] = instagram_android_user_agent_from_android_device_info(
            device,
            version_info,
        )

        headers.update(
            {
                "X-Bloks-Version-Id": version_info.bloks_version_id,
                "X-Bloks-Is-Layout-Rtl": "false",
                "X-Bloks-Prism-Ax-Base-Colors-Enabled": "false",
                "X-Bloks-Prism-Button-Version": "CONTROL",
                "X-Bloks-Prism-Colors-Enabled": "true",  # "false" for feed / clips
                "X-Bloks-Prism-Font-Enabled": "false",  # "false" for feed / clips
                "X-Bloks-Prism-Indigo-Link-Version": "0",  # "0" for feed / clips
            }
        )

        # V410 version-specific
        if version_info.version == InstagramAppVersion.V410:
            headers.update(
                {
                    "X-Fb-Http-Engine": "Tigon/MNS/TCP",
                    "X-Fb-Network-Properties": "Wifi;",
                    "X-Ig-Is-Foldable": "false",
                    # "x-meta-usdid": "eceba10e-4b42-404a-91ba-b837f478284e.1767158763.MEUCIGGBXqguHnGkt2887_JzMJ2onLXCJKcSIMCO3IeK6m7hAiEAm0lUbR7Tz7VLQ2pmYqxLPXFe8WZqPfniTS3OozOTTsg",
                    "X-Bloks-Prism-Extended-Palette-Rest-Of-Colors": "true",  # "false" for feed / clips
                    "X-Bloks-Prism-Extended-Palette-Gray": "false",
                    "X-Bloks-Prism-Extended-Palette-Red": "true",  # "false" for feed / clips
                    "X-Bloks-Prism-Extended-Palette-Indigo": "true",  # "false" for feed / clips
                    "X-Bloks-Prism-Extended-Palette-Polish-Enabled": "true",  # "false" for feed / clips
                }
            )

        return headers

    def graphql_headers(self) -> dict[str, str]:
        """Базовые заголовки graqphql запросов"""

        local_data = self.state.local_data
        device = self.state.device
        version_info = self.state.version_info

        headers = {
            "Accept-Encoding": "zstd",
            "Accept-Language": f"{locale_code_to_bcp47(device.locale)}, en-US",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Fb-Client-Ip": "True",
            "X-Fb-Request-Analytics-Tags": '{"network_tags":{"product":"567067343352427","purpose":"none","request_category":"graphql","retry_attempt":"0"}}',
            "X-Fb-Server-Cluster": "True",
            "X-Ig-App-Id": version_info.app_id,
            "X-Ig-Capabilities": version_info.capabilities,
            "X-Ig-Android-Id": device.android_id,
            "X-Ig-Device-Id": device.device_id,
            "X-Ig-Validate-Null-In-Legacy-Dict": "true",
            "X-Fb-Http-Engine": "MNS/TCP",
            "X-Tigon-Is-Retry": "False",
            "X-Fb-Conn-Uuid-Client": uuid_v4_hex(),
            "X-Fb-Rmd": "state=URL_ELIGIBLE",
            "Priority": "u=3, i",
        }

        if local_data.user_id:
            headers["Ig-U-Ds-User-Id"] = local_data.user_id
        if local_data.authorization:
            headers["Authorization"] = local_data.authorization
        if local_data.rur:
            headers["Ig-U-Rur"] = local_data.rur

        if local_data.mid:
            headers["X-Mid"] = local_data.mid

        headers["Ig-Intended-User-Id"] = local_data.user_id if local_data.user_id else "0"

        headers["User-Agent"] = instagram_android_user_agent_from_android_device_info(
            device,
            version_info,
        )

        # v410 version-specific
        if version_info.version == InstagramAppVersion.V410:
            headers.update(
                {
                    "X-Fb-Http-Engine": "Tigon/MNS/TCP",
                    "X-Bloks-Version-Id": version_info.bloks_version_id,
                    "X-Ig-Is-Foldable": "false",
                    "X-Ig-Timezone-Offset": str(utc_offset_from_timezone(device.timezone)),
                    # "x-meta-usdid": "eceba10e-4b42-404a-91ba-b837f478284e.1767158763.MEUCIGGBXqguHnGkt2887_JzMJ2onLXCJKcSIMCO3IeK6m7hAiEAm0lUbR7Tz7VLQ2pmYqxLPXFe8WZqPfniTS3OozOTTsg",
                }
            )

        return headers
