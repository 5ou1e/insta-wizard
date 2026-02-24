from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.web.commands._responses.navigation.get_shared_data import (
    GetSharedDataResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class GetSharedData(Command[GetSharedDataResult]):
    """Получить SharedData конфиги"""

    pass


class GetSharedDataHandler(CommandHandler[GetSharedData, GetSharedDataResult]):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: GetSharedData) -> GetSharedDataResult:
        resp = await self.api_requester.execute(
            method="GET",
            url=constants.SHARED_DATA_URL,
        )
        return cast(GetSharedDataResult, resp)
