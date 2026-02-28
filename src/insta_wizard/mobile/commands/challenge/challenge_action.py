from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.challenge_action import (
    ChallengeActionResponse,
)
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
class ChallengeAction(Command[ChallengeActionResponse]):
    choice: str


class ChallengeActionHandler(CommandHandler[ChallengeAction, ChallengeActionResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: ChallengeAction,
    ) -> ChallengeActionResponse:
        """При успехе возвращает - {'action': 'close', 'status': 'ok'}"""
        uri = "challenge/"

        payload = {"choice": command.choice}
        data = build_signed_body(payload)

        resp = await self.api.call_b_api(
            method="POST",
            uri=uri,
            data=data,
        )
        return cast(ChallengeActionResponse, resp)
