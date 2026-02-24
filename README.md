# insta-wizard
<small>[Русский](README.ru.md)</small>

[![PyPI](https://img.shields.io/pypi/v/insta-wizard)](https://pypi.org/project/insta-wizard/)
[![Python](https://img.shields.io/pypi/pyversions/insta-wizard)](https://pypi.org/project/insta-wizard/)
[![License](https://img.shields.io/github/license/5ou1e/insta-wizard)](LICENSE)

Async Python library for working with Instagram.

It provides two clients:
- **`MobileInstagramClient`** — works with the **private mobile API** by imitating the official Android app's API behavior
- **`WebInstagramClient`** — works with the **web API** by imitating browser behavior

Use it to log in, manage profiles, follow/unfollow users, work with Direct messages, like/comment on media, fetch user data, and more.

Includes proxy support, device/profile presets, and flexible session/cookie state management.

It offers two usage styles: high-level **Sections** (recommended) and low-level typed **Commands** for full request control.

> **Status:** Active development (API may change between versions).
> **Planned:** automated checkpoint flows, account registration, broader API coverage.

---

## Clients overview

| Client | Description |
|---|---|
| `MobileInstagramClient` | Primary client. Uses the private mobile API |
| `WebInstagramClient` | Client for working with the Instagram web API, imitating browser behavior |

The **mobile client** covers most Instagram functionality. The web client offers similar functionality but works with different Instagram API endpoints, imitating browser behavior.

## Key features

**Mobile client** — imitates the Android app API behavior, uses private mobile API:
- Login, profile management (edit bio, name, profile picture)
- Search users, get user info by ID or username
- Follow / unfollow, manage followers and following lists
- Browse timeline, stories tray, suggested reels
- Direct messages: inbox, pending, group thread management (create, approve, decline, hide, mute)
- Comments: get, add, like, unlike
- Notifications and activity inbox
- Live and Clips discovery

**Web client** — imitates browser behavior, uses web API:
- Login
- Follow / unfollow
- Like / unlike media
- Add / like / unlike comments

---

## Installation

```bash
pip install insta-wizard
```

---

## Quick start

```python
import asyncio
from insta_wizard import MobileInstagramClient

async def main():
    async with MobileInstagramClient() as client:
        await client.account.login("username", "password")
        user = await client.users.get_info("1200123809")  # numeric user ID as string
        print(user)

asyncio.run(main())
```

---

## Two API styles

### 1. Sections (primary interface)

Sections are attributes on the client. This is the recommended way to interact — they cover the most common use cases:

```python
# Account
await client.account.login("username", "password")
me = await client.account.get_current_user()

# Users
user = await client.users.get_info_by_username("someuser")
user = await client.users.get_info(user_id)
results = await client.users.search("query")

# Friendships
await client.friendships.follow(user_id)
await client.friendships.unfollow(user_id)
await client.friendships.remove_follower(user_id)
followers = await client.friendships.get_user_followers(user_id)
following = await client.friendships.get_user_following(user_id)

# Feed
timeline = await client.feed.get_timeline()
stories  = await client.feed.get_stories_tray()
reels    = await client.feed.get_suggested_reels()

# Direct
inbox   = await client.direct.get_inbox()
pending = await client.direct.get_pending()

# Media & comments
comments = await client.media.get_comments(media_id)
await client.media.add_comment(media_id, "great post!")
await client.media.like_comment(comment_id)
await client.media.unlike_comment(comment_id)
```

**All mobile client sections:**

| Section | What it covers |
|---|---|
| `account` | login, get current user, edit profile, set bio, set profile picture |
| `users` | user info by id / username, web profile, search |
| `friendships` | follow, unfollow, remove follower, followers/following lists, friendship status |
| `feed` | timeline, stories tray, suggested reels |
| `direct` | inbox, pending, presence, group thread management |
| `media` | comments (get / add / like / unlike), blocked users list |
| `notifications` | notification settings, badge count |
| `news` | activity inbox |
| `live` | good time for live |
| `clips` | discover stream |
| `challenge` | challenge info |

**Web client sections:**

| Section | What it covers |
|---|---|
| `account` | edit profile, age eligibility |
| `navigation` | load pages, get shared data |
| `friendships` | follow, unfollow |
| `comments` | add / like / unlike comment |
| `likes` | like / unlike media |
| `challenge` | challenge info |

### 2. Commands

Commands are the building blocks of the library. Each command is a typed wrapper around a single Instagram API request — in 99% of cases, one command = one API call.

Section methods are just a convenient layer on top of commands. You can also call any command directly via `client.execute()` — useful when you need full control over request parameters or access to commands not yet exposed through sections:

```python
from insta_wizard.mobile.commands.user.get_user_info_by_username import UserUsernameInfo

user = await client.execute(UserUsernameInfo(username="someuser"))
```

### Browsing available commands

```python
from insta_wizard.mobile import print_help

print_help()  # prints a table: command name, module, signature
```

For web:

```python
from insta_wizard.web import print_help

print_help()
```

---

## Common features

### Proxy

```python
from insta_wizard import MobileInstagramClient, ProxyInfo

proxy = ProxyInfo.from_string("user:pass@1.2.3.4:8080")

async with MobileInstagramClient(proxy=proxy) as client:
    ...
```

Supported formats for `from_string`:

```
1.2.3.4:8080
http://1.2.3.4:8080
user:pass@1.2.3.4:8080
http://user:pass@1.2.3.4:8080
1.2.3.4:8080:user:pass
http://1.2.3.4:8080:user:pass
```

Change proxy at runtime:

```python
await client.set_proxy(ProxyInfo.from_string("..."))
await client.set_proxy(None)  # remove proxy
```

### Auto proxy rotation on network errors

Implement `ProxyProvider` and pass it via `TransportSettings`:

```python
from insta_wizard import TransportSettings, ProxyInfo
from insta_wizard.common.interfaces import ProxyProvider

class MyProxyPool(ProxyProvider):
    async def provide_new(self) -> ProxyInfo | None:
        return ProxyInfo.from_string(fetch_next_from_pool())

settings = TransportSettings(
    max_retries_on_network_errors=3,
    delay_before_retries_on_network_errors=1.0,
    change_proxy_after_all_failed_attempts=True,
    proxy_provider=MyProxyPool(),
)

async with MobileInstagramClient(transport_settings=settings) as client:
    ...
```

When all retry attempts are exhausted, the client calls `proxy_provider.provide_new()` and retries with the new proxy.

### Session state: dump & load

Persist session between runs — no need to re-login every time:

```python
import json
from insta_wizard import MobileInstagramClient

# Save after login
async with MobileInstagramClient() as client:
    await client.account.login("username", "password")

    state = client.dump_state()
    with open("session.json", "w") as f:
        json.dump(state, f)

# Restore on next run
async with MobileInstagramClient() as client:
    with open("session.json") as f:
        client.load_state(json.load(f))

    me = await client.account.get_current_user()  # already authenticated
```

State is a plain Python dictionary — you can work with it directly:

```python
state = client.dump_state()  # returns dict
client.load_state(state)     # accepts dict
```

> `dump_state` / `load_state` do not include proxy or transport settings — pass those in the constructor as usual.

### TransportSettings

```python
from insta_wizard import TransportSettings

settings = TransportSettings(
    max_network_wait_time=30.0,               # request timeout in seconds
    max_retries_on_network_errors=3,
    delay_before_retries_on_network_errors=1.0,
)

async with MobileInstagramClient(transport_settings=settings) as client:
    ...
```

---

## Mobile client

### Device presets

```python
from insta_wizard import AndroidDeviceInfo, MobileInstagramClient
from insta_wizard.mobile.models.android_device_info import AndroidPreset

# from a preset
device = AndroidDeviceInfo.from_preset(AndroidPreset.SAMSUNG_A16)

# with overrides
device = AndroidDeviceInfo.from_preset(AndroidPreset.PIXEL_8, locale="ru_RU", timezone="Europe/Moscow")

# random preset
device = AndroidDeviceInfo.random()

async with MobileInstagramClient(device=device) as client:
    ...
```

Available presets: `SAMSUNG_A16`, `SAMSUNG_S23`, `SAMSUNG_A54`, `PIXEL_8`, `REDMI_NOTE_13_PRO`.

### Local data

`MobileClientLocalData` holds cookies, auth tokens, and device IDs generated during login:

```python
from insta_wizard import MobileInstagramClient, MobileClientLocalData

local_data = MobileClientLocalData.create()  # fresh, empty
client = MobileInstagramClient(local_data=local_data)

# read it back later
local_data = client.get_local_data()
```


## Web client

Works with the Instagram web API by imitating browser behavior. Offers similar functionality to the mobile client but uses different API endpoints.

### Device presets

```python
from insta_wizard import BrowserDeviceInfo, WebInstagramClient
from insta_wizard.web.models.device_info import BrowserPreset

device = BrowserDeviceInfo.from_preset(BrowserPreset.CHROME_143_WIN11)
device = BrowserDeviceInfo.from_preset(BrowserPreset.CHROME_143_MACOS, locale="ru_RU")
device = BrowserDeviceInfo.random()

async with WebInstagramClient(device=device) as client:
    ...
```

Available presets: `CHROME_143_WIN11`, `CHROME_143_MACOS`.

### Login

```python
import asyncio
from insta_wizard import WebInstagramClient
from insta_wizard.web.flows.login import Login
from insta_wizard.web.exceptions import CheckpointRequiredError

async def main():
    async with WebInstagramClient() as client:
        try:
            await client.execute(Login(username="...", password="..."))
        except CheckpointRequiredError:
            # Automated checkpoint passing is planned — see Roadmap
            pass

        cookies = client.get_cookies()

asyncio.run(main())
```

### Follow a user

```python
async with WebInstagramClient() as client:
    await client.execute(Login(username="...", password="..."))
    await client.friendships.follow("1200123809")  # numeric user ID as string
```

### Cookies

```python
# inject existing cookies (e.g. from a previous session)
client.set_cookies({"sessionid": "...", "csrftoken": "...", "mid": "..."})

# read current cookies
cookies = client.get_cookies()  # dict
```

---

## Exceptions

Key exceptions to handle:

**Base (`insta_wizard`):**

| Exception | Description |
|---|---|
| `InstaWizardError` | Base class for all library errors |

**Mobile (`insta_wizard.mobile.exceptions`):**

| Exception | When |
|---|---|
| `ChallengeRequiredError` | Instagram requires a challenge (captcha / 2FA) |
| `LoginError` | Authorization failed |
| `LoginBadPasswordError` | Wrong password |
| `TooManyRequestsError` | Rate limited (HTTP 429) |
| `FeedbackRequiredError` | Action blocked by Instagram |
| `UnauthorizedError` | Session invalid or expired |
| `NetworkError` | Network connectivity issue |
| `NotFoundError` | Resource not found |

**Web (`insta_wizard.web.exceptions`):**

| Exception | When |
|---|---|
| `CheckpointRequiredError` | Checkpoint on login |
| `LoginError` | Authorization failed |
| `LoginBadPasswordError` | Wrong password |
| `TooManyRequestsError` | Rate limited (HTTP 429) |
| `NetworkError` | Network connectivity issue |
| `StateParametersMissingError` | State not initialized (call `initialize_state()` first) |

**Transport (`insta_wizard.common.transport.exceptions`):**

| Exception | When |
|---|---|
| `TransportTimeoutError` | Request timed out |
| `TransportNetworkError` | Low-level network error |

---


## Roadmap

Planned features and improvements:

- [ ] Automated checkpoint passing
- [ ] Account registration
- [ ] More Instagram API methods
- [ ] httpcloak transport support (TLS fingerprint spoofing for stronger browser emulation)

---

## Disclaimer

This project is a developer tool for building personal integrations and exploring the Instagram API. It is **not** designed or intended for automation, mass botting, spamming, or any activity that violates [Instagram's Terms of Service](https://help.instagram.com/581066165581870). We are not affiliated with Meta or Instagram. Use only with accounts and data you have the right to access. Comply with all applicable laws and platform rules.

## License

MIT — see [LICENSE](LICENSE)
