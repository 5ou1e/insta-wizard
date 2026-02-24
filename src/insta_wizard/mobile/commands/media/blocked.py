from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.media.media_blocked import (
    MediaBlockedResponse,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class MediaBlocked(Command[MediaBlockedResponse]):
    pass


class MediaBlockedHandler(CommandHandler[MediaBlocked, MediaBlockedResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: MediaBlocked) -> MediaBlockedResponse:
        resp = await self.api.call_api(
            method="GET",
            uri=constants.MEDIA_BLOCKED_URI,
            client_endpoint="MainFeedFragment:feed_timeline",
        )
        return cast(MediaBlockedResponse, resp)
