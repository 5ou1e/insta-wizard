from __future__ import annotations

from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


class GraphqlQuery:
    def __init__(
        self,
        state: MobileClientState,
        requester: MobileRequester,
    ):
        self.state = state
        self.requester = requester

    async def GetResurrectedUserNUXEligibility(self):
        return await self.requester.call_graphql_query(
            friendly_name="GetResurrectedUserNUXEligibility",
            client_doc_id="221788370615369272591224122891",
            root_field_name="xdt_async_should_show_resurrected_user_flow",
            variables={
                "request_data": {
                    "is_push_enabled": True,
                    "dp_nux_eligible": True,
                    "ci_nux_eligible": True,
                }
            },
        )

    async def GetOnboardingNuxEligibility(self):
        return await self.requester.call_graphql_query(
            friendly_name="GetOnboardingNuxEligibility",
            client_doc_id="222791017215896159003559603708",
            root_field_name="xdt_async_should_show_nux_flow",
            variables={
                "request_data": {
                    "push_permission_requested": False,
                    "ci_nux_eligible": True,
                }
            },
        )

    async def IGRealtimeRegionHintQuery(self):
        return await self.requester.call_graphql_query(
            friendly_name="IGRealtimeRegionHintQuery",
            client_doc_id="52232106018313849661757113193",
            root_field_name="xdt_igd_msg_region",
            variables={},
        )
