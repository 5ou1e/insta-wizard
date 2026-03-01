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
from insta_wizard.mobile.responses.media.media_blocked import MediaBlockedResponse


@dataclass(slots=True)
class MediaBlocked(Command[MediaBlockedResponse]):
    pass


class MediaBlockedHandler(CommandHandler[MediaBlocked, MediaBlockedResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: MediaBlocked) -> MediaBlockedResponse:
        resp = await self.requester.call_api(
            method="GET",
            uri=constants.MEDIA_BLOCKED_URI,
            client_endpoint="MainFeedFragment:feed_timeline",
        )
        return cast(MediaBlockedResponse, resp)
