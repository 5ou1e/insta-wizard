from typing import Any, TypedDict


class _ImageCandidate(TypedDict):
    url: str
    width: int
    height: int


class _ImageVersions2(TypedDict):
    candidates: list[_ImageCandidate]


class _Caption(TypedDict):
    pk: str
    text: str
    user_id: int
    media_id: int
    created_at: int
    created_at_utc: int


class _User(TypedDict):
    pk: int
    id: str
    username: str
    full_name: str
    is_private: bool
    is_verified: bool
    profile_pic_url: str


class _MediaItem(TypedDict):
    pk: int
    id: str
    code: str
    media_type: int  # 1 = photo, 2 = video
    product_type: str  # "feed"
    taken_at: int
    device_timestamp: int
    original_width: int
    original_height: int
    image_versions2: _ImageVersions2
    caption: _Caption | None
    like_count: int
    comment_count: int
    filter_type: int
    has_liked: bool
    can_viewer_reshare: bool
    can_viewer_save: bool
    has_shared_to_fb: int
    is_paid_partnership: bool
    organic_tracking_token: str
    sharing_friction_info: dict[str, Any]
    user: _User


class MediaConfigureResponse(TypedDict):
    upload_id: str
    media: _MediaItem
    status: str
