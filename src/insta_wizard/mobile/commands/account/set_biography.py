from dataclasses import dataclass
from typing import cast

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
from insta_wizard.mobile.responses.account.account_set_biography import (
    AccountSetBiographyResponse,
)


@dataclass(slots=True)
class AccountSetBiography(Command[AccountSetBiographyResponse]):
    """Update account biography"""

    bio_text: str


class AccountSetBiographyHandler(CommandHandler[AccountSetBiography, AccountSetBiographyResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: AccountSetBiography) -> AccountSetBiographyResponse:
        payload = build_signed_body(
            {
                "_uid": self.state.local_data.user_id,
                "device_id": self.state.device.android_id,
                "_uuid": self.state.device.device_id,
                "raw_text": command.bio_text,
            }
        )

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_SET_BIOGRAPHY_URI,
            data=payload,
            client_endpoint="EditFullNameFragment:profile_edit_full_name",
        )
        return cast(AccountSetBiographyResponse, resp)
