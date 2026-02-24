from dataclasses import dataclass
from typing import Any

from insta_wizard.web.commands._responses.challenge.bloks_navigation import (
    BloksNavigationTakeChallengeResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class BloksNavigationTakeChallenge(Command[BloksNavigationTakeChallengeResult]):
    day: int
    month: int
    year: int


class BloksNavigationTakeChallengeHandler(
    CommandHandler[BloksNavigationTakeChallenge, BloksNavigationTakeChallengeResult]
):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(
        self, command: BloksNavigationTakeChallenge
    ) -> BloksNavigationTakeChallengeResult:
        raise NotImplementedError()
        """
        Response example:
            {
                "layout": {
                    "bloks_payload": {
                        "data": [],
                        "tree": {
                            "bk.components.internal.Action": {
                                "handler": "(bk.action.core.TakeLast, (ig.action.navigation.ClearChallenge), (ig.action.navigation.CloseToScreen, (bk.action.i64.Const, 11), (bk.action.bool.Const, true)), (bk.action.i32.Const, 1))"
                            }
                        },
                        "embedded_payloads": [],
                        "error_attribution": {
                            "logging_id": "{\"callsite\":\"{\\\"oncall\\\":\\\"igwb_experiences\\\",\\\"feature\\\":\\\"HandlerForAsyncTakeChallenge\\\",\\\"product\\\":\\\"bloks_async_component\\\"}\",\"push_phase\":\"c2\"}",
                            "source_map_id": "(distillery_unknown)"
                        }
                    }
                },
                "status": "ok"
            }
        """
        # TODO challenge_context нужно брать из ответа на запрос challenge/web
        #  из этой строки - "on_click": '(bk.action.bloks.AsyncActionWithDataManifest, "com.instagram.challenge.navigation.take_challenge"

        data = {
            "challenge_context": "AaVo0eeNs4jxsqTtSPoiGuLWVctQ5nAtwfW3N68aZewja3qmLrS26zZAYc-Km-DMLtt9jIJ41JbLhe5RGaGWOmvIyy43v_xh0FnRdCeFLdNzME-XR-IvhpsHjoR2fI5mmui6nDzMiM9pkQANJ8wQEqMGqn9tW6KAlDHyL1oUZkbW_EVbyYrbJKeiNcddBgaqGz6EZurSdK7RQvLVBRVwO4medsSr_4wtyW7u55ceEc_j8PkpYJUkR3lO0pQkdOAY2b-JMSRbIxrw49gP",
            "has_follow_up_screens": "false",
            "nest_data_manifest": "true",
        }

        return await self.api_requester.execute(
            method="GET",
            url=constants.BLOKS_NAVIGATION_TAKE_CHALLENGE_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com/challenge/",
            },
        )
