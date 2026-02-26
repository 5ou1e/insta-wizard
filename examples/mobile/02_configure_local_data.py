"""
Mobile client — configuring local session data (MobileClientLocalData).

MobileClientLocalData holds the session tokens that the client sends with
every request: session cookie, CSRF token, user_id, and various Instagram
internal tokens. The client updates this data automatically as it runs.

Two typical starting points:

  1. Fresh session — no pre-existing tokens. You must log in before making
     authenticated requests.

  2. Restored session — tokens from a previous session. No login needed;
     the client continues as if it never stopped. This is the normal
     production pattern (see also: state_persistence.py).
"""

import asyncio

from insta_wizard import MobileClientLocalData, MobileInstagramClient


# ---------------------------------------------------------------------------
# Option 1 — fresh, empty session
# All tokens are either empty or auto-generated (pigeon_session_id, etc.).
# You must call client.login() before any authenticated operation.
# ---------------------------------------------------------------------------
fresh_local_data = MobileClientLocalData.create()


# ---------------------------------------------------------------------------
# Option 2 — restored session from previously saved tokens
# Obtained from client.get_local_data()
# or via the higher-level client.dump_state() / client.load_state() API.
# ---------------------------------------------------------------------------
restored_local_data = MobileClientLocalData.create(
    authorization_data={
        "ds_user_id": "YOUR_USER_ID",
        "sessionid":  "YOUR_SESSION_ID",
    },
    # The rest of the tokens (mid, csrftoken, rur, …) are populated
    # automatically by the client during the session. You can pass them
    # too if you saved them from a previous run.
)


async def main() -> None:
    # Using a restored session — no login call needed.
    async with MobileInstagramClient(local_data=restored_local_data) as client:
        me = await client.account.get_current_user()
        print(f"Resumed session for: {me['user']['username']}")

        # Retrieve the current state of all tokens at any point.
        data = client.get_local_data()
        print(f"CSRF token: {data.csrftoken}")
        print(f"User id:    {data.user_id}")


if __name__ == "__main__":
    asyncio.run(main())
