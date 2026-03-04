import asyncio
from dataclasses import dataclass

from insta_wizard.common.entities.media import AlbumPhotoItem, AlbumVideoItem, Media
from insta_wizard.common.media_utils import (
    extract_video_thumbnail,
    get_image_size,
    get_video_metadata,
    transcode_video_for_instagram,
)
from insta_wizard.mobile.commands.media.configure_sidecar import (
    MediaConfigureSidecar,
    SidecarChild,
)
from insta_wizard.mobile.commands.media.upload_finish import MediaUploadFinish
from insta_wizard.mobile.commands.rupload_igphoto import RuploadIgphoto
from insta_wizard.mobile.commands.rupload_igvideo import RuploadIgvideo
from insta_wizard.mobile.common.command import Command, CommandBus, CommandHandler
from insta_wizard.mobile.exceptions import TranscodeNotFinishedYetError


@dataclass(slots=True, kw_only=True)
class PublishAlbum(Command[Media]):
    """Upload multiple media items and publish them as a carousel (album).

    Items can be any mix of AlbumPhotoItem and AlbumVideoItem.

    Args:
        items: List of photo and/or video items. Instagram allows up to 10.
        caption: Post caption text.
        retries: Max retry attempts per video item if Instagram transcoding is not finished.
        retry_delay: Seconds to wait between retries.
    """

    items: list[AlbumPhotoItem | AlbumVideoItem]
    caption: str = ""
    retries: int = 5
    retry_delay: float = 1.0


class PublishAlbumHandler(CommandHandler[PublishAlbum, Media]):
    def __init__(self, bus: CommandBus) -> None:
        self.bus = bus

    async def __call__(self, command: PublishAlbum) -> Media:
        async def upload_one(item: AlbumPhotoItem | AlbumVideoItem) -> SidecarChild:
            if isinstance(item, AlbumVideoItem):
                return await self.upload_video(
                    item,
                    retries=command.retries,
                    retry_delay=command.retry_delay,
                )
            return await self.upload_photo(item)

        children = list(await asyncio.gather(*[upload_one(item) for item in command.items]))
        resp = await self.bus.execute(
            MediaConfigureSidecar(children=children, caption=command.caption)
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
            item_count=m.get("carousel_media_count"),
            item_pks=m.get("carousel_media_ids"),
        )

    async def upload_photo(self, item: AlbumPhotoItem) -> SidecarChild:
        width, height = get_image_size(item.image_bytes)
        upload_id = await self.bus.execute(
            RuploadIgphoto(image_bytes=item.image_bytes, to_album=True)
        )
        return SidecarChild(upload_id=upload_id, width=width, height=height)

    async def upload_video(
        self,
        item: AlbumVideoItem,
        retries: int,
        retry_delay: float,
    ) -> SidecarChild:
        video_bytes = (
            transcode_video_for_instagram(item.video_bytes, item.fit_mode)
            if item.transcode
            else item.video_bytes
        )
        width, height, duration_ms = get_video_metadata(video_bytes)
        thumbnail = item.thumbnail_bytes or extract_video_thumbnail(video_bytes)

        upload_id = await self.bus.execute(
            RuploadIgvideo(
                video_bytes=video_bytes,
                duration_ms=duration_ms,
                width=width,
                height=height,
                to_album=True,
            )
        )
        await self.bus.execute(
            RuploadIgphoto(image_bytes=thumbnail, upload_id=upload_id, to_album=True)
        )

        _retries = 0
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
                if _retries >= retries:
                    raise e
                _retries += 1
                await asyncio.sleep(retry_delay)

        return SidecarChild(
            upload_id=upload_id,
            width=width,
            height=height,
            duration_ms=duration_ms,
        )
