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
from insta_wizard.web.responses.navigation.get_email_signup_page import (
    GetEmailSignupPageResponse,
)


@dataclass(slots=True)
class GetEmailSignupPage(Command[GetEmailSignupPageResponse]):
    """Navigate to the registration page"""

    pass


class GetEmailSignupPageHandler(CommandHandler[GetEmailSignupPage, GetEmailSignupPageResponse]):
    def __init__(self, navigator: WebNavigator, state: WebClientState) -> None:
        self.navigator = navigator
        self.state = state

    async def __call__(self, command: GetEmailSignupPage) -> GetEmailSignupPageResponse:
        return await self.navigator.navigate(url=constants.ACCOUNTS_EMAIL_SIGNUP_URL)
