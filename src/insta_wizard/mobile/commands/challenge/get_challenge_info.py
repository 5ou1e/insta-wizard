from dataclasses import dataclass
from typing import cast

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
from insta_wizard.mobile.responses.challenge_info import ChallengeGetChallengeInfoResponse


@dataclass(slots=True)
class ChallengeGetChallengeInfo(Command[ChallengeGetChallengeInfoResponse]):
    """Get challenge info"""

    api_path: str
    challenge_context: str | None = None


class ChallengeGetChallengeInfoHandler(
    CommandHandler[ChallengeGetChallengeInfo, ChallengeGetChallengeInfoResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: ChallengeGetChallengeInfo,
    ) -> ChallengeGetChallengeInfoResponse:
        params: dict = {
            "guid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
        }
        if command.challenge_context:
            params["challenge_context"] = command.challenge_context

        resp = await self.api.call_b_api(
            method="GET",
            uri=str(command.api_path).lstrip("/"),
            params=params,
        )
        return cast(ChallengeGetChallengeInfoResponse, resp)
