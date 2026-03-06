# InstaWizard
<small>🌐 **Languages:** English · [Русский](README.ru.md)</small>

[![PyPI](https://img.shields.io/pypi/v/insta-wizard?cacheSeconds=0)](https://pypi.org/project/insta-wizard/)
[![Python](https://img.shields.io/pypi/pyversions/insta-wizard)](https://pypi.org/project/insta-wizard/)
[![License](https://img.shields.io/github/license/5ou1e/insta-wizard)](https://github.com/5ou1e/insta-wizard/blob/main/LICENSE)

Async Python library for the Instagram private API.

Manage profiles, follow users, send Direct messages, work with media and comments — all through a clean, typed, fully async interface.

Two backend clients are included:

- **`MobileInstagramClient`** — mimics the official Android app (private mobile API, v374)
- **`WebInstagramClient`** — mimics browser behavior (Instagram web API)

---

## Highlights

### Common

- ⚡ **Fully async** — asyncio + aiohttp
- 💾 **Session persistence** — `dump_state()` / `load_state()`, no re-login on every run
- 🖥️ **Device / browser fingerprints** — built-in presets and random generation
- 🔐 **Checkpoint / challenge** detection and handling
- 🌐 **HTTP proxy support** — static or auto-rotating via a custom provider
- 📋 **Standard `logging` integration** out of the box

### Mobile client

- Login and session management
- Profile editing (bio, name, profile picture)
- User search; get info by user ID or username
- Follow / unfollow, remove follower; retrieve followers and following lists
- Direct: inbox, pending requests, send messages and reactions, group thread management
- Media: like, unlike, save; comments — get, add, like, unlike
- Media publishing: photos and videos to feed, Stories, carousels (albums), and Reels
- Checkpoint / challenge detection and passing
- Account registration via SMS / Email

### Web client

- Login and session persistence
- Follow / unfollow
- Like / unlike media
- Add / like / unlike comments
- Checkpoint / challenge detection and passing

---

## Installation

**Requires Python 3.11+**

```bash
pip install insta-wizard
```

From GitHub (latest):

```bash
pip install git+https://github.com/5ou1e/insta-wizard.git
```

---

## Quick start

**Mobile:**

```python
import asyncio
from insta_wizard import MobileInstagramClient

async def main() -> None:
    async with MobileInstagramClient() as client:
        await client.account.login("USERNAME", "PASSWORD")

        me = await client.account.get_current_user()
        print("Logged in as:", me.username)

        user = await client.users.get_info_by_username("instagram")
        await client.friendships.follow(user.pk)

asyncio.run(main())
```

**Web:**

```python
import asyncio
from insta_wizard import WebInstagramClient

async def main() -> None:
    async with WebInstagramClient() as client:
        await client.login("USERNAME", "PASSWORD")

        await client.likes.like("MEDIA_ID")
        await client.likes.unlike("MEDIA_ID")

asyncio.run(main())
```

---

## Proxy

The client supports routing traffic through a proxy. Currently only HTTP/HTTPS proxies are supported, with or without authentication.

```python
from insta_wizard import MobileInstagramClient, ProxyInfo

# Supported formats: "1.2.3.4:8080", "user:pass@1.2.3.4:8080", "1.2.3.4:8080:user:pass"
proxy = ProxyInfo.from_string("user:pass@1.2.3.4:8080")

async with MobileInstagramClient(proxy=proxy) as client:
    ...
    await client.set_proxy(ProxyInfo.from_string("..."))  # change at runtime
    await client.set_proxy(None)                          # or remove it
```

On network errors, the client can automatically retry the request and rotate to a new proxy if needed — configure this via `TransportSettings`:

**Automatic rotation** — implement `ProxyProvider` and pass it via `TransportSettings`:

```python
import random

from insta_wizard import TransportSettings, ProxyInfo
from insta_wizard.common.interfaces import ProxyProvider

class MyProxyPool(ProxyProvider):
    _proxies = [
        "194.67.201.14:8080:user1:pass1",
        "91.108.4.220:3128:user2:pass2",
        "185.199.229.156:7492:user3:pass3",
    ]

    async def provide_new(self) -> ProxyInfo | None:
        return ProxyInfo.from_string(random.choice(self._proxies))

settings = TransportSettings(
    network_error_retry_limit=3,   # retry each proxy 3 times before switching
    network_error_retry_delay=1.0, # wait 1 s between retries
    change_proxies=True,           # switch proxy after all retries are exhausted
    proxy_change_limit=5,          # switch at most 5 times, then raise NetworkError
    proxy_provider=MyProxyPool(),
)

async with MobileInstagramClient(transport_settings=settings) as client:
    ...
```
When all retry attempts are exhausted, the client calls proxy_provider.provide_new() and retries with the new proxy.

---

## Device / browser presets

You can configure device settings for the client (user-agent, fingerprint, etc.). If not set explicitly, a default preset will be selected automatically.

**Mobile (Android):**

```python
from insta_wizard import AndroidDeviceInfo, MobileInstagramClient
from insta_wizard.mobile.models.android_device_info import AndroidPreset

device = AndroidDeviceInfo.from_preset(AndroidPreset.SAMSUNG_A16)
device = AndroidDeviceInfo.from_preset(AndroidPreset.PIXEL_8, locale="en_US", timezone="America/New_York")
device = AndroidDeviceInfo.random()  # picks a random preset from real Android devices

async with MobileInstagramClient(device=device) as client:
    ...
```

Available presets: `SAMSUNG_A16`, `SAMSUNG_S23`, `SAMSUNG_A54`, `PIXEL_8`, `REDMI_NOTE_13_PRO`

**Web (browser):**

```python
from insta_wizard import BrowserDeviceInfo, WebInstagramClient
from insta_wizard.web.models.device_info import BrowserPreset

device = BrowserDeviceInfo.from_preset(BrowserPreset.CHROME_143_WIN11)
device = BrowserDeviceInfo.random()  # picks a random preset from real browser configurations

async with WebInstagramClient(device=device) as client:
    ...
```

Available presets: `CHROME_143_WIN11`, `CHROME_143_MACOS`

---

## Session state

Persist a session between runs — no need to re-login every time:

```python
import asyncio, json
from insta_wizard import MobileInstagramClient

async def main() -> None:
    async with MobileInstagramClient() as client:
        await client.account.login("USERNAME", "PASSWORD")

        with open("session.json", "w", encoding="utf-8") as f:
            json.dump(client.dump_state(), f)

asyncio.run(main())
```

Restore on the next run:

```python
import asyncio, json
from insta_wizard import MobileInstagramClient

async def main() -> None:
    async with MobileInstagramClient() as client:
        with open("session.json", encoding="utf-8") as f:
            client.load_state(json.load(f))

        me = await client.account.get_current_user()  # already authenticated

asyncio.run(main())
```

State is a plain Python dictionary. Proxy and transport settings are not included — pass those to the constructor as usual.

---

## Logging

Clients log via Python's standard `logging` module by default. To enable output:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

To use a **custom logger** or disable logging entirely:

```python
from insta_wizard import MobileInstagramClient, NoOpInstagramClientLogger

async with MobileInstagramClient(logger=NoOpInstagramClientLogger()) as client:
    ...
```

See [`examples/logging_setup.py`](examples/logging_setup.py) for a custom logger example.

---

## Commands

Commands are typed wrappers around individual Instagram API calls that return the raw response as-is. In some cases it may be useful to call them directly via `client.execute()`:

```python
from insta_wizard.mobile.commands.user.usernameinfo import UserUsernameInfo

raw = await client.execute(UserUsernameInfo(username="someuser"))
```

To browse all available commands:

```python
from insta_wizard.mobile import print_help  # or insta_wizard.web

print_help()  # prints a table: command name, module, signature
```

---

## Examples

See the [`examples/`](examples) folder for ready-to-run scripts covering device presets (mobile and web), proxy setup and rotation, session persistence, and common client flows.

---

## Roadmap

- [ ] Login checkpoint passing
- [ ] Broader API coverage
- [ ] Synchronous client wrapper

---

## Disclaimer

This library is a developer tool for building personal integrations and exploring the Instagram API. It is **not** intended for spam, automation at scale, or any activity that violates [Instagram's Terms of Service](https://help.instagram.com/581066165581870). We are not affiliated with Meta or Instagram. Use only with accounts and data you have authorization to access.

---

## License

MIT — see [LICENSE](LICENSE)
