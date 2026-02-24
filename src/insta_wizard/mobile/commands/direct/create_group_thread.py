from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.direct.create_group_thread import (
    DirectV2CreateGroupThreadResponse,
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
class DirectV2CreateGroupThread(Command[DirectV2CreateGroupThreadResponse]):
    recipient_users: list[str]
    thread_title: str


class DirectV2CreateGroupThreadHandler(
    CommandHandler[DirectV2CreateGroupThread, DirectV2CreateGroupThreadResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self, command: DirectV2CreateGroupThread
    ) -> DirectV2CreateGroupThreadResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            **({"_uid": self.state.local_data.user_id} if self.state.local_data.user_id else {}),
            "recipient_users": command.recipient_users,
            "thread_title": command.thread_title,
        }
        data = build_signed_body(payload)
        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_GET_CREATE_GROUP_THREAD_URI,
            data=data,
            # client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(DirectV2CreateGroupThreadResponse, resp)
