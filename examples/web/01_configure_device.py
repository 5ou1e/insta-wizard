"""
Web client — configuring the browser device fingerprint.

WebInstagramClient imitates a real browser. The BrowserDeviceInfo object
describes which browser, OS and viewport, locale and timezone the client presents to Instagram.

If no device is passed, the client picks one automatically.
Three ways to configure it explicitly:

  1. Random — picks a random preset.
  2. From preset — uses a specific known browser/OS profile.
  3. From preset with overrides — same as above but with custom fields.
"""

import asyncio

from insta_wizard import BrowserDeviceInfo, WebInstagramClient
from insta_wizard.web.models.device_info import BrowserPreset


# Option 1 — random preset
device_random = BrowserDeviceInfo.random(locale="en_US")

# Option 2 — specific preset
device_preset = BrowserDeviceInfo.from_preset(BrowserPreset.CHROME_143_WIN11)

# Option 3 — preset with overrides
device_custom = BrowserDeviceInfo.from_preset(
    BrowserPreset.CHROME_143_WIN11,
    locale="en_US",
    color_scheme="dark",
    viewport_width=1920,
    viewport_height=1080,
)


async def main() -> None:
    async with WebInstagramClient(device=device_custom) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        await client.account.get_edit_form_data()


if __name__ == "__main__":
    asyncio.run(main())
