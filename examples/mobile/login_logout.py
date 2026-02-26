"""
Mobile client — login and logout.

client.login() runs the full Bloks login flow under the hood.
After a successful login the session data is stored inside the client
and used automatically for all subsequent requests.

Use client.logout() to invalidate the session on Instagram's side.
"""

import asyncio

from insta_wizard import MobileInstagramClient


async def main() -> None:
    async with MobileInstagramClient() as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")

        # The session is now active — you can call any authenticated method.
        me = await client.account.get_current_user()
        print(f"Logged in as: {me['user']['username']}")

        # Invalidates the session on Instagram's side.
        await client.logout()
        print("Logged out.")


if __name__ == "__main__":
    asyncio.run(main())
