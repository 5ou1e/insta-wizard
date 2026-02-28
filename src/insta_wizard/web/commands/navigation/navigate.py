from dataclasses import dataclass

from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.web_navigator import (
    WebNavigator,
)
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.navigation.navigate import (
    NavigateResponse,
)


@dataclass(slots=True)
class Navigate(Command[NavigateResponse]):
    url: str


class NavigateHandler(CommandHandler[Navigate, NavigateResponse]):
    def __init__(self, navigator: WebNavigator, state: WebClientState) -> None:
        self.navigator = navigator
        self.state = state

    async def __call__(self, command: Navigate) -> NavigateResponse:
        return await self.navigator.navigate(url=command.url)
