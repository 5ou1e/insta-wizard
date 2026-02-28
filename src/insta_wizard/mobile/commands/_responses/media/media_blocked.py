from typing import TypedDict, Any

class MediaBlockedResponse(TypedDict):
    media_ids: list[Any]
    status: str