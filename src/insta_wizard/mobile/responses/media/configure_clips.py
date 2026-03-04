from typing import Any, TypedDict


class _MediaItem(TypedDict):
    pk: int
    id: str
    code: str
    media_type: int
    product_type: str  # "clips"
    taken_at: int
    original_width: int
    original_height: int
    caption: dict[str, Any] | None
    like_count: int
    comment_count: int
    has_liked: bool


class MediaConfigureToClipsResponse(TypedDict):
    upload_id: str
    media: _MediaItem
    status: str
