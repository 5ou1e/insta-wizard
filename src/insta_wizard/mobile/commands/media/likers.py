from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.responses.media.likers import MediaLikersResponse


@dataclass(slots=True)
class MediaLikers(Command[MediaLikersResponse]):
    """Get medias likers"""

    media_id: str


class MediaLikersHandler(CommandHandler[MediaLikers, MediaLikersResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: MediaLikers) -> MediaLikersResponse:
        resp = await self.requester.call_api(
            method="GET",
            uri=constants.MEDIA_LIKERS_URI.format(media_id=command.media_id),
        )
        return cast(MediaLikersResponse, resp)
