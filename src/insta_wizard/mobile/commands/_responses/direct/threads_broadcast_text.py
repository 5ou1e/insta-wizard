from typing import TypedDict, Any


class Payload(TypedDict):
    client_context: str
    item_id: str
    timestamp: str
    thread_id: str
    msg_id: str


class DirectV2ThreadsBroadcastTextResponse(TypedDict):
    action: str
    status_code: str
    payload: Payload
    status: str
