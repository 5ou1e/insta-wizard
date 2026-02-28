from dataclasses import dataclass
from typing import cast


from insta_wizard.mobile.commands._responses.news.inbox_seen import NewsInboxSeenResponse

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
class NewsInboxSeen(Command[NewsInboxSeenResponse]):
    pass


class NewsInboxSeenHandler(CommandHandler[NewsInboxSeen, NewsInboxSeenResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: NewsInboxSeen) -> NewsInboxSeenResponse:
        data = {'_uuid': self.state.device.device_id}

        resp = await self.api.call_api(
            method="POST",
            uri=constants.NEWS_INBOX_SEEN_URI,
            data=data,
            client_endpoint="NewsfeedYouComposeFragment:newsfeed_you",
        )
        return cast(NewsInboxSeenResponse, resp)
