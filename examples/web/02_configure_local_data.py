"""
Web client — configuring local session data (WebClientLocalData).

WebClientLocalData holds the session cookies the client sends with every
request. The client updates them automatically as it runs.

Two typical starting points:

  1. Fresh session — no pre-existing cookies. You must call client.login()
     before making authenticated requests.

  2. Restored session — cookies from a previous session. No login needed;
     pass at least `sessionid` (ds_user_id is derived from it automatically).
     This is the normal production pattern (see also: 03_configure_state.py).
"""

import asyncio

from insta_wizard import WebClientLocalData, WebInstagramClient


# Option 1 — fresh, empty session
fresh_local_data = WebClientLocalData.create()

# Option 2 — restored session from saved cookies
restored_local_data = WebClientLocalData.create(
    cookies={
        "sessionid": "YOUR_SESSION_ID",
        "csrftoken": "YOUR_CSRF_TOKEN",
        "mid":       "YOUR_MID",
    }
)


async def main() -> None:
    # Using a restored session — no login call needed.
    async with WebInstagramClient(local_data=restored_local_data) as client:
        await client.account.get_edit_form_data()

        # Inspect current cookies at any point.
        cookies = client.get_cookies()
        print(cookies.get("sessionid"))


if __name__ == "__main__":
    asyncio.run(main())
