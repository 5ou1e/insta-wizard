from insta_wizard.common.help import _print_help
from insta_wizard.web.client import WebInstagramClient
from insta_wizard.web.models.device_info import BrowserDeviceInfo
from insta_wizard.web.models.local_data import WebClientLocalData

__all__ = [
    "WebInstagramClient",
    "BrowserDeviceInfo",
    "WebClientLocalData",
]


def print_help():
    return _print_help("insta_wizard.web")
