import asyncio
from dataclasses import dataclass
from typing import Literal

from insta_wizard.common.entities.media import Media
from insta_wizard.common.media_utils import (
    extract_video_thumbnail,
    get_video_metadata,
    transcode_video_for_instagram,
)
from insta_wizard.mobile.commands.media.configure_timeline import MediaConfigure
from insta_wizard.mobile.commands.media.upload_finish import MediaUploadFinish
from insta_wizard.mobile.commands.rupload_igphoto import RuploadIgphoto
from insta_wizard.mobile.commands.rupload_igvideo import RuploadIgvideo
from insta_wizard.mobile.common.command import Command, CommandBus, CommandHandler
from insta_wizard.mobile.exceptions import TranscodeNotFinishedYetError


@dataclass(slots=True, kw_only=True)
class PublishVideo(Command[Media]):
    """Upload a video and publish it to the timeline feed.

    Args:
        video_bytes: Raw video file bytes (MP4, MOV, or any ffmpeg-supported format).
        caption: Post caption text.
        thumbnail_bytes: Custom cover image as JPEG bytes. Auto-extracted from mid-frame if not provided.
        transcode: Re-encode to H.264/yuv420p before uploading. Fixes HEVC, gbrp and other
            formats Instagram cannot process. Set to False if the video is already H.264 yuv420p.
        fit_mode: How to handle aspect ratios outside Instagram limits (portrait >9:16, landscape >1.91:1).
            "pad" — add black bars to fit (default). "crop" — crop to fit.
        retries: Max retry attempts if Instagram reports transcoding is not yet finished.
        retry_delay: Seconds to wait between retries.
    """

    video_bytes: bytes
    caption: str = ""
    thumbnail_bytes: bytes | None = None
    transcode: bool = True
    fit_mode: Literal["pad", "crop"] = "pad"
    retries: int = 5
    retry_delay: float = 1.0


class PublishVideoHandler(CommandHandler[PublishVideo, Media]):
    def __init__(self, bus: CommandBus) -> None:
        self.bus = bus

    async def __call__(self, command: PublishVideo) -> Media:
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
            )
        )
        await self.bus.execute(RuploadIgphoto(image_bytes=thumbnail, upload_id=upload_id))

        retries = 0
        while True:
            try:
                await self.bus.execute(
                    MediaUploadFinish(
                        upload_id=upload_id,
                        source_type="4",
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
            MediaConfigure(
                upload_id=upload_id,
                width=width,
                height=height,
                caption=command.caption,
                video=True,
                duration_ms=duration_ms,
            )
        )
        m = resp["media"]
        return Media(
            pk=str(m["pk"]),
            id=m["id"],
            code=m["code"],
            media_type=m["media_type"],
            taken_at=m["taken_at"],
            width=m["original_width"],
            height=m["original_height"],
            caption=m["caption"]["text"] if m.get("caption") else None,
            like_count=m.get("like_count"),
            comment_count=m.get("comment_count"),
        )
