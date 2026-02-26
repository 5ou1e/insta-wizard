"""
Mobile client — fetching user information.

Demonstrates:
- Getting your own account info
- Looking up a user by username
- Looking up a user by numeric user_id
- Searching users by query string
"""

import asyncio
import json

from insta_wizard import MobileInstagramClient


async def main() -> None:
    async with MobileInstagramClient() as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")

        # --- Your own profile ------------------------------------------------
        me = await client.account.get_current_user()
        print("=== Current user ===")
        print(json.dumps(me, indent=2))

        # --- Look up by username ---------------------------------------------
        user = await client.users.get_info_by_username("some_username")
        user_id = str(user["user"]["pk"])
        print(f"\n=== @some_username (id={user_id}) ===")
        print(json.dumps(user, indent=2))

        # --- Look up by numeric user_id --------------------------------------
        user_by_id = await client.users.get_info(user_id)
        print("\n=== User by id ===")
        print(json.dumps(user_by_id, indent=2))

        # --- Search ----------------------------------------------------------
        results = await client.users.search("john")
        print(f"\n=== Search 'john' — {len(results['users'])} results ===")
        for u in results["users"]:
            print(f"  @{u['username']} (id={u['pk']})")


if __name__ == "__main__":
    asyncio.run(main())
