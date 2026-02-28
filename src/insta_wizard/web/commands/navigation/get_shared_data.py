from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.navigation.get_shared_data import (
    GetSharedDataResponse,
)


@dataclass(slots=True)
class GetSharedData(Command[GetSharedDataResponse]):
    """Get SharedData configs"""

    pass


class GetSharedDataHandler(CommandHandler[GetSharedData, GetSharedDataResponse]):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: GetSharedData) -> GetSharedDataResponse:
        resp = await self.api_requester.execute(
            method="GET",
            url=constants.SHARED_DATA_URL,
        )
        return cast(GetSharedDataResponse, resp)
