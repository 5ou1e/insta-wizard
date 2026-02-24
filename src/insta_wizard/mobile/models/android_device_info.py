import random
import secrets
import uuid
from dataclasses import asdict, dataclass, replace
from enum import StrEnum
from typing import Literal

from mashumaro import DataClassDictMixin

from insta_wizard.common.generators import generate_android_id_from_guid

ConnectionType = Literal["WIFI"]  # , "MOBILE(LTE)"


@dataclass(kw_only=True, slots=True)
class AndroidDeviceInfo(DataClassDictMixin):
    manufacturer: str
    brand: str
    model: str
    device: str
    cpu: str
    dpi: str
    resolution: str
    os_version: str
    os_api_level: str
    locale: str
    timezone: str
    connection_type: ConnectionType
    battery_level: int
    is_charging: bool

    android_id: str  # android-1923fjnma8123; since Android 8.0 each app has its own
    device_id: str  # UUID v4; reset on app reinstall
    phone_id: str  # UUID v4; device ID within the Meta app family (Instagram, Facebook, WhatsApp)
    adid: str  # Google Advertising ID

    @staticmethod
    def _validate_required(**fields: object) -> None:
        missing = [
            k for k, v in fields.items() if v is None or (isinstance(v, str) and not v.strip())
        ]
        if missing:
            raise ValueError(
                f"AndroidDeviceInfo: missing or invalid values: {', '.join(missing)}"
            )

    @classmethod
    def create(
        cls,
        manufacturer: str,
        brand: str,
        model: str,
        device: str,
        cpu: str,
        dpi: str,
        resolution: str,
        os_version: str,
        os_api_level: str,
        locale: str,
        timezone: str,
        connection_type: ConnectionType,
        battery_level: int = 80,
        is_charging: bool = False,
        android_id: str | None = None,
        device_id: str | None = None,
        phone_id: str | None = None,
        adid: str | None = None,
    ) -> "AndroidDeviceInfo":

        cls._validate_required(
            manufacturer=manufacturer,
            brand=brand,
            model=model,
            device=device,
            cpu=cpu,
            dpi=dpi,
            resolution=resolution,
            os_version=os_version,
            os_api_level=os_api_level,
            locale=locale,
            timezone=timezone,
            connection_type=connection_type,
        )

        device_id = (device_id.strip() if isinstance(device_id, str) else None) or str(uuid.uuid4())
        android_id = (
            android_id.strip() if isinstance(android_id, str) else None
        ) or generate_android_id_from_guid(device_id)
        phone_id = (phone_id.strip() if isinstance(phone_id, str) else None) or str(uuid.uuid4())
        adid = (adid.strip() if isinstance(adid, str) else None) or str(uuid.uuid4())

        return cls(
            manufacturer=manufacturer,
            brand=brand,
            model=model,
            device=device,
            cpu=cpu,
            dpi=dpi,
            resolution=resolution,
            os_version=os_version,
            os_api_level=os_api_level,
            locale=locale,
            timezone=timezone,
            connection_type=connection_type,
            battery_level=battery_level,
            is_charging=is_charging,
            android_id=android_id,
            device_id=device_id,
            phone_id=phone_id,
            adid=adid,
        )

    def with_(self, **overrides) -> "AndroidDeviceInfo":
        """Returns a copy with overridden fields. Analogous to BrowserDeviceInfo.with_()."""
        return replace(self, **overrides)

    @classmethod
    def from_preset(cls, preset: "AndroidPreset", **overrides) -> "AndroidDeviceInfo":
        """Create a device from a preset. Example: AndroidDeviceInfo.from_preset(AndroidPreset.PIXEL_8, locale='ru_RU')"""
        return AndroidPreset.create(preset, **overrides)

    @classmethod
    def random(cls, **kwargs) -> "AndroidDeviceInfo":
        """Random device from all available presets."""
        return AndroidPreset.random(**kwargs)


@dataclass(frozen=True, slots=True)
class _AndroidHardwareProfile:
    manufacturer: str
    brand: str
    model: str
    device: str  # device codename
    cpu: str
    dpi: str
    resolution: str
    os_version: str
    os_api_level: str


class AndroidPreset(StrEnum):
    """
    Usage::
        device = AndroidPreset.create(AndroidPreset.SAMSUNG_S23, timezone="Europe/Berlin")
        device = AndroidPreset.random()
    """

    SAMSUNG_A16 = "SAMSUNG_A16"
    SAMSUNG_S23 = "SAMSUNG_S23"
    SAMSUNG_A54 = "SAMSUNG_A54"
    PIXEL_8 = "PIXEL_8"
    REDMI_NOTE_13_PRO = "REDMI_NOTE_13_PRO"

    @classmethod
    def create(
        cls,
        preset: "AndroidPreset",
        locale: str = "en_US",
        timezone: str = "Europe/London",
        connection_type: ConnectionType = "WIFI",
        battery_level: int | None = None,
        is_charging: bool | None = None,
        **overrides,
    ) -> AndroidDeviceInfo:
        hw = _HARDWARE_PROFILES[preset]
        return AndroidDeviceInfo.create(
            **asdict(hw),
            locale=locale,
            timezone=timezone,
            connection_type=connection_type,
            battery_level=battery_level if battery_level is not None else random.randint(15, 95),
            is_charging=is_charging if is_charging is not None else random.choice([True, False]),
            **overrides,
        )

    @classmethod
    def random(
        cls,
        locale: str = "en_US",
        timezone: str = "Europe/London",
        **overrides,
    ) -> AndroidDeviceInfo:
        preset = secrets.choice(list(_HARDWARE_PROFILES))
        return cls.create(preset, locale=locale, timezone=timezone, **overrides)


_HARDWARE_PROFILES: dict[AndroidPreset, _AndroidHardwareProfile] = {
    AndroidPreset.SAMSUNG_A16: _AndroidHardwareProfile(
        manufacturer="samsung",
        brand="samsung",
        model="SM-A165F",
        device="a16",
        cpu="mt6789",
        dpi="450",
        resolution="1080x2340",
        os_version="15",
        os_api_level="35",
    ),
    AndroidPreset.SAMSUNG_S23: _AndroidHardwareProfile(
        manufacturer="samsung",
        brand="samsung",
        model="SM-S911B",
        device="dm1q",
        cpu="qcom",
        dpi="480",
        resolution="1080x2340",
        os_version="15",
        os_api_level="35",
    ),
    AndroidPreset.SAMSUNG_A54: _AndroidHardwareProfile(
        manufacturer="samsung",
        brand="samsung",
        model="SM-A546B",
        device="a54x",
        cpu="s5e8835",
        dpi="420",
        resolution="1080x2134",
        os_version="14",
        os_api_level="34",
    ),
    AndroidPreset.PIXEL_8: _AndroidHardwareProfile(
        manufacturer="Google",
        brand="google",
        model="Pixel 8",
        device="shiba",
        cpu="shiba",
        dpi="420",
        resolution="1080x2142",
        os_version="14",
        os_api_level="34",
    ),
    AndroidPreset.REDMI_NOTE_13_PRO: _AndroidHardwareProfile(
        manufacturer="Xiaomi",
        brand="Redmi",
        model="2312DRA50G",
        device="garnet",
        cpu="qcom",
        dpi="480",
        resolution="1220x2466",
        os_version="14",
        os_api_level="34",
    ),
}
