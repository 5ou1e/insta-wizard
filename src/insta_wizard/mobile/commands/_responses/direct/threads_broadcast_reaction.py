from typing import TypedDict, Any
class Payload(TypedDict):
    client_context: str
    item_id: str
    timestamp: str
    thread_id: str

class DirectV2ThreadsBroadcastReactionResponse(TypedDict):
    status: str
    status_code: str
    action: str
    payload: Payload