from dataclasses import dataclass
from typing import Literal, cast

from insta_wizard.mobile.commands._responses.direct.ranked_recipients import (
    DirectV2RankedRecipientsResponse,
)
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


@dataclass(slots=True)
class DirectV2RankedRecipients(Command[DirectV2RankedRecipientsResponse]):
    mode: Literal["raven", "reshare"] = "raven"
    query = ""


class DirectV2RankedRecipientsHandler(
    CommandHandler[DirectV2RankedRecipients, DirectV2RankedRecipientsResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2RankedRecipients) -> DirectV2RankedRecipientsResponse:
        params = {
            "mode": command.mode,
            "query": command.query,
        }

        resp = await self.api.call_api(
            method="GET",
            uri=constants.DIRECT_V2_GET_RANKED_RECIPIENTS_URI,
            params=params,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(DirectV2RankedRecipientsResponse, resp)
