from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.web.commands._responses.account.edit_web_form_data import (
    AccountsEditWebFormDataResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class AccountsEditWebFormData(Command[AccountsEditWebFormDataResult]):
    """Get account data from the profile edit page"""

    pass


class AccountsEditWebFormDataHandler(
    CommandHandler[AccountsEditWebFormData, AccountsEditWebFormDataResult]
):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(
        self,
        command: AccountsEditWebFormData,
    ) -> AccountsEditWebFormDataResult:
        resp = await self.api_requester.execute(
            method="GET",
            url=constants.ACCOUNTS_EDIT_WEB_FORM_DATA_URL,
            extra_headers={
                "Referer": "https://www.instagram.com/accounts/edit/",
            },
        )
        return cast(AccountsEditWebFormDataResult, resp)
