from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.commands._responses.account.check_age_eligibility import (
    CheckAgeEligibilityResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class CheckAgeEligibility(Command[CheckAgeEligibilityResult]):
    """Проверить, возможна ли регистрация с введенной датой рождения"""

    day: int
    month: int
    year: int


class CheckAgeEligibilityHandler(CommandHandler[CheckAgeEligibility, CheckAgeEligibilityResult]):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: CheckAgeEligibility) -> CheckAgeEligibilityResult:
        """
        Response example:
        {
            "eligible_to_register": true,
            "parental_consent_required": false,
            "is_supervised_user": false,
            "status": "ok"
        }
        """

        self.state.csrftoken_guard()
        self.state.machine_id_guard()

        jazoest = generate_jazoest(self.state.csrftoken)

        data = {
            "day": command.day,
            "month": command.month,
            "year": command.year,
            "jazoest": jazoest,
        }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.WEB_CONSENT_CHECK_AGE_ELIGIBILITY,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com/accounts/emailsignup/",
            },
        )
        return cast(CheckAgeEligibilityResult, resp)
