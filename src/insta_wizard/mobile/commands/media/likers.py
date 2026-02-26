
from dataclasses import dataclass
from typing import cast, TypedDict

from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.models.state import (
    MobileClientState,
)

class MediaLikersResponse(TypedDict):
    pass

@dataclass(slots=True)
class MediaLikers(Command[MediaLikersResponse]):
    """ Get medias likers """
    media_id: str


class MediaLikersHandler(CommandHandler[MediaLikers, MediaLikersResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: MediaLikers) -> MediaLikersResponse:
        resp = await self.api.call_api(
            method="GET",
            uri=constants.MEDIA_LIKERS_URI.format(media_id=command.media_id),
        )
        return cast(MediaLikersResponse, resp)
