from dataclasses import dataclass
from typing import cast

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
from insta_wizard.mobile.responses.notifications.get_notification_settings import (
    NotificationsGetNotificationSettingsResponse,
)


@dataclass(slots=True)
class NotificationsGetNotificationSettings(Command[NotificationsGetNotificationSettingsResponse]):
    pass


class NotificationsGetNotificationSettingsHandler(
    CommandHandler[
        NotificationsGetNotificationSettings,
        NotificationsGetNotificationSettingsResponse,
    ]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(
        self,
        command: NotificationsGetNotificationSettings,
    ) -> NotificationsGetNotificationSettingsResponse:
        data = await self.api.call_api(
            method="GET",
            uri=constants.NOTIFICATIONS_GET_NOTIFICATION_SETTINGS_URI,
            params={"content_type": "post_and_comments"},
            client_endpoint="com.bloks.www.caa.login.login_homepage",
        )
        return cast(NotificationsGetNotificationSettingsResponse, data)
