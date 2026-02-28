from typing import Any, TypedDict


class _Comment(TypedDict):
    pk: str
    text: str
    user_id: str
    type: int
    did_report_as_spam: bool
    created_at: int
    created_at_utc: int
    created_at_for_fb_app: int
    content_type: str
    status: str
    bit_flags: int
    share_enabled: bool
    media_id: str
    carousel_child_mentions: list[Any]
    has_liked_comment: bool


class MediaCommentLikeResponse(TypedDict):
    comment: _Comment
    status: str
    status_code: str
