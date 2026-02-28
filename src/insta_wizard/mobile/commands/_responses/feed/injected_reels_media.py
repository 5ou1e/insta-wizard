from typing import TypedDict, Any


class _Reel(TypedDict):
    pass


class FeedInjectedReelsMediaResponse(TypedDict):
    reels: _Reel
    earliest_request_position: int
    status: str
