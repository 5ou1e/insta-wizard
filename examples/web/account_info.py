"""
Web client — fetching user information.

The web client exposes account data through the profile edit form endpoint,
which returns the full profile of the currently authenticated user.
"""

import asyncio
import json

from insta_wizard import WebInstagramClient


async def main() -> None:
    async with WebInstagramClient() as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")

        # Returns profile data for the authenticated user:
        # username, full name, biography, email, phone, gender, etc.
        info = await client.account.get_edit_form_data()
        print(json.dumps(info, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
