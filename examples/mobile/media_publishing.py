"""
Mobile client — media publishing.

Demonstrates all available publish methods:
- publish_photo       — photo to the timeline feed
- publish_story_photo — photo to stories
- publish_video       — video to the timeline feed
- publish_story_video — video to stories
- publish_reel        — short-form video (Reels / Clips)
- publish_carousel    — album(carousel) with mixed photo + video items

Replace the file paths, credentials, and caption strings before running.
"""

import asyncio
from pathlib import Path

from insta_wizard import MobileClient
from insta_wizard.common.entities.media import AlbumPhotoItem, AlbumVideoItem

IMAGE_PATH = Path(r"C:\path\to\photo.jpg")
VIDEO_PATH = Path(r"C:\path\to\video.mp4")


async def main() -> None:
    image = IMAGE_PATH.read_bytes()
    video = VIDEO_PATH.read_bytes()

    async with MobileClient() as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")

        # --- Photo (timeline) ------------------------------------------------
        photo = await client.media.publish_photo(
            image=image,
            caption="My awesome photo!",
        )
        print(f"Photo published: {photo.url}")

        # --- Story photo -----------------------------------------------------
        story_photo = await client.media.publish_story_photo(image=image)
        print(f"Story photo published: {story_photo.url}")

        # --- Video (timeline) ------------------------------------------------
        # fit_mode="crop" trims sides to fit Instagram's aspect-ratio limits.
        # Use "pad" (default) to add black bars instead.
        video_post = await client.media.publish_video(
            video=video,
            caption="My awesome video!",
            fit_mode="crop",
        )
        print(f"Video published: {video_post.url}")

        # --- Story video -----------------------------------------------------
        story_video = await client.media.publish_story_video(
            video=video,
            fit_mode="crop",
        )
        print(f"Story video published: {story_video.url}")

        # --- Carousel (album with mixed photo + video) -----------------------
        # Instagram allows 2–10 items per carousel.
        carousel = await client.media.publish_carousel(
            items=[
                AlbumPhotoItem(image_bytes=image),
                AlbumVideoItem(video_bytes=video, fit_mode="crop"),
            ],
            caption="My awesome carousel!",
        )
        print(f"Carousel published: {carousel.url}")


        # --- Reel (Clips) ----------------------------------------------------
        reel = await client.media.publish_reel(
            video=video,
            caption="My awesome reel!",
            share_to_feed=True,  # also appear in the timeline feed
            fit_mode="crop",
        )
        print(f"Reel published: {reel.url}")

        # --- Interact with the published photo -------------------------------
        # Like the photo we just uploaded.
        await client.media.like(photo.pk)
        print(f"Liked photo {photo.pk}")

        # Leave a comment on the same photo.
        comment = await client.media.add_comment(
            media_id=photo.pk,
            text="Nice shot!",
        )
        print(f"Comment posted (id={comment.pk}): {comment.text}")


if __name__ == "__main__":
    asyncio.run(main())
