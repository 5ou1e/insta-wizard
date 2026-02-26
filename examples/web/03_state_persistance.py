"""
Web client — saving and restoring client state.

Why this matters:
  When you log in, Instagram sets session cookies that the client stores
  internally. Without persisting this state you would need to log in on
  every run, which Instagram flags as suspicious behaviour.

  By calling dump_state() and saving the result, you can call load_state()
  on the next run and continue the session seamlessly — no login required.

What dump_state() saves:
  - device      — the browser device fingerprint
  - local_data  — session cookies and internal tokens (sessionid, csrftoken, …)
"""

import asyncio
import json
import os

from insta_wizard import WebInstagramClient

STATE_FILE = "web_session_state.json"


async def first_run() -> None:
    async with WebInstagramClient() as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")

        state = client.dump_state()
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)


async def subsequent_run() -> None:
    with open(STATE_FILE) as f:
        state = json.load(f)

    async with WebInstagramClient() as client:
        client.load_state(state)

        # The session is immediately active — no login needed.
        await client.account.get_edit_form_data()

        # Save updated state after each run so fresh tokens are not lost.
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
