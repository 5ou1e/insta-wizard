from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import (
    current_timestamp,
    generate_jazoest,
)
from insta_wizard.common.utils import (
    dumps,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.responses.auth_platform.send_code_again import (
    UseAuthPlatformSendCodeAgainMutationResponse,
)


@dataclass(slots=True)
class UseAuthPlatformSendCodeAgainMutation(Command[UseAuthPlatformSendCodeAgainMutationResponse]):
    """Request resending verification code for AuthPlatform login checkpoint"""

    encrypted_ap_context: str


class UseAuthPlatformSendCodeAgainMutationHandler(
    CommandHandler[
        UseAuthPlatformSendCodeAgainMutation,
        UseAuthPlatformSendCodeAgainMutationResponse,
    ]
):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(
        self,
        command: UseAuthPlatformSendCodeAgainMutation,
    ) -> UseAuthPlatformSendCodeAgainMutationResponse:
        self.state.csrftoken_guard()

        jazoest = generate_jazoest(self.state.csrftoken)

        data = {
            "av": "0",
            "__d": "www",
            "__user": "0",
            "__a": "1",
            "__req": "9",
            "__hs": "20493.HYP:instagram_web_pkg.2.1...0",
            "dpr": "1",
            "__ccg": "GOOD",
            "__rev": "1033126112",
            "__s": self.state.local_data.web_session_id,
            "__hsi": "7604787112440269023",
            "__dyn": "7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo1nEhw2nVE4W0qa0FE2awt81s8hwnU6a3a1YwBgao6C0Mo2swaO4U2zxe2GewGw9a361qw8Xwn8e87q0oa2-azo7u3u2C2O0Lo6-3u2WE5B0bK1Iwqo5p0qZ6goK1sAwHxW1owLwlE2xyUC4o1oE",
            "__csr": "jNBPNI4Idnb4cLdkQGBiKTZnakwGit13Lmt3rjK6uem9DwzghAyF4ax27E8EcFk2SEiyWRKnCKi5UK8wAyE-4k5qwxymGx22O22u9hA2m4cwSUO8mucWz8C26dxO16gvwkEkBDxi00m-Ki3204yiw1eO3TK0eX802ijw3b2w4Bg2sCgKm0LC0k21bebwj80ye3W8VEeUmDg0-aU1J802U0w1oa",
            "__hsdp": "goC2h0X3g50AxQaEgtfzuOTfiOhZd4xm8S7Ugg21w7Nwt81oE1m8by01kG04v80Cy0qG0p60p208hw2l8",
            "__hblp": "044wau0rG1-wee1hwo87G1vw4Ewc-0h-0LU6-08Iw28U0SO0wEjwbS3C0MoO2a08gw6gw24o2aw79wroy2i13w6TwVw",
            "__sjsp": "goC2h0X3g50ypQaEgtfzuOTfL9kpjh8lyC7U2jw7Nw7nw5owK8",
            "__comet_req": "7",
            "lsd": "AdRuXsEsCP0e7CBj9Rvb_hQY0UY",
            "jazoest": jazoest,
            "__spin_r": "1033126112",
            "__spin_b": "trunk",
            "__spin_t": current_timestamp(),
            "__crn": "comet.igweb.PolarisAuthPlatformCodeEntryRoute",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useAuthPlatformSendCodeAgainMutation",
            "server_timestamps": "true",
            "variables": dumps(
                {
                    "input": {
                        "client_mutation_id": "1",
                        "actor_id": "0",
                        "encrypted_ap_context": command.encrypted_ap_context,
                    }
                }
            ),
            "doc_id": "29612122925068775",
        }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.WEB_API_GRAPHQL_URL,
            data=data,
            extra_headers={
                "X-Fb-Friendly-Name": "useAuthPlatformSendCodeAgainMutation",
                "X-Fb-Lsd": "AdHdagTBW8A",
            },
        )
        return cast(UseAuthPlatformSendCodeAgainMutationResponse, resp)
