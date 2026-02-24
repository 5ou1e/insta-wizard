from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import (
    current_timestamp,
    generate_jazoest,
)
from insta_wizard.common.utils import (
    dumps,
)
from insta_wizard.web.commands._responses.auth_platform.submit_code import (
    UseAuthPlatformSubmitCodeMutationResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class UseAuthPlatformSubmitCodeMutation(Command[UseAuthPlatformSubmitCodeMutationResult]):
    """Отправить код подтверждения при чекпоинте авторизации AuthPlatform"""

    code: str
    encrypted_ap_context: str


class UseAuthPlatformSubmitCodeMutationHandler(
    CommandHandler[
        UseAuthPlatformSubmitCodeMutation,
        UseAuthPlatformSubmitCodeMutationResult,
    ]
):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(
        self,
        command: UseAuthPlatformSubmitCodeMutation,
    ) -> UseAuthPlatformSubmitCodeMutationResult:
        self.state.csrftoken_guard()

        jazoest = generate_jazoest(self.state.csrftoken)

        data = {
            "av": "0",
            "__d": "www",
            "__user": "0",
            "__a": "1",
            "__req": "1",
            "__hs": "20473.HYP:instagram_web_pkg.2.1...0",
            "dpr": "1",
            "__ccg": "GOOD",
            "__rev": "1032213758",
            "__s": self.state.local_data.web_session_id,
            "__hsi": "7597618180985208367",
            "__dyn": "7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo1nEhw2nVE4W0qa0FE2awt81s8hwnU6a3a1YwBgao6C0Mo2swaO4U2zxe2GewGw9a361qw8Xwn8e87q0oa2-azo7u3u2C2O0Lo6-3u2WE5B0bK1Iwqo5p0qZ6goK1sAwHxW1owLwHwGwa6byohw5yw",
            # mb random
            "__csr": "gRik2hONBtH7mBlQPPvlqnT-oyKaChZ4RzJ5GF4K23BF1eUmozh-dy8S2-2OczEO2GfAh948yUlF2GU-cFa4ecyHgnGcBFecwzw-x2bGVUuGfxjKl0Emm4ocrx-uczFVEak2W3O7o2mg2qw05AwyHwso0yUMW2F01GWdAU3xx-1h802Si5o0YF0b614o3oo1mU4m8PwkU0zBwZmm8gKu0cIK0Co02VHw1mK",
            # mb random
            "__hsdp": "go21I784ZcC9GaN1aCCA2qTbPSA9yolyJy8vgbE0Iacw48w4Qw41802H60ZK0l-05K8",
            "__hblp": "05qwjo1To13E5C0xEeHw47wdG6oe81QUbUO0tS08ew4Cwyw3dUcoG16w21E0Ym0yE1go9ohwww64wh8",
            "__sjsp": "go21I85yy4285gC9GazqCCB7QJOYLqgC9xmcoy1fw2ME15o1d810i0",
            "__comet_req": "7",
            "lsd": "AdHdagTBW8A",
            "jazoest": jazoest,
            "__spin_r": "1032213758",
            "__spin_b": "trunk",
            "__spin_t": current_timestamp(),
            "__crn": "comet.igweb.PolarisAuthPlatformCodeEntryRoute",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useAuthPlatformSubmitCodeMutation",
            "variables": dumps(
                {
                    "input": {
                        "client_mutation_id": "6",
                        "actor_id": "0",
                        "code": command.code,
                        "encrypted_ap_context": command.encrypted_ap_context,
                    }
                }
            ),
            "server_timestamps": "true",
            "doc_id": "25017097917894476",
        }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.WEB_API_GRAPHQL_URL,
            data=data,
            extra_headers={
                "X-Fb-Friendly-Name": "useAuthPlatformSubmitCodeMutation",
                "X-Fb-Lsd": "AdHdagTBW8A",
            },
        )
        return cast(UseAuthPlatformSubmitCodeMutationResult, resp)
