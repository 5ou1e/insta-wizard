from dataclasses import dataclass
from typing import Any

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.challenge.bloks_navigation import (
    BloksNavigationTakeChallengeResponse,
)


@dataclass(slots=True)
class BloksNavigationTakeChallenge(Command[BloksNavigationTakeChallengeResponse]):
    challenge_context: str
    has_follow_up_screens: str = "false"
    nest_data_manifest: str = "true"


class BloksNavigationTakeChallengeHandler(
    CommandHandler[BloksNavigationTakeChallenge, BloksNavigationTakeChallengeResponse]
):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(
        self, command: BloksNavigationTakeChallenge
    ) -> BloksNavigationTakeChallengeResponse:
        self.state.csrftoken_guard()

        data = {
            "challenge_context": command.challenge_context,
            "has_follow_up_screens": command.has_follow_up_screens,
            "nest_data_manifest": command.nest_data_manifest,
            "jazoest": generate_jazoest(self.state.csrftoken),
        }

        return await self.api_requester.execute(
            method="POST",
            url=constants.BLOKS_NAVIGATION_TAKE_CHALLENGE_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com/challenge/",
                # "X-Bloks-Version-Id": ...
            },
        )
