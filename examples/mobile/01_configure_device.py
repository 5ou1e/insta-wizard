"""
Mobile client — configuring the device fingerprint.

Instagram ties sessions to a specific device. The library needs a stable
AndroidDeviceInfo object that represents the virtual Android device making
the requests. There are three ways to create one:

  1. Random — generates all hardware parameters and IDs automatically.
  2. From preset — picks a known hardware profile; you supply persistent IDs.
  3. Fully custom — specify every field manually via AndroidDeviceInfo.create().

For production use: generate once with option 1 or 2, persist the result
(e.g., as part of dump_state()), and pass it on every subsequent run.
"""

import asyncio
import uuid

from insta_wizard import AndroidDeviceInfo, MobileInstagramClient
from insta_wizard.mobile.models.android_device_info import AndroidPreset


# ---------------------------------------------------------------------------
# Option 1 — fully random
# Generates a random hardware profile AND random persistent IDs.
# Useful for quick testing; for long-lived accounts persist this object.
# ---------------------------------------------------------------------------
device_random = AndroidDeviceInfo.random(
    locale="en_US",
    timezone="America/New_York",
)


# ---------------------------------------------------------------------------
# Option 2 — preset with overrides
# Uses a predefined hardware profile (manufacturer, model, CPU, DPI, etc.)
# but lets you supply your own stable persistent IDs.
# Use this when you want a realistic known device with a fixed identity.
# ---------------------------------------------------------------------------
device_preset = AndroidDeviceInfo.from_preset(
    AndroidPreset.SAMSUNG_A16,
    locale="en_US",
    timezone="America/New_York",
    android_id="android-a1b2c3d4e5f60001",   # stays the same per app install
    device_id=str(uuid.uuid4()),              # resets on app reinstall
    phone_id=str(uuid.uuid4()),              # shared across Meta apps
    adid=str(uuid.uuid4()),                  # Google Advertising ID
)


# ---------------------------------------------------------------------------
# Option 3 — fully custom
# Build the device from scratch when you need precise control over every
# hardware parameter, e.g., to match a specific real device.
# ---------------------------------------------------------------------------
device_custom = AndroidDeviceInfo.create(
    manufacturer="Samsung",
    brand="samsung",
    model="SM-A165F",
    device="a16",
    cpu="mt6769t",
    dpi="270dpi",
    resolution="720x1560",
    os_version="14",
    os_api_level="34",
    locale="en_US",
    timezone="America/New_York",
    connection_type="WIFI",
    battery_level=85,
    is_charging=False,
    # Omit android_id / device_id / phone_id / adid to auto-generate them.
)


async def main() -> None:
    # Pass whichever device you need via the `device` parameter.
    async with MobileInstagramClient(device=device_preset) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        me = await client.account.get_current_user()
        print(f"Using device: {client.state.device.model}")
        print(f"Logged in as: {me['user']['username']}")


if __name__ == "__main__":
    asyncio.run(main())
