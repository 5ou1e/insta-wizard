import asyncio
from dataclasses import dataclass
from typing import Literal

from insta_wizard.common.entities.media import Media
from insta_wizard.common.media_utils import (
    extract_video_thumbnail,
    get_video_metadata,
    transcode_video_for_instagram,
)
from insta_wizard.mobile.commands.media.configure_to_story import MediaConfigureToStory
from insta_wizard.mobile.commands.media.upload_finish import MediaUploadFinish
from insta_wizard.mobile.commands.rupload_igphoto import RuploadIgphoto
from insta_wizard.mobile.commands.rupload_igvideo import RuploadIgvideo
from insta_wizard.mobile.common.command import Command, CommandBus, CommandHandler
from insta_wizard.mobile.exceptions import TranscodeNotFinishedYetError


@dataclass(slots=True, kw_only=True)
class PublishStoryVideo(Command[Media]):
    """Upload a video and publish it to stories.

    Args:
        video_bytes: Raw video file bytes (MP4, MOV, or any ffmpeg-supported format).
        thumbnail_bytes: Custom cover image as JPEG bytes. Auto-extracted from mid-frame if not provided.
        transcode: Re-encode to H.264/yuv420p before uploading. Set to False if already H.264 yuv420p.
        fit_mode: How to handle aspect ratios outside Instagram limits.
            "pad" — add black bars (default). "crop" — crop to fit.
        retries: Max retry attempts if Instagram reports transcoding is not yet finished.
        retry_delay: Seconds to wait between retries.
    """

    video_bytes: bytes
    thumbnail_bytes: bytes | None = None
    transcode: bool = True
    fit_mode: Literal["pad", "crop"] = "pad"
    retries: int = 5
    retry_delay: float = 1.0


class PublishStoryVideoHandler(CommandHandler[PublishStoryVideo, Media]):
    def __init__(self, bus: CommandBus) -> None:
        self.bus = bus

    async def __call__(self, command: PublishStoryVideo) -> Media:
        video_bytes = (
            transcode_video_for_instagram(command.video_bytes, command.fit_mode)
            if command.transcode
            else command.video_bytes
        )
        width, height, duration_ms = get_video_metadata(video_bytes)
        thumbnail = command.thumbnail_bytes or extract_video_thumbnail(video_bytes)

        upload_id = await self.bus.execute(
            RuploadIgvideo(
                video_bytes=video_bytes,
                duration_ms=duration_ms,
                width=width,
                height=height,
                for_story=True,
            )
        )
        await self.bus.execute(RuploadIgphoto(image_bytes=thumbnail, upload_id=upload_id))

        retries = 0
        while True:
            try:
                await self.bus.execute(
                    MediaUploadFinish(
                        upload_id=upload_id,
                        source_type="3",
                        video=True,
                        duration_ms=duration_ms,
                    )
                )
                break
            except TranscodeNotFinishedYetError as e:
                if retries >= command.retries:
                    raise e
                retries += 1
                await asyncio.sleep(command.retry_delay)

        resp = await self.bus.execute(
            MediaConfigureToStory(
                upload_id=upload_id,
                video=True,
                duration_ms=duration_ms,
                width=width,
                height=height,
            )
        )
        m = resp["media"]
        return Media(
            pk=m["pk"],
            id=m["id"],
            code=m["code"],
            media_type=m["media_type"],
            taken_at=m["taken_at"],
            width=m["original_width"],
            height=m["original_height"],
            expiring_at=m["expiring_at"],
            viewer_count=m.get("viewer_count", 0),
        )
