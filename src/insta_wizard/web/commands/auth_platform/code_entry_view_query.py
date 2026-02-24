from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import (
    current_timestamp,
    generate_jazoest,
)
from insta_wizard.common.utils import (
    dumps,
)
from insta_wizard.web.commands._responses.auth_platform.code_entry_view_query import (
    AuthPlatformCodeEntryViewQueryResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class AuthPlatformCodeEntryViewQuery(Command[AuthPlatformCodeEntryViewQueryResult]):
    apc: str


class AuthPlatformCodeEntryViewQueryHandler(
    CommandHandler[AuthPlatformCodeEntryViewQuery, AuthPlatformCodeEntryViewQueryResult]
):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(
        self,
        command: AuthPlatformCodeEntryViewQuery,
    ) -> AuthPlatformCodeEntryViewQueryResult:
        self.state.csrftoken_guard()

        jazoest = generate_jazoest(self.state.csrftoken)
        apc = command.apc

        data = {
            "av": "0",
            "__d": "www",
            "__user": "0",
            "__a": "1",
            "__req": "1",
            "__hs": "20473.HYP:instagram_web_pkg.2.1...0",
            "dpr": "1",
            "__ccg": "MODERATE",
            "__rev": "1032195405",
            "__s": self.state.local_data.web_session_id,
            "__hsi": "7597569751052904312",
            "__dyn": "7xe6E5q5U5ObwKBBwno6u5U4e0C8dEc8co38w5ux609vCwjE1EE2Cw8G0um4o5-1ywOwv89k2C0iK0D830wae4UaEW2G0AEco5G0zE5W3y0vC2-azo7u3u2C2O0Lo6-3u2WE5B0bK1Iwqo5p0qZ6goK1sAwHxW1owLwHwcObyohw5yw",
            "__csr": "jOMyw8cn7YBlliSyibTaPIGLuGi8AZ2pBpHDiKEypz9UgypEGEgHy4UJ2Q13yawByEkzERaE8UK4mbV46K4kqml246U_z9UOhyVodoao-8xm4qxa5HzQp48i6UcoWeyUSbxa4ElgeE4Km12U37w05B2yE7e1Ow6Y40Tw1G2q5rwf-9wjy00JwU0-F0b613Q0RC0lC15ycU5e08RDgeyUJ03hrw9C00KlU0m2w",
            "__hsdp": "l1qsn15361fja8GuggFVpQTcwAANahErymidxZ0Sw2JUjwe20nm0YO00I8wbXw6nw1lC",
            "__hblp": "05-wHw7sw4RwUwpE6m0gS14w9q1dw53w8G3e09LwhE1KE4y0jG0aWwZxu2C08Kw3Mo1BU6a4UiwkE1Do",
            "__sjsp": "l1qsn2hoJA2e1ka8GueDBDh5cwAATl96xK9oiwlU0Hu0Z81to3P8",
            "__comet_req": "7",
            "lsd": "AdHdagTBW8A",
            "jazoest": jazoest,
            "__spin_r": "1032195405",
            "__spin_b": "trunk",
            "__spin_t": current_timestamp(),
            "__crn": "comet.igweb.PolarisAuthPlatformCodeEntryRoute",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "AuthPlatformCodeEntryViewQuery",
            "variables": dumps(
                {
                    "apc": apc,
                }
            ),
            "server_timestamps": "true",
            "doc_id": "25704707145784488",
        }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.WEB_API_GRAPHQL_URL,
            data=data,
            extra_headers={
                "X-Fb-Friendly-Name": "AuthPlatformCodeEntryViewQuery",
                "X-Fb-Lsd": "AdHdagTBW8A",  # ???
            },
        )
        return cast(AuthPlatformCodeEntryViewQueryResult, resp)
