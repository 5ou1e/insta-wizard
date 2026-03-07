from insta_wizard.common.help import _print_help
from insta_wizard.web.client import WebClient
from insta_wizard.web.models.device_info import BrowserDeviceInfo
from insta_wizard.web.models.local_data import WebClientLocalData
from insta_wizard.web.sync_client import SyncWebClient

__all__ = [
    "WebClient",
    "SyncWebClient",
    "BrowserDeviceInfo",
    "WebClientLocalData",
]


def print_help():
    return _print_help("insta_wizard.web")
