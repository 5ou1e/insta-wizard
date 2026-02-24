from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.live.live_get_good_time_for_live import (
    LiveGetGoodTimeForLiveResponse,
)
from insta_wizard.mobile.common import constants
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
class LiveGetGoodTimeForLive(Command[LiveGetGoodTimeForLiveResponse]):
    pass


class LiveGetGoodTimeForLiveHandler(
    CommandHandler[LiveGetGoodTimeForLive, LiveGetGoodTimeForLiveResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: LiveGetGoodTimeForLive) -> LiveGetGoodTimeForLiveResponse:
        data = {
            "_uid": self.state.local_data.user_id,
            "_uuid": self.state.device.device_id,
        }
        payload = build_signed_body(data)

        resp = await self.api.call_api(
            method="POST",
            uri=constants.LIVE_GET_GOOD_TIME_FOR_LIVE_URI,
            data=payload,
            client_endpoint="MainFeedFragment:feed_timeline",
        )
        return cast(LiveGetGoodTimeForLiveResponse, resp)
