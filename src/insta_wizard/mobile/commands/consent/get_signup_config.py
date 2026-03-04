from dataclasses import dataclass
from typing import cast

from insta_wizard.mobile.common import constants
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
from insta_wizard.mobile.responses.consent.get_signup_config import (
    ConsentGetSignupConfigResponse,
)


@dataclass(slots=True)
class ConsentGetSignupConfig(Command[ConsentGetSignupConfigResponse]):
    """Get SignupConfig with required parameters before account registration"""

    main_account_selected: bool = False


class ConsentGetSignupConfigHandler(
    CommandHandler[ConsentGetSignupConfig, ConsentGetSignupConfigResponse]
):
    def __init__(self, requester: MobileRequester, state: MobileClientState) -> None:
        self.requester = requester
        self.state = state

    async def __call__(self, command: ConsentGetSignupConfig) -> ConsentGetSignupConfigResponse:
        resp = await self.requester.call_api(
            method="GET",
            uri=constants.CONSENT_GET_SIGNUP_CONFIG_URI,
            params={
                "guid": self.state.device.device_id,
                "main_account_selected": str(command.main_account_selected),
            },
        )
        return cast(ConsentGetSignupConfigResponse, resp)
