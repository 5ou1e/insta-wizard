from typing import Any, TypedDict


class MediaCommentsResponseCaptionUser(TypedDict):
    fbid_v2: int
    full_name: str
    id: str
    is_private: bool
    is_unpublished: bool
    is_verified: bool
    pk: int
    pk_id: str
    profile_pic_id: str
    profile_pic_url: str
    strong_id__: str
    username: str


class MediaCommentsResponseCaption(TypedDict):
    bit_flags: int
    content_type: str
    created_at: int
    created_at_for_fb_app: int
    created_at_utc: int
    did_report_as_spam: bool
    is_covered: bool
    is_created_by_media_owner: bool
    is_ranked_comment: bool
    has_translation: bool
    media_id: int
    pk: str
    private_reply_status: int
    share_enabled: bool
    status: str
    strong_id__: str
    text: str
    type: int
    user: MediaCommentsResponseCaptionUser
    user_id: int


class MediaCommentsResponseCommentsItemUser(TypedDict):
    fbid_v2: int
    full_name: str
    id: str
    is_mentionable: bool
    is_private: bool
    is_verified: bool
    latest_reel_media: int
    pk: int
    pk_id: str
    profile_pic_id: str
    profile_pic_url: str
    strong_id__: str
    username: str
    qe_use_smaller_comment_like_tap_target: bool
    has_onboarded_to_text_post_app: bool


class MediaCommentsResponseCommentsItem(TypedDict):
    bit_flags: int
    child_comment_count: int
    comment_index: int
    comment_like_count: int
    content_type: str
    created_at: int
    created_at_for_fb_app: int
    created_at_utc: int
    did_report_as_spam: bool
    has_liked_comment: bool
    has_disliked_comment: bool
    inline_composer_display_condition: str
    is_covered: bool
    is_photo_comments_enabled_for_comment_author: bool
    is_text_editable: bool
    is_edited: bool
    is_ranked_comment: bool
    keywords_data: list[Any]
    liked_by_media_coauthors: list[Any]
    other_preview_users: list[Any]
    media_id: int
    pk: str
    preview_child_comments: list[Any]
    private_reply_status: int
    share_enabled: bool
    status: str
    strong_id__: str
    text: str
    type: int
    user: MediaCommentsResponseCommentsItemUser
    user_id: int


class MediaCommentsResponseQuickResponseEmojisItem(TypedDict):
    unicode: str


class MediaCommentsResponse(TypedDict):
    can_view_more_preview_comments: bool
    caption: MediaCommentsResponseCaption
    caption_is_edited: bool
    comment_count: int
    comment_cover_pos: str
    comment_filter_param: str
    comment_likes_enabled: bool
    comments: list[MediaCommentsResponseCommentsItem]
    has_more_comments: bool
    has_more_headload_comments: bool
    initiate_at_top: bool
    insert_new_comment_to_top: bool
    is_ranked: bool
    liked_by_media_owner_badge_enabled: bool
    media_header_display: str
    next_min_id: str
    quick_response_emojis: list[MediaCommentsResponseQuickResponseEmojisItem]
    scroll_behavior: int
    threading_enabled: bool
    filter_options: list[Any]
    sort_options: list[Any]
    should_render_upsell: bool
    foundation_improvements_enabled: bool
    has_more_headload_fb_comments: bool
    fb_comments: list[Any]
    ai_topic_filters: list[Any]
    status: str
