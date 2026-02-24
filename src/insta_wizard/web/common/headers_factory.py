from insta_wizard.web.common.utils import (
    accept_language_from_locale,
)
from insta_wizard.web.models.state import WebClientState


class WebClientHeadersFactory:
    def __init__(
        self,
        client_state: WebClientState,
    ):
        self.state = client_state

    def base_browser_headers(
        self,
    ) -> dict[str, str]:
        """Базовые заголовки web запросов"""

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": accept_language_from_locale(self.state.device.locale),
            "Sec-Ch-Prefers-Color-Scheme": self.state.device.sec_ch_prefers_color_scheme,
            "Sec-Ch-Ua": self.state.device.sec_ch_ua,
            "Sec-Ch-Ua-Full-Version-List": self.state.device.sec_ch_full_version_list,
            "Sec-Ch-Ua-Mobile": self.state.device.sec_ch_mobile,
            "Sec-Ch-Ua-Model": self.state.device.sec_ch_model,
            "Sec-Ch-Ua-Platform": self.state.device.sec_ch_platform,
            "Sec-Ch-Ua-Platform-Version": self.state.device.sec_ch_platform_version,
            "User-Agent": self.state.device.user_agent,
            "Priority": "u=1, i",
            # "Pragma": "no-cache",
            # "Cache-Control": "no-cache",
        }

        return headers

    def navigation_headers(self):
        headers = self.base_browser_headers()
        headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Dpr": str(self.state.device.dpr),
                "Viewport-Width": str(self.state.device.viewport_width),
                "Priority": "u=0, i",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-site",  # or 'none'
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            }
        )
        return headers

    def api_headers(self):
        headers = self.base_browser_headers()
        headers.update(
            {
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "X-Asbd-Id": self.state.asbd_id,
                "X-Ig-App-Id": self.state.app_id,
                "X-Ig-Www-Claim": self.state.local_data.www_claim or "0",
                "X-Requested-With": "XMLHttpRequest",
                "X-Web-session-Id": self.state.local_data.web_session_id,
            }
        )
        if self.state.csrftoken:
            headers["X-Csrftoken"] = self.state.csrftoken

        device_id = self.state.local_data.get_cookie("ig_did")
        if device_id:
            headers["X-Web-Device-Id"] = device_id

        return headers
