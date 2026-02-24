from __future__ import annotations

import secrets
from dataclasses import dataclass, replace
from enum import StrEnum
from functools import cache
from typing import Literal

from mashumaro import DataClassDictMixin

Browser = Literal["chrome", "firefox", "edge"]
OS = Literal["windows", "macos", "linux"]
ARCH = Literal["x64", "arm64"]
COLOR_SCHEME = Literal["light", "dark"]


DEFAULT_LOCALES: tuple[str, ...] = (
    "en_US",
    "en_GB",
    "ru_RU",
    "de_DE",
    "fr_FR",
    "es_ES",
    "it_IT",
    "nl_NL",
    "tr_TR",
)


@dataclass(frozen=True, slots=True)
class BrowserDeviceInfo(DataClassDictMixin):
    browser: Browser
    major_version: int
    full_version: str

    os: OS
    os_version: str
    arch: ARCH

    mobile: bool
    device_model: str

    viewport_width: int
    viewport_height: int
    dpr: float

    locale: str = "en_US"
    color_scheme: COLOR_SCHEME = "light"

    def with_(self, **overrides) -> BrowserDeviceInfo:
        return replace(self, **overrides)

    @classmethod
    def from_preset(cls, preset: BrowserPreset, **overrides) -> BrowserDeviceInfo:
        return BrowserPreset.create(preset, **overrides)

    @classmethod
    def random(cls, **kwargs) -> BrowserDeviceInfo:
        return BrowserPreset.random(**kwargs)

    @property
    def user_agent(self) -> str:
        os_str = self._ua_os_string()

        if self.browser in ("chrome", "edge"):
            # Edge отдельно можно доработать (Edg/...), если понадобится
            return (
                f"Mozilla/5.0 ({os_str}) AppleWebKit/537.36 "
                f"(KHTML, like Gecko) Chrome/{self.major_version}.0.0.0 Safari/537.36"
            )

        if self.browser == "firefox":
            return (
                f"Mozilla/5.0 ({os_str}; rv:{self.major_version}.0) "
                f"Gecko/20100101 Firefox/{self.major_version}.0"
            )

        raise ValueError("unsupported browser")

    @property
    def sec_ch_ua(self) -> str:
        if self.browser in ("chrome", "edge"):
            return (
                f'"Google Chrome";v="{self.major_version}", '
                f'"Chromium";v="{self.major_version}", '
                f'"Not A(Brand";v="24"'
            )

        if self.browser == "firefox":
            return f'"Firefox";v="{self.major_version}"'

        raise ValueError("unsupported browser")

    @property
    def sec_ch_full_version_list(self) -> str:
        if self.browser in ("chrome", "edge"):
            return (
                f'"Google Chrome";v="{self.full_version}", '
                f'"Chromium";v="{self.full_version}", '
                f'"Not A(Brand";v="24.0.0.0"'
            )

        if self.browser == "firefox":
            return f'"Firefox";v="{self.major_version}.0"'

        raise ValueError("unsupported browser")

    @property
    def sec_ch_platform(self) -> str:
        return {"windows": '"Windows"', "macos": '"macOS"', "linux": '"Linux"'}[self.os]

    @property
    def sec_ch_platform_version(self) -> str:
        return f'"{self.os_version}"'

    @property
    def sec_ch_mobile(self) -> str:
        return "?1" if self.mobile else "?0"

    @property
    def sec_ch_model(self) -> str:
        return "" if not self.mobile else f'"{self.device_model}"'

    @property
    def sec_ch_prefers_color_scheme(self) -> str:
        return self.color_scheme

    def _ua_os_string(self) -> str:
        if self.os == "windows":
            arch = "Win64; x64" if self.arch == "x64" else "Win64; ARM64"
            return f"Windows NT 10.0; {arch}"
        if self.os == "macos":
            return "Macintosh; Intel Mac OS X 10_15_7"
        if self.os == "linux":
            return "X11; Linux x86_64"
        raise ValueError("unsupported os")


class BrowserPreset(StrEnum):
    """
    usage:
       device1 = BrowserPreset.create(BrowserPreset.CHROME_143_WIN11, locale="ru_RU", color_scheme="dark")
       device2 = BrowserPreset.random(locale="ru_RU")
    """

    CHROME_143_WIN11 = "CHROME_143_WIN11"
    CHROME_143_MACOS = "CHROME_143_MACOS"

    @classmethod
    def create(cls, preset: BrowserPreset, **overrides) -> BrowserDeviceInfo:
        return replace(_base(preset), **overrides)

    @classmethod
    def random(
        cls,
        locale: str = "en_US",
        **overrides,
    ) -> BrowserDeviceInfo:
        preset = secrets.choice(list(_PRESETS))
        return cls.create(preset, locale=locale, **overrides)


@cache
def _base(preset: BrowserPreset) -> BrowserDeviceInfo:
    return _PRESETS[preset]


_PRESETS: dict[BrowserPreset, BrowserDeviceInfo] = {
    BrowserPreset.CHROME_143_WIN11: BrowserDeviceInfo(
        browser="chrome",
        major_version=143,
        full_version="143.0.7499.170",
        os="windows",
        os_version="19.0.0",
        arch="x64",
        mobile=False,
        device_model="",
        viewport_width=1253,
        viewport_height=947,
        dpr=1,
    ),
    BrowserPreset.CHROME_143_MACOS: BrowserDeviceInfo(
        browser="chrome",
        major_version=143,
        full_version="143.0.7499.170",
        os="macos",
        os_version="15.4.0",
        arch="arm64",
        mobile=False,
        device_model="",
        viewport_width=1253,
        viewport_height=947,
        dpr=1,
    ),
}
