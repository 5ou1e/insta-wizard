from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.get_challenge_info_b_api import (
    ChallengeGetChallengeInfoBApiResponse,
)
from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.models.challenge import (
    ChallengeRequiredData,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


@dataclass(slots=True)
class ChallengeGetChallengeInfoBApi(Command[ChallengeGetChallengeInfoBApiResponse]):
    """Получить информацию о чекпоинте"""

    challenge_data: ChallengeRequiredData


class ChallengeGetChallengeInfoBApiHandler(
    CommandHandler[ChallengeGetChallengeInfoBApi, ChallengeGetChallengeInfoBApiResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: ChallengeGetChallengeInfoBApi,
    ) -> ChallengeGetChallengeInfoBApiResponse:
        challenge_data = command.challenge_data
        if not challenge_data.api_path:
            raise ValueError("Отсутствует api_path в challenge_data")

        uri = str(challenge_data.api_path).lstrip("/")

        params: dict = {
            "guid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
        }
        if challenge_data.challenge_context:
            params["challenge_context"] = challenge_data.challenge_context

        resp = await self.api.call_b_api(
            method="GET",
            uri=uri,
            params=params,
        )
        return cast(ChallengeGetChallengeInfoBApiResponse, resp)
