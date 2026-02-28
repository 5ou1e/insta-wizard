from typing import TypedDict, Any


class _Owner(TypedDict):
    type: str
    pk: str
    name: str
    profile_pic_url: str
    lat: None
    lng: None
    location_dict: None
    short_name: None
    profile_pic_username: str
    challenge_id: None


class _ReelsItem(TypedDict):
    id: str
    strong_id__: str
    latest_reel_media: int
    seen: int
    can_reply: bool
    can_gif_quick_reply: bool
    can_reshare: bool
    reel_type: str
    ad_expiry_timestamp_in_millis: None
    is_cta_sticker_available: None
    should_treat_link_sticker_as_cta: None
    pool_refresh_ttl_in_sec: None
    can_react_with_avatar: bool
    prefetch_count: int
    expiring_at: int
    owner: _Owner
    items: list[Any]
    is_nux: bool
    unique_integer_reel_id: int
    media_count: int
    media_ids: list[Any]
    disabled_reply_types: list[str]
    is_archived: bool
    show_expiration_tray_signal: bool


class _StoryMentions(TypedDict):
    mentions_count_string: str
    reels: list[_ReelsItem]
    notif_name: str
    is_pinned_row: bool
    product_stories_count: str


class _Counts(TypedDict):
    requests: int


class _UserInfo(TypedDict):
    id: int
    username: str
    is_private: bool
    profile_pic_url: str


class _InlineFollow(TypedDict):
    user_info: _UserInfo
    following: bool
    outgoing_request: bool
    incoming_request: bool


class _LoggingContext(TypedDict):
    mentioned_user_ids: list[int]
    mentioned_content_ids: None
    content_id: None


class _InlineControlsItem(TypedDict):
    action_type: str


class _Args(TypedDict):
    destination: str
    extra_actions: list[str]
    rich_text: str
    profile_id: int
    profile_name: str
    profile_image: str
    inline_follow: _InlineFollow
    logging_context: _LoggingContext
    actions: list[str]
    inline_controls: list[_InlineControlsItem]
    content_version_id: str
    aggregation_type: str
    timestamp: float
    tuuid: str
    clicked: bool
    af_candidate_id: int
    latest_reel_media: int


class _NewStoriesItemCounts(TypedDict):
    pass


class _GenerationSource(TypedDict):
    is_send_platform: bool
    is_grand_central: bool
    is_nf_grand_central: bool
    is_hub_model: bool


class _NewStoriesItem(TypedDict):
    story_type: int
    notif_name: str
    type: int
    args: _Args
    counts: _NewStoriesItemCounts
    pk: str
    ndid: str
    trace_id: str
    generation_source: _GenerationSource


class _Extra(TypedDict):
    lat: float
    long: float


class _OldStoriesItemArgsLoggingContext(TypedDict):
    mentioned_user_ids: None
    mentioned_content_ids: None
    content_id: None


class _OldStoriesItemArgs(TypedDict):
    rich_text: str
    destination: str
    thumbnail_icon_config: None
    icon_url: str
    should_icon_apply_filter: bool
    icon_should_apply_filter: bool
    extra: _Extra
    logging_context: _OldStoriesItemArgsLoggingContext
    actions: list[str]
    inline_controls: list[_InlineControlsItem]
    content_version_id: str
    aggregation_type: str
    timestamp: float
    tuuid: str
    clicked: bool
    af_candidate_id: int


class _OldStoriesItem(TypedDict):
    story_type: int
    notif_name: str
    type: int
    args: _OldStoriesItemArgs
    counts: _NewStoriesItemCounts
    pk: str
    ndid: str
    trace_id: None
    generation_source: _GenerationSource


class _PillsItem(TypedDict):
    id: str
    name: str
    empty_state_str: str


class _BadgeCountBreakdownItem(TypedDict):
    badge_use_case_id: str
    count: int


class _BadgingInfo(TypedDict):
    total_badge_count: int
    badge_count_breakdown: list[_BadgeCountBreakdownItem]


class _UiConfig(TypedDict):
    new_timebucket_enabled: bool


class _TimeBucket(TypedDict):
    headers: list[str]
    indices: list[int]


class _Partition(TypedDict):
    time_bucket: _TimeBucket


class _IncludedFiltersItem(TypedDict):
    id: str
    name: str
    value: int


class _FiltersItem(TypedDict):
    section_header: str
    selector_type: str
    included_filters: list[_IncludedFiltersItem]


class NewsInboxResponse(TypedDict):
    friend_request_stories: list[Any]
    story_mentions: _StoryMentions
    counts: _Counts
    last_checked: float
    priority_stories: list[Any]
    new_stories: list[_NewStoriesItem]
    old_stories: list[_OldStoriesItem]
    continuation_token: int
    subscription: None
    is_first_page: bool
    is_last_page: bool
    pills: list[_PillsItem]
    badging_info: _BadgingInfo
    unaggregated_badging_info: _BadgingInfo
    ui_config: _UiConfig
    partition: _Partition
    next_max_id: str
    auto_load_more_enabled: bool
    pagination_first_record_timestamp: float
    page_num: int
    filters: list[_FiltersItem]
    status: str
