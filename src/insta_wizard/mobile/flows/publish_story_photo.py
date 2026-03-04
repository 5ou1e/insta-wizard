from dataclasses import dataclass

from insta_wizard.common.entities.media import Media
from insta_wizard.mobile.commands.media.configure_to_story import MediaConfigureToStory
from insta_wizard.mobile.commands.rupload_igphoto import RuploadIgphoto
from insta_wizard.mobile.common.command import Command, CommandBus, CommandHandler


@dataclass(slots=True, kw_only=True)
class PublishStoryPhoto(Command[Media]):
    """Upload a photo and publish it to stories."""

    image_bytes: bytes


class PublishStoryPhotoHandler(CommandHandler[PublishStoryPhoto, Media]):
    def __init__(self, bus: CommandBus) -> None:
        self.bus = bus

    async def __call__(self, command: PublishStoryPhoto) -> Media:
        upload_id = await self.bus.execute(RuploadIgphoto(image_bytes=command.image_bytes))
        resp = await self.bus.execute(MediaConfigureToStory(upload_id=upload_id))
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
