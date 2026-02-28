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
from insta_wizard.web.responses.navigation.get_web_mid import (
    GetWebMidResponse,
)


@dataclass(slots=True)
class GetWebMid(Command[GetWebMidResponse]):
    pass


class GetWebMidHandler(CommandHandler[GetWebMid, GetWebMidResponse]):
    def __init__(self, navigator: WebNavigator, state: WebClientState) -> None:
        self.navigator = navigator
        self.state = state

    async def __call__(self, command: GetWebMid) -> GetWebMidResponse:
        return await self.navigator.navigate(url=constants.WEB_MID_URL)
