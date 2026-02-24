from dataclasses import dataclass
from typing import cast

from insta_wizard.common.utils import dumps
from insta_wizard.mobile.commands._responses.direct.threads_add_user import (
    DirectV2ThreadsAddUserResponse,
)
from insta_wizard.mobile.common import constants
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


@dataclass(slots=True)
class DirectV2ThreadsAddUser(Command[DirectV2ThreadsAddUserResponse]):
    thread_id: str
    user_ids: list[str | int]


class DirectV2ThreadsAddUserHandler(
    CommandHandler[DirectV2ThreadsAddUser, DirectV2ThreadsAddUserResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: DirectV2ThreadsAddUser) -> DirectV2ThreadsAddUserResponse:
        payload = {
            "_uuid": self.state.device.device_id,
            "user_ids": dumps(command.user_ids),
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.DIRECT_V2_THREADS_ADD_USER_URI.format(thread_id=command.thread_id),
            data=payload,
        )
        return cast(DirectV2ThreadsAddUserResponse, resp)
