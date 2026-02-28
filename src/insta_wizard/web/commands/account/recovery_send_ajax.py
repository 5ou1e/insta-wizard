from dataclasses import dataclass
from typing import cast

from insta_wizard.common.generators import generate_jazoest
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.common.requesters.api_requester import (
    WebApiRequester,
)
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.account.recovery_send_ajax import (
    AccountRecoverySendAjaxResponse,
)


@dataclass(slots=True)
class AccountRecoverySendAjax(Command[AccountRecoverySendAjaxResponse]):
    """Send password recovery link to email"""

    email_or_username: str


class AccountRecoverySendAjaxHandler(
    CommandHandler[AccountRecoverySendAjax, AccountRecoverySendAjaxResponse]
):
    def __init__(self, api_requester: WebApiRequester, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(
        self,
        command: AccountRecoverySendAjax,
    ) -> AccountRecoverySendAjaxResponse:
        # Response example
        # {
        #     "title": "Сообщение отправлено",
        #     "body": "Мы отправили ссылку для восстановления доступа к вашему аккаунту на адрес s******t@m*****.com.",
        #     "can_recover_with_code": false,
        #     "contact_point": "s******t@m*****.com",
        #     "recovery_method": "send_email",
        #     "status": "ok"
        # }

        self.state.csrftoken_guard()

        data = {
            "email_or_username": command.email_or_username,
            "jazoest": generate_jazoest(self.state.csrftoken),
        }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.ACCOUNT_RECOVERY_SEND_AJAX_URL,
            data=data,
            extra_headers={
                "Referer": "https://www.instagram.com/accounts/password/reset/",
            },
        )

        return cast(AccountRecoverySendAjaxResponse, resp)
