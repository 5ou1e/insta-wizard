from __future__ import annotations

from dataclasses import dataclass

from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.web_navigator import (
    WebNavigator,
)
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.navigation.get_home_page import (
    GetInstagramHomePageResponse,
)


@dataclass(slots=True)
class GetInstagramHomePage(Command[GetInstagramHomePageResponse]):
    """Navigate to the Instagram home page"""

    pass


class GetInstagramHomePageHandler(
    CommandHandler[GetInstagramHomePage, GetInstagramHomePageResponse]
):
    def __init__(self, navigator: WebNavigator, state: WebClientState) -> None:
        self.navigator = navigator
        self.state = state

    async def __call__(self, command: GetInstagramHomePage) -> GetInstagramHomePageResponse:
        return await self.navigator.navigate(url=constants.WWW_INSTAGRAM_URL)
