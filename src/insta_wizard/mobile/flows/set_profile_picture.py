from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

import aiofiles

from insta_wizard.mobile.commands.account.change_profile_picture import (
    AccountChangeProfilePicture,
)
from insta_wizard.mobile.commands.rupload_igphoto import (
    RuploadIgphoto,
)
from insta_wizard.mobile.common.command import (
    Command,
    CommandBus,
    CommandHandler,
)

SetProfilePictureResult: TypeAlias = None


@dataclass(slots=True)
class SetProfilePicture(Command[SetProfilePictureResult]):
    """Установить аватар на аккаунт"""

    path: Path


class SetProfilePictureHandler(CommandHandler[SetProfilePicture, SetProfilePictureResult]):
    def __init__(
        self,
        bus: CommandBus,
    ) -> None:
        self.bus = bus

    async def __call__(
        self,
        command: SetProfilePicture,
    ) -> SetProfilePictureResult:
        async with aiofiles.open(command.path, "rb") as f:
            image_bytes = await f.read()

        upload_id = await self.bus.execute(RuploadIgphoto(image_bytes=image_bytes))
        await self.bus.execute(AccountChangeProfilePicture(upload_id=str(upload_id)))
