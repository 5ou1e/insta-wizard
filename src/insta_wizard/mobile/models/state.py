from dataclasses import dataclass
from typing import Literal

from insta_wizard.mobile.models.android_device_info import (
    AndroidDeviceInfo,
)
from insta_wizard.mobile.models.local_data import (
    MobileClientLocalData,
)
from insta_wizard.mobile.models.version import (
    InstagramAppVersionInfo,
)


@dataclass(kw_only=True, slots=True)
class MobileClientState:
    device: AndroidDeviceInfo
    local_data: MobileClientLocalData
    version_info: InstagramAppVersionInfo

    radio_type: Literal["wifi-none"] = "wifi-none"

    def increment_request_stats(self, response_bytes: int, response_time_ms: float):
        # Увеличивавет счетчики связанные с запросами

        self.local_data.requests_count += 1
        self.local_data.total_bytes += response_bytes
        self.local_data.total_time_ms += response_time_ms
