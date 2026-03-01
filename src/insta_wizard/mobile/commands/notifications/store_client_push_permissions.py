from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)
from insta_wizard.mobile.responses.notifications.store_client_push_permissions import (
    NotificationsStoreClientPushPermissionsResponse,
)


@dataclass(slots=True)
class NotificationsStoreClientPushPermissions(
    Command[NotificationsStoreClientPushPermissionsResponse]
):
    pass


class NotificationsStoreClientPushPermissionsHandler(
    CommandHandler[
        NotificationsStoreClientPushPermissions,
        NotificationsStoreClientPushPermissionsResponse,
    ]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(
        self,
        command: NotificationsStoreClientPushPermissions,
    ) -> NotificationsStoreClientPushPermissionsResponse:
        payload = {
            "enabled": "false",
            "device_id": self.state.device.device_id,
            "_uuid": self.state.device.device_id,
        }

        resp = await self.requester.call_api(
            method="POST",
            uri="notifications/store_client_push_permissions/",
            data=payload,
            client_endpoint="feed_timeline",
            extra_headers={
                "x-ig-nav-chain": "MainFeedFragment:feed_timeline:1:cold_start:1755922781.967::",
            },
        )
        return cast(NotificationsStoreClientPushPermissionsResponse, resp)
