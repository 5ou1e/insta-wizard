from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import (
    utc_offset_from_timezone,
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
from insta_wizard.mobile.responses.news.inbox import (
    NewsInboxResponse,
)


@dataclass(slots=True)
class NewsInbox(Command[NewsInboxResponse]):
    pass


class NewsInboxHandler(CommandHandler[NewsInbox, NewsInboxResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: NewsInbox) -> NewsInboxResponse:
        tz = self.state.device.timezone
        params = {
            "could_truncate_feed": "true",
            "should_skip_su": "false",
            "mark_as_seen": "false",
            "timezone_offset": utc_offset_from_timezone(tz),
            "timezone_name": tz,
        }

        resp = await self.api.call_api(
            method="GET",
            uri=constants.NEWS_INBOX_URI,
            params=params,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
            extra_headers={
                "X-Ig-304-Eligible": "true",
                "X-Ig-Prefetch-Request": "foreground",
            },
        )
        return cast(NewsInboxResponse, resp)
