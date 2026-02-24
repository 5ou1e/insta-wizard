from dataclasses import dataclass
from typing import Any, cast

from insta_wizard.common.generators import (
    generate_uuid_v4_string,
)
from insta_wizard.common.utils import (
    dumps,
)
from insta_wizard.web.commands._responses.search.polaris_search_box import (
    PolarisSearchBoxRefetchableQueryResult,
)
from insta_wizard.web.common import constants
from insta_wizard.web.common.command import (
    Command,
    CommandHandler,
)
from insta_wizard.web.models.state import WebClientState


@dataclass(slots=True)
class PolarisSearchBoxRefetchableQuery(Command[PolarisSearchBoxRefetchableQueryResult]):
    """Search users by username (GraphQL API)"""

    query: str


class PolarisSearchBoxRefetchableQueryHandler(
    CommandHandler[PolarisSearchBoxRefetchableQuery, PolarisSearchBoxRefetchableQueryResult]
):
    def __init__(self, api_requester: Any, state: WebClientState) -> None:
        self.api_requester = api_requester
        self.state = state

    async def __call__(
        self,
        command: PolarisSearchBoxRefetchableQuery,
    ) -> PolarisSearchBoxRefetchableQueryResult:
        raise NotImplementedError()
        # TODO Метод сломан - отдает в 'xdt_api__v1__fbsearch__topsearch_connection': None - видимо из-за кривых\недостающих параметров в запросе
        query = command.query
        initial_params = self.state.initial_params

        data = {
            "av": "17841445438378523",
            "__d": "www",
            "__user": "0",
            "__a": "1",
            "__req": "10",
            "__hs": initial_params.haste_session,
            "dpr": str(self.state.device.dpr),
            "__ccg": "GOOD",
            "__rev": initial_params.spin_r,
            "__s": "02tz5q:w24u4t:46svda",
            "__hsi": initial_params.hsi,
            "__dyn": "7xeUjG1mxu1syaxG4Vp41twpUnwgU7SbzEdF8aUco2qwJyEiw9-1DwUx609vCwjE1EEc87m0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo31w9a9wlo5qfK0zEkxe2GewGw9a361qwuEjUlwhEe88o5i7U1oEbUGdG1QwTU9UaQ0Lo6-bwHwKG1pg2fwxyo6O1FwlA3a3zhAq4rwQyXxui2qiUqwm8jxK1mwa6bBK4o16U8opyFEaU4y16wAwj8",
            "__csr": "gF5NQegVkvs4lh79fcPNqaBXuNt9ldquB6eteuUHkMKutrHnJfh6BJaSqhqLRjyvm8gzzkvCxaFpLHBh4fgCJyyKp4HBiq9uWbiCAjHGQiihbhryd2GxmvAi-8hpEPAFd4yV9XUKu5aKBVXBF5BHyDmAbDyJ9ABF7iVkp2b8mUpLiFfmiluiQjoFpQdypoOuF8DFCy9bhpoGV-iqaCxOibBiBzoG9xq0xU01qT8IUchoWWwcO4E3Iw99047wdifwgA17Dl0dO1ewZU0wMMpwm41rBx0lgc8vxkPDQbybhdm4FU2cxy4azEuwXdxy1pwsUG7o1v20feu0J41nwXwr80GyCB_wSo0UStwRwaK0Gi0yU2bYQAwqDm0N9EC68zofu7611D4yUR0qFOw-w9lw58wj3e8wio0x-Oz8lxuu1jCh8vw3b2amei8m92U40yAw68wHw83y_yVE6a2Gt0kEd4bxm0XU5-0bSw4yw3bE1o5BBZ0Ow1yy0a_w1Zq8w17l5RweXU0xR0evEE2lwdS4pE7G06co1mWwdW7k0S8x2BWgbQ0M87Cq",
            "__hsdp": "go4Mx1-whwFaxcn2IptNkLYn8h58X98ygQkKMYGkQ_sl6g_11hy8I886kvgOB2qtetwAB12eq72hRCylu6hFyAyAp10wow8qcwDwOSm0ji0L80KG1NwXw17u05eUeU6K2m5o3xU3iwcG0Uo7G09rwcJ06EwtU2Kw",
            "__hblp": "0Xwa63eewRCxKq4AagG0x8cEao63Bw-Dx6iqmaAx2fpubhUkx25EfecwEmE8EyA9yVoOp4VGGqm5K6oOFU8459rh9EcaypVoSXK2mrxe4UqHWDyaGQqqfUhUmiCCxubzEhxjU-u4UCUBG7o6m5GVoymewIgHohghxaq2OEdrwOxi22h1yEtUhyku6VGJ1Si5U7q2W262jw64w6BxK3WEbk0O829xW7obo4Lg14axK-A3u0QolxO0y8C37wqu2eump2UpyEW361jwYU6O14wxway0G8e8y2W12DxW0xEf8boW8wgohwc-q3-586qEN0-wko5C1KCwhUmDyEeoig98K49k4ofpIwCFomwTz8y12wmEnwCwICCwIg",
            "__sjsp": "go4Mx1-whwFaxcn2IptYhb_sYx4kzIAy93hiXMGyGBdfT5hAfMgkoyb221B7QcFgCDjDo99ggzCxMAthUBnxAqoF8F6g2Pw0iiU",
            "fb_dtsg": initial_params.dtsg_token,
            "__comet_req": initial_params.comet_env,
            "lsd": initial_params.lsd_token,
            "jazoest": initial_params.jazoest,
            "__spin_r": initial_params.spin_r,
            "__spin_b": initial_params.spin_b,
            "__spin_t": initial_params.spin_t,
            "__crn": "comet.igweb.PolarisOneTapAfterLoginRoute",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "PolarisSearchBoxRefetchableQuery",
            "server_timestamps": "true",
            "variables": dumps(
                {
                    "data": {
                        "context": "blended",
                        "include_reel": "true",
                        "query": query,
                        "rank_token": "1770517571651|cf35fac29cbf693c5b7f9aa475b6ed98f9eddad0da500e99954bd6acd75bd1d2",
                        "search_session_id": generate_uuid_v4_string(),
                        "search_surface": "web_top_search",
                    },
                    "hasQuery": True,
                }
            ),
            "doc_id": "24146980661639222",
        }

        resp = await self.api_requester.execute(
            method="POST",
            url=constants.WEB_API_GRAPHQL_URL,
            data=data,
            extra_headers={
                "X-Fb-Friendly-Name": "PolarisSearchBoxRefetchableQuery",
                "X-Fb-Lsd": initial_params.lsd_token,
                "X-BLOKS-VERSION-ID": initial_params.versioning_id,
                "X-Root-Field-Name": "xdt_api__v1__fbsearch__topsearch_connection",
            },
        )
        return cast(PolarisSearchBoxRefetchableQueryResult, resp)
