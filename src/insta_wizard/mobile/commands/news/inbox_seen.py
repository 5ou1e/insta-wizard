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
from insta_wizard.mobile.responses.news.inbox_seen import NewsInboxSeenResponse


@dataclass(slots=True)
class NewsInboxSeen(Command[NewsInboxSeenResponse]):
    pass


class NewsInboxSeenHandler(CommandHandler[NewsInboxSeen, NewsInboxSeenResponse]):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: NewsInboxSeen) -> NewsInboxSeenResponse:
        data = {"_uuid": self.state.device.device_id}

        resp = await self.requester.call_api(
            method="POST",
            uri=constants.NEWS_INBOX_SEEN_URI,
            data=data,
            client_endpoint="NewsfeedYouComposeFragment:newsfeed_you",
        )
        return cast(NewsInboxSeenResponse, resp)
