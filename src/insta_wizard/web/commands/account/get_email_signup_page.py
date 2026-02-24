from dataclasses import dataclass

from insta_wizard.web.commands._responses.account.get_email_signup_page import (
    GetEmailSignupPageResult,
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
class GetEmailSignupPage(Command[GetEmailSignupPageResult]):
    """Navigate to the registration page"""

    pass


class GetEmailSignupPageHandler(CommandHandler[GetEmailSignupPage, GetEmailSignupPageResult]):
    def __init__(self, navigator: WebNavigator, state: WebClientState) -> None:
        self.navigator = navigator
        self.state = state

    async def __call__(self, command: GetEmailSignupPage) -> GetEmailSignupPageResult:
        return await self.navigator.navigate(url=constants.ACCOUNTS_EMAIL_SIGNUP_URL)
