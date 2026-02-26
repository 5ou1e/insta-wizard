"""
Mobile client — using commands directly via client.execute().

The sections API (client.account, client.users, etc.) is the primary interface
and covers the most common operations. For anything beyond that, you can
execute any command directly using client.execute().

This example shows the login + fetch user info flow using raw commands

Commands are imported from insta_wizard.mobile.commands (or from
insta_wizard.mobile.flows for multi-step flows like BloksLogin).
"""

import asyncio
import json

from insta_wizard import MobileInstagramClient
from insta_wizard.mobile.commands import UserInfo
from insta_wizard.mobile.flows import BloksLogin


async def main() -> None:
    async with MobileInstagramClient() as client:

        # Login via BloksLogin flow
        # This is equivalent to client.login() but executed explicitly as a
        # command, giving you direct access to the command object if needed.
        await client.execute(BloksLogin(username="YOUR_USERNAME", password="YOUR_PASSWORD"))
        user_id = client.get_local_data().user_id

        # Fetch user info
        info = await client.execute(UserInfo(user_id=user_id))
        print("\n=== User info ===")
        print(json.dumps(info, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
