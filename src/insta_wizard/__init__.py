from insta_wizard.common.entities.media import AlbumPhotoItem, AlbumVideoItem
from insta_wizard.common.interfaces import (
    CaptchaSolver,
    EmailCodeProvider,
    EmailCodeSignupProvider,
    PhoneSmsCodeProvider,
    ProxyProvider,
    ResetPasswordLinkProvider,
    SelfiePhotoProvider,
)
from insta_wizard.common.logger import (
    InstagramClientLogger,
    NoOpInstagramClientLogger,
    StdLoggingInstagramClientLogger,
)
from insta_wizard.common.models.proxy import ProxyInfo
from insta_wizard.common.transport.models import TransportResponse, TransportSettings
from insta_wizard.mobile import MobileClient, SyncMobileClient
from insta_wizard.mobile.models.android_device_info import AndroidDeviceInfo
from insta_wizard.mobile.models.local_data import MobileClientLocalData
from insta_wizard.mobile.models.version import (
    InstagramAppVersion,
    InstagramAppVersionInfo,
    InstagramAppVersionInfoRegistry,
)
from insta_wizard.web import SyncWebClient, WebClient
from insta_wizard.web.models.device_info import BrowserDeviceInfo
from insta_wizard.web.models.local_data import WebClientLocalData

__all__ = [
    # Mobile client
    "MobileClient",
    "SyncMobileClient",
    "AndroidDeviceInfo",
    "MobileClientLocalData",
    "InstagramAppVersion",
    "InstagramAppVersionInfo",
    "InstagramAppVersionInfoRegistry",
    # Web client
    "WebClient",
    "SyncWebClient",
    "BrowserDeviceInfo",
    "WebClientLocalData",
    # Loggers
    "InstagramClientLogger",
    "StdLoggingInstagramClientLogger",
    "NoOpInstagramClientLogger",
    # Http
    "TransportSettings",
    "TransportResponse",
    "ProxyInfo",
    # Providers
    "ProxyProvider",
    "PhoneSmsCodeProvider",
    "ResetPasswordLinkProvider",
    "EmailCodeProvider",
    "EmailCodeSignupProvider",
    "CaptchaSolver",
    "SelfiePhotoProvider",
    # models
    "AlbumPhotoItem",
    "AlbumVideoItem",
]
