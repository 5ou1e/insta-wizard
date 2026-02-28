from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.account.edit import (
    AccountsEditResponse,
)


@dataclass(kw_only=True, slots=True)
class AccountsEdit(Command[AccountsEditResponse]):
    """Edit account profile"""

    biography: str | None = None
    chaining_enabled: bool  # Показывать рекомендации аккаунтов в профилях
    external_url: str | None = None
    first_name: str
    username: str


class AccountsEditHandler(CommandHandler[AccountsEdit, AccountsEditResponse]):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(
        self,
        command: AccountsEdit,
    ) -> AccountsEditResponse:
        self.state.csrftoken_guard()

        data = {
            "biography": command.biography or "",
            "chaining_enabled": "on" if command.chaining_enabled else "",
            "external_url": command.external_url or "",
            "first_name": command.first_name,
            "username": command.username,
        }

        data.update({"jazoest": generate_jazoest(self.state.csrftoken)})

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.ACCOUNTS_EDIT_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com/accounts/edit/",
            },
        )
        return cast(AccountsEditResponse, resp)
