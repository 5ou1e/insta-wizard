from typing import TypedDict


class _Media(TypedDict):
    pk: str
    has_liked: bool


class MediaLikeResponse(TypedDict):
    media: _Media
    status: str
    status_code: str
