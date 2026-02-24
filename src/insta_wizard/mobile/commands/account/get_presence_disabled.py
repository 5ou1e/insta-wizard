from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import (
    dumps,
)
from insta_wizard.mobile.commands._responses.account.account_get_presence_disabled import (
    AccountGetPresenceDisabledResponse,
)
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.common.utils import (
    build_signed_body_value,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class AccountGetPresenceDisabled(Command[AccountGetPresenceDisabledResponse]):
    pass


class AccountGetPresenceDisabledHandler(
    CommandHandler[AccountGetPresenceDisabled, AccountGetPresenceDisabledResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: AccountGetPresenceDisabled
    ) -> AccountGetPresenceDisabledResponse:
        params = {"signed_body": build_signed_body_value(dumps({}))}

        resp = await self.api.call_api(
            method="GET",
            uri=constants.ACCOUNTS_GET_PRESENCE_DISABLED_URI,
            params=params,
        )
        return cast(AccountGetPresenceDisabledResponse, resp)
