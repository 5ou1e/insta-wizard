from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.account.account_username_suggestions import (
    AccountUsernameSuggestionsResponse,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.common.utils import build_signed_body
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class AccountUsernameSuggestions(Command[AccountUsernameSuggestionsResponse]):
    username: str


class AccountUsernameSuggestionsHandler(
    CommandHandler[AccountUsernameSuggestions, AccountUsernameSuggestionsResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: AccountUsernameSuggestions
    ) -> AccountUsernameSuggestionsResponse:
        data = {
            "phone_id": self.state.device.phone_id,
            "guid": self.state.device.device_id,
            "name": command.username,
            "device_id": self.state.device.android_id,
            "email": "",
            "waterfall_id": self.state.local_data.waterfall_id,
        }
        payload = build_signed_body(data)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_USERNAME_SUGGESTIONS_URI,
            data=payload,
        )
        return cast(AccountUsernameSuggestionsResponse, resp)
