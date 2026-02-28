from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.notifications.badge import (
    NotificationsBadgeResponse,
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
class NotificationsBadge(Command[NotificationsBadgeResponse]):
    pass


class NotificationsBadgeHandler(CommandHandler[NotificationsBadge, NotificationsBadgeResponse]):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: NotificationsBadge) -> NotificationsBadgeResponse:
        data = {
            "phone_id": self.state.device.phone_id,
            "trigger": "NOTIFICATION_FEED_HEART_ICON",
            "user_ids": self.state.local_data.user_id,
            "device_id": self.state.device.device_id,
            "_uuid": self.state.device.device_id,
        }

        resp = await self.api.call_api(
            method="POST",
            uri=constants.NOTIFICATIONS_BADGE_URI,
            data=data,
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(NotificationsBadgeResponse, resp)
