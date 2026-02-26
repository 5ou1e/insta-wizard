"""
Mobile client — saving and restoring client state.

Why this matters:
  When you log in, Instagram sets session cookies and returns various tokens
  that the client stores internally (session id, CSRF token, user_id, device
  binding, etc.). Without persisting this state you would need to log in on
  every run, which Instagram flags as suspicious behaviour.

  By calling dump_state() after login (or after any operation) and saving the
  result, you can call load_state() on the next run and continue the session
  seamlessly — no login required.

What dump_state() saves:
  - version     — Instagram app version used
  - device      — the full Android device fingerprint
  - local_data  — all session tokens (sessionid, csrftoken, mid, rur, …)
"""

import asyncio
import json
import os

from insta_wizard import MobileInstagramClient

STATE_FILE = "session_state.json"


async def first_run() -> None:
    """Login, do some work, then save the state for future runs."""
    async with MobileInstagramClient() as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")

        me = await client.account.get_current_user()
        print(f"Logged in as: {me['user']['username']}")

        # Persist the full state so we can resume next time without logging in.
        state = client.dump_state()
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        print(f"State saved to {STATE_FILE}")


async def subsequent_run() -> None:
    """Restore a previously saved state and continue without logging in."""
    with open(STATE_FILE) as f:
        state = json.load(f)

    async with MobileInstagramClient() as client:
        client.load_state(state)

        # The session is immediately active — no login needed.
        me = await client.account.get_current_user()
        print(f"Resumed session for: {me['user']['username']}")

        # Always save the updated state after each run so fresh tokens
        # (csrf, rur, www_claim, …) are not lost.
        updated_state = client.dump_state()
        with open(STATE_FILE, "w") as f:
            json.dump(updated_state, f, indent=2)


async def main() -> None:
    if os.path.exists(STATE_FILE):
        await subsequent_run()
    else:
        await first_run()


if __name__ == "__main__":
    asyncio.run(main())
