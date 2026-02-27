from dataclasses import dataclass
from typing import Any, TypedDict

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


class ChallengeWebActionResult(TypedDict):
    """
    Response example:
        {
            "location": "https://www.instagram.com/api/v1/web/fxcal/ig_sso_users/",
            "type": "CHALLENGE_REDIRECTION",
            "status": "ok"
        }
    """

    pass


@dataclass(slots=True)
class ChallengeWebAction(Command[ChallengeWebActionResult]):
    """Get challenge info"""

    choice: str  # 0, 1, 2 ...
    enc_new_password1: str | None = None  # for LegacyForceSetNewPasswordForm
    enc_new_password2: str | None = None  # for LegacyForceSetNewPasswordForm
    next: str | None = None  # /api/v1/web/fxcal/ig_sso_users/


class ChallengeWebActionHandler(CommandHandler[ChallengeWebAction, ChallengeWebActionResult]):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: ChallengeWebAction) -> ChallengeWebActionResult:
        self.state.csrftoken_guard()

        data = {
            "choice": command.choice,
            **(
                {"enc_new_password1": command.enc_new_password1}
                if command.enc_new_password1
                else {}
            ),
            **(
                {"enc_new_password2": command.enc_new_password2}
                if command.enc_new_password2
                else {}
            ),
            **({"next": command.next} if command.next else {}),
            "jazoest": generate_jazoest(self.state.csrftoken),
        }

        return await self.api_requester.execute(
            method="POST",
            url=constants.CHALLENGE_WEB_ACTION_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com/challenge/",
            },
        )
