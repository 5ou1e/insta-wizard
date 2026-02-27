from dataclasses import dataclass
from typing import Any

from insta_wizard.common.models.other import EncryptionInfo
from insta_wizard.web.exceptions import StateParametersMissingError
from insta_wizard.web.models.device_info import BrowserDeviceInfo
from insta_wizard.web.models.local_data import WebClientLocalData


@dataclass(kw_only=True, slots=True)
class WebClientState:
    app_id = "936619743392459"  # Instagram Web-APP ID
    asbd_id = "359341"  # X-Asbd-Id Header

    initial_params: Any = None

    device: BrowserDeviceInfo
    local_data: WebClientLocalData

    encryption_info: EncryptionInfo | None = None

    def csrftoken_guard(self):
        if not self.csrftoken:
            raise StateParametersMissingError(msg="Отсутствует csrftoken-cookie")

    def machine_id_guard(self):
        if not self.mid:
            raise StateParametersMissingError(msg="Отсутствует mid-cookie")

    def encryption_info_guard(self):
        if self.encryption_info is None:
            raise StateParametersMissingError(msg="Отсутствует Password encryption-info")

    @property
    def csrftoken(self) -> str | None:
        return self.local_data.get_cookie("csrftoken")

    @property
    def sessionid(self) -> str | None:
        return self.local_data.get_cookie("sessionid")

    @property
    def mid(self) -> str | None:
        return self.local_data.get_cookie("mid")
