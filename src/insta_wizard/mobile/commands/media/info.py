from dataclasses import dataclass
from typing import TypedDict, cast

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


class MediaInfoResponse(TypedDict):
    pass


@dataclass(slots=True)
class MediaInfo(Command[MediaInfoResponse]):
    """Get media info"""

    media_id: str


class MediaInfoHandler(CommandHandler[MediaInfo, MediaInfoResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: MediaInfo) -> MediaInfoResponse:
        resp = await self.requester.call_api(
            method="GET",
            uri=constants.MEDIA_INFO_URI.format(media_id=command.media_id),
        )
        return cast(MediaInfoResponse, resp)
