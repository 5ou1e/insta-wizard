from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from insta_wizard.common.transport.models import HttpRequest
from insta_wizard.mobile.common import constants
from insta_wizard.mobile.common.headers_factory import (
    MobileClientHeadersFactory,
)
from insta_wizard.mobile.common.requesters.requester import (
    RequestExecutor,
)
from insta_wizard.mobile.common.utils import (
    build_graphql_payload,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)


class GraphqlQuery:
    def __init__(
        self,
        state: MobileClientState,
        request_executor: RequestExecutor,
        headers: MobileClientHeadersFactory,
    ):
        self.state = state
        self.request_executor = request_executor

        self.headers = headers

    async def _graphql_call(
        self,
        *,
        friendly_name: str,
        client_doc_id: str,
        root_field_name: str,
        variables: Mapping[str, Any] | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ):
        url = constants.GRAPHQL_QUERY_URL

        headers = self.headers.graphql_headers()
        headers.update(
            {
                "x-client-doc-id": client_doc_id,
                "x-fb-friendly-name": friendly_name,
                "x-root-field-name": root_field_name,
                "x-graphql-client-library": "pando",
            }
        )
        if extra_headers:
            headers.update(dict(extra_headers))

        payload = build_graphql_payload(
            friendly_name=friendly_name,
            client_doc_id=client_doc_id,
            variables=dict(variables or {}),
        )

        return await self.request_executor(
            HttpRequest(
                method="POST",
                url=url,
                headers=headers,
                data=payload,
            )
        )

    async def GetResurrectedUserNUXEligibility(self):
        return await self._graphql_call(
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
        return await self._graphql_call(
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
        return await self._graphql_call(
            friendly_name="IGRealtimeRegionHintQuery",
            client_doc_id="52232106018313849661757113193",
            root_field_name="xdt_igd_msg_region",
            variables={},
        )
