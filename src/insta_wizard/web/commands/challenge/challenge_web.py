from dataclasses import dataclass
from typing import Any

from insta_wizard.web.commands._responses.challenge.challenge_web import (
    ChallengeWebResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class ChallengeWeb(Command[ChallengeWebResult]):
    """Get challenge info"""

    next: str | None = None  # /api/v1/web/fxcal/ig_sso_users/


class ChallengeWebHandler(CommandHandler[ChallengeWeb, ChallengeWebResult]):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(self, command: ChallengeWeb) -> ChallengeWebResult:
        """
        Response example:
            "challengeType": "ScrapingWarningForm",
            "errors": [],
            "experiments": {},
            "extraData": null,
            "fields": {},
            "navigation": {
                "forward": "/api/v1/challenge/web/action/",
                "replay": "/challenge/replay/"
             },
            "privacyPolicyUrl": "/about/legal/privacy/",
            "type": "CHALLENGE",
            "challenge_context": "AaXKJs7-c5TZc10mjCw5TAooinEhsu9RpGyAr0jxDfe9xwUmGIDC7mWXhzZ4DLkN2Vjs2UWM2zcSO_4_RU8WCtDxT6N0k452lixdvwpbk65hIKai8VT_UKThmvUe7VMU3yn9RPXcGJeDGBBNGWDgA9inPvr10SZdlZb3EHlrh5uDY8zPyiM_wDxM538-Qu2mVLvE6vHTJJ8sGCCDvpy5dvt2By9u_g6MrADH87X6KNhIPLw3u3trkv9XZjpd_21dAy0ipKvaG-XrtM3r",
            "bloksData": {},
            "status": "ok"
        """
        params = {
            **({"next": command.next} if command.next else {}),
        }
        return await self.api_requester.execute(
            method="GET",
            url=constants.CHALLENGE_WEB_URL,
            extra_headers={
                "Referer": "https://www.instagram.com/challenge/",
            },
            params=params,
        )
