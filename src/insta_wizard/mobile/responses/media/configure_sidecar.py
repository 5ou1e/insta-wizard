from typing import Any, TypedDict


class _ImageCandidate(TypedDict):
    url: str
    width: int
    height: int


class _ImageVersions2(TypedDict):
    candidates: list[_ImageCandidate]


class _CarouselItem(TypedDict):
    pk: int
    id: str
    media_type: int  # 1 = photo, 2 = video
    image_versions2: _ImageVersions2
    original_width: int
    original_height: int
    carousel_parent_id: str
    product_type: str  # "carousel_item"


class _Caption(TypedDict):
    pk: str
    text: str
    user_id: int
    created_at: int


class _User(TypedDict):
    pk: int
    id: str
    username: str
    full_name: str
    is_private: bool
    is_verified: bool
    profile_pic_url: str


class _SidecarMedia(TypedDict):
    pk: int
    id: str
    code: str
    media_type: int  # 8 = carousel_container
    product_type: str  # "carousel_container"
    taken_at: int
    device_timestamp: int
    image_versions2: _ImageVersions2
    original_width: int
    original_height: int
    carousel_media_count: int
    carousel_media_ids: list[int]
    carousel_media: list[_CarouselItem]
    caption: _Caption | None
    like_count: int
    comment_count: int
    can_viewer_reshare: bool
    can_viewer_save: bool
    has_liked: bool
    user: _User
    filter_type: int
    sharing_friction_info: dict[str, Any]


class MediaConfigureSidecarResponse(TypedDict):
    client_sidecar_id: str
    media: _SidecarMedia
    status: str
