"""
Mobile client — follow, unfollow and friendship status.

Demonstrates:
- Following and unfollowing a user
- Removing a follower
- Getting a user's followers / following list (with pagination)
- Checking friendship status with one or multiple users
"""

import asyncio
import json

from insta_wizard import MobileInstagramClient

TARGET_USER_ID = "123456789"  # replace with a real numeric user_id


async def main() -> None:
    async with MobileInstagramClient() as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")

        # --- Follow / unfollow -----------------------------------------------
        await client.friendships.follow(TARGET_USER_ID)
        print(f"Followed {TARGET_USER_ID}")

        await client.friendships.unfollow(TARGET_USER_ID)
        print(f"Unfollowed {TARGET_USER_ID}")

        # --- Remove a follower -----------------------------------------------
        # Silently removes the user from your own followers list.
        await client.friendships.remove_follower(TARGET_USER_ID)
        print(f"Removed {TARGET_USER_ID} from followers")

        # --- Friendship status -----------------------------------------------
        status = await client.friendships.get_status_single(TARGET_USER_ID)
        print(f"\nStatus with {TARGET_USER_ID}: {status}")

        # Batch status check for multiple users at once
        statuses = await client.friendships.get_status(["111", "222", TARGET_USER_ID])
        print(f"\nBatch statuses: {json.dumps(statuses, indent=2)}")

        # --- Followers list --------------------------------------------------
        # Use max_id for pagination: pass next_max_id from the previous response.
        followers = await client.friendships.get_user_followers(TARGET_USER_ID)
        print(f"\nFollowers ({len(followers['users'])} loaded):")
        for u in followers["users"]:
            print(f"  @{u['username']}")

        # Load the next page if available
        if followers.get("next_max_id"):
            next_page = await client.friendships.get_user_followers(
                TARGET_USER_ID,
                max_id=followers["next_max_id"],
            )
            print(f"  ... {len(next_page['users'])} more on next page")

        # --- Following list --------------------------------------------------
        following = await client.friendships.get_user_following(TARGET_USER_ID)
        print(f"\nFollowing ({len(following['users'])} loaded):")
        for u in following["users"]:
            print(f"  @{u['username']}")


if __name__ == "__main__":
    asyncio.run(main())
