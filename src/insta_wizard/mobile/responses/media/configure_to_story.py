from typing import Any, TypedDict


class _ImageCandidate(TypedDict):
    url: str
    width: int
    height: int


class _ImageVersions2(TypedDict):
    candidates: list[_ImageCandidate]


class _User(TypedDict):
    pk: int
    id: str
    username: str
    full_name: str
    is_private: bool
    is_verified: bool
    profile_pic_url: str


class _StoryMedia(TypedDict):
    pk: int
    id: str
    code: str
    media_type: int  # 1 = photo, 2 = video
    original_media_type: int
    product_type: str  # "story"
    source_type: int  # 3 = camera
    taken_at: int
    device_timestamp: int
    expiring_at: int
    original_width: int
    original_height: int
    image_versions2: _ImageVersions2
    caption: Any
    filter_type: int
    is_reel_media: bool
    story_is_saved_to_archive: bool
    can_reshare: bool
    can_reply: bool
    viewer_count: int
    total_viewer_count: int
    has_shared_to_fb: int
    is_paid_partnership: bool
    organic_tracking_token: str
    sharing_friction_info: dict[str, Any]
    user: _User


class MediaConfigureToStoryResponse(TypedDict):
    upload_id: str
    media: _StoryMedia
    status: str
