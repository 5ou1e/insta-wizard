from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.commands._responses.consent.get_signup_config import (
    ConsentGetSignupConfigResponse,
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
class ConsentGetSignupConfig(Command[ConsentGetSignupConfigResponse]):
    """Получить SignupConfig с необходимыми параметрами, перед регистрацией аккаунта"""

    main_account_selected: str = "False"


class ConsentGetSignupConfigHandler(
    CommandHandler[ConsentGetSignupConfig, ConsentGetSignupConfigResponse]
):
    def __init__(self, api: ApiRequestExecutor, state: MobileClientState) -> None:
        self.api = api
        self.state = state

    async def __call__(self, command: ConsentGetSignupConfig) -> ConsentGetSignupConfigResponse:
        resp = await self.api.call_api(
            method="GET",
            uri=constants.CONSENT_GET_SIGNUP_CONFIG_URI,
            params={
                "guid": self.state.device.device_id,
                "main_account_selected": command.main_account_selected,
            },
        )
        return cast(ConsentGetSignupConfigResponse, resp)
