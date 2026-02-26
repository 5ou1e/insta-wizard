"""
Web client — follow and unfollow.
"""

import asyncio

from insta_wizard import WebInstagramClient


async def main() -> None:
    user_id = "123456789" # replace with a real numeric user_id

    async with WebInstagramClient() as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        # Follow user
        await client.friendships.follow(user_id=user_id)
        # And then unfollow
        await client.friendships.unfollow(user_id=user_id)


if __name__ == "__main__":
    asyncio.run(main())
