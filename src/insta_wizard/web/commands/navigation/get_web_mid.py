from dataclasses import dataclass

from insta_wizard.web.commands._responses.navigation.get_web_mid import (
    GetWebMidResult,
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
class GetWebMid(Command[GetWebMidResult]):
    pass


class GetWebMidHandler(CommandHandler[GetWebMid, GetWebMidResult]):
    def __init__(self, navigator: WebNavigator, state: WebClientState) -> None:
        self.navigator = navigator
        self.state = state

    async def __call__(self, command: GetWebMid) -> GetWebMidResult:
        return await self.navigator.navigate(url=constants.WEB_MID_URL)
