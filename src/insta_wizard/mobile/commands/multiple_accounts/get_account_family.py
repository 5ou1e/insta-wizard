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
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.responses.multiple_accounts.multiple_accounts_get_account_family import (
    MultipleAcountsGetAccountFamilyResponse,
)


@dataclass(slots=True)
class MultipleAcountsGetAccountFamily(Command[MultipleAcountsGetAccountFamilyResponse]):
    pass


class MultipleAcountsGetAccountFamilyHandler(
    CommandHandler[MultipleAcountsGetAccountFamily, MultipleAcountsGetAccountFamilyResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: MultipleAcountsGetAccountFamily
    ) -> MultipleAcountsGetAccountFamilyResponse:
        resp = await self.api.call_api(
            method="GET",
            uri=constants.MULTIPLE_ACCOUNTS_GET_ACCOUNT_FAMILY_URI,
            params={"request_source": "com.bloks.www.caa.login.login_homepage"},
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(MultipleAcountsGetAccountFamilyResponse, resp)
