from typing import Any, TypedDict


class MediaCommentResponseCommentUser(TypedDict):
    pk: str
    pk_id: str
    id: str
    username: str
    full_name: str
    is_private: bool
    is_verified: bool
    profile_pic_id: str
    profile_pic_url: str
    has_onboarded_to_text_post_app: bool
    strong_id__: str
    is_mentionable: bool
    _is__IGCommentDefaultCommenterUserFieldsFragment: str


class MediaCommentResponseComment(TypedDict):
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
    distinct_emojis_used: list[Any]
    is_text_editable: bool
    keywords_data: list[Any]
    strong_id__: str
    user: MediaCommentResponseCommentUser


class MediaCommentResponse(TypedDict):
    comment: MediaCommentResponseComment
    comment_creation_key: str
    _is__TOnXIGCommentCreateMutationSuccessResponse0: str
    status: str
