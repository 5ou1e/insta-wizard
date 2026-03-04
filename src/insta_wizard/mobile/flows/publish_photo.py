from dataclasses import dataclass

from insta_wizard.common.entities.media import Media
from insta_wizard.common.media_utils import get_image_size
from insta_wizard.mobile.commands.media.configure_timeline import MediaConfigure
from insta_wizard.mobile.commands.rupload_igphoto import RuploadIgphoto
from insta_wizard.mobile.common.command import Command, CommandBus, CommandHandler


@dataclass(slots=True, kw_only=True)
class PublishPhoto(Command[Media]):
    """Upload a photo and publish it to the timeline feed."""

    image_bytes: bytes
    caption: str = ""


class PublishPhotoHandler(CommandHandler[PublishPhoto, Media]):
    def __init__(self, bus: CommandBus) -> None:
        self.bus = bus

    async def __call__(self, command: PublishPhoto) -> Media:
        width, height = get_image_size(command.image_bytes)

        upload_id = await self.bus.execute(RuploadIgphoto(image_bytes=command.image_bytes))
        resp = await self.bus.execute(
            MediaConfigure(
                upload_id=upload_id,
                width=width,
                height=height,
                caption=command.caption,
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
            caption=m["caption"]["text"] if m.get("caption") else None,
            like_count=m.get("like_count"),
            comment_count=m.get("comment_count"),
        )
