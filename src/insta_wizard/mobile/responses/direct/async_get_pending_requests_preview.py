from typing import TypedDict


class DirectV2AsyncGetPendingRequestsPreviewResponse(TypedDict):
    pending_requests_total: int
    unread_pending_requests: int
    notes: None
    status: str
    status_code: str
