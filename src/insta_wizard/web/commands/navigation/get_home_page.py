from __future__ import annotations

from dataclasses import dataclass

from insta_wizard.web.commands._responses.navigation.get_home_page import (
    GetInstagramHomePageResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.web_navigator import (
    WebNavigator,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class GetInstagramHomePage(Command[GetInstagramHomePageResult]):
    """Перейти на главную страницу Instargam"""

    pass


class GetInstagramHomePageHandler(CommandHandler[GetInstagramHomePage, GetInstagramHomePageResult]):
    def __init__(self, navigator: WebNavigator, state: WebClientState) -> None:
        self.navigator = navigator
        self.state = state

    async def __call__(self, command: GetInstagramHomePage) -> GetInstagramHomePageResult:
        return await self.navigator.navigate(url=constants.WWW_INSTAGRAM_URL)
