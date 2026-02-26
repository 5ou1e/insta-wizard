"""
Web client — login and logout.
"""

import asyncio

from insta_wizard import WebInstagramClient


async def main() -> None:
    async with WebInstagramClient() as client:
        # After login the session cookies are stored inside the client
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        # The session is now active — you can call any authenticated method.

        # Invalidates the session on Instagram's side.
        await client.logout()


if __name__ == "__main__":
    asyncio.run(main())
