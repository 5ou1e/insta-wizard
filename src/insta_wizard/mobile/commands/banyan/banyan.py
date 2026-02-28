from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import dumps
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
from insta_wizard.mobile.responses.banyan import BanyanBanyanResponse


@dataclass(slots=True)
class BanyanBanyan(Command[BanyanBanyanResponse]):
    pass


class BanyanBanyanHandler(CommandHandler[BanyanBanyan, BanyanBanyanResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: BanyanBanyan) -> BanyanBanyanResponse:
        params = {
            "is_private_share": "false",
            "views": dumps(
                [
                    "direct_user_search_keypressed",
                    "direct_user_search_nullstate",
                    "direct_inbox_active_now",
                    "call_recipients",
                ]
            ),
            "IBCShareSheetParams": dumps({"size": 5}),
            "is_real_time": "false",
        }

        resp = await self.api.call_api(
            method="GET",
            uri=constants.BANYAN_BANYAN_URI,
            params=params,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
            extra_headers={
                "x-ig-salt-ids": "220140399,332020310",
            },
        )
        return cast(BanyanBanyanResponse, resp)
