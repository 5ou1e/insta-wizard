from typing import Any, TypedDict


class MediaBlockedResponse(TypedDict):
    media_ids: list[Any]
    status: str
