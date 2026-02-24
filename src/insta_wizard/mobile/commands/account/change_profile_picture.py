from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.account.account_change_profile_picture import (
    AccountChangeProfilePictureResponse,
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
class AccountChangeProfilePicture(Command[AccountChangeProfilePictureResponse]):
    """Set account profile picture (requires upload_id)"""

    upload_id: str


class AccountChangeProfilePictureHandler(
    CommandHandler[AccountChangeProfilePicture, AccountChangeProfilePictureResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: AccountChangeProfilePicture,
    ) -> AccountChangeProfilePictureResponse:
        data = {
            "_uuid": self.state.device.device_id,
            "device_id": self.state.device.android_id,
            "use_fbuploader": True,
            "upload_id": command.upload_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.ACCOUNTS_CHANGE_PROFILE_PICTURE_URI,
            data=data,
        )
        return cast(AccountChangeProfilePictureResponse, resp)
