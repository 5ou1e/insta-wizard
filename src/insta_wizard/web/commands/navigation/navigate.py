from dataclasses import dataclass

from insta_wizard.web.commands._responses.navigation.navigate import (
    NavigateResult,
)
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.web_navigator import (
    WebNavigator,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class Navigate(Command[NavigateResult]):
    url: str


class NavigateHandler(CommandHandler[Navigate, NavigateResult]):
    def __init__(self, navigator: WebNavigator, state: WebClientState) -> None:
        self.navigator = navigator
        self.state = state

    async def __call__(self, command: Navigate) -> NavigateResult:
        return await self.navigator.navigate(url=command.url)
