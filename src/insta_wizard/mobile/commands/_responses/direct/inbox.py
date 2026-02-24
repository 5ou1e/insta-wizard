from typing import TypedDict, Any


class IcebreakerSuggestions(TypedDict):
    mutually_liked_reels: list[Any]
    mutual_followed_creators: list[Any]
    mutual_friends: list[Any]
    sticker_packs: list[Any]


class Snippet(TypedDict):
    pass


class PublicChatMetadata(TypedDict):
    is_public: bool
    is_pinnable_to_viewer_profile: bool
    is_pinned_to_viewer_profile: bool
    is_added_to_inbox: bool
    is_subscribed_collaborator: bool
    channel_end_source: None
    is_comments_enabled: bool
    hidden_emojis: None
    channel_end_timestamp: int
    is_xposting_eligible: bool
    is_linked_account_eligible_for_xposting: bool
    xposting_available_channel_count: int


class SnoozedMessagesMetadata(TypedDict):
    snoozed_messages_count: int
    last_snoozed_message_timestamp_ms: int
    show_snooze_pill: bool


class Nudge(TypedDict):
    create_time: None
    nudge_type: int


class NicknamesSettingItem(TypedDict):
    user_igid: str
    nickname_setting: str


class ParticipantRequestsCount(TypedDict):
    participant_requests_count: int
    timestamp: int


class FriendshipStatus(TypedDict):
    following: bool
    followed_by: bool
    is_bestie: bool
    is_feed_favorite: bool
    is_restricted: bool
    outgoing_request: bool
    incoming_request: bool
    muting: bool
    blocking: bool
    is_messaging_pseudo_blocking: bool
    is_private: bool
    is_viewer_unconnected: bool
    reachability_status: int


class UsersItem(TypedDict):
    id: str
    strong_id__: str
    pk: int
    pk_id: str
    full_name: str
    username: str
    account_type: int
    short_name: str
    profile_pic_url: str
    is_verified: bool
    interop_messaging_user_fbid: int
    fbid_v2: int
    has_ig_profile: bool
    interop_user_type: int
    is_using_unified_inbox_for_direct: bool
    is_private: bool
    is_cannes: bool
    is_ring_creator: bool
    show_ring_award: bool
    is_creator_agent_enabled: bool
    is_creator_automated_response_enabled: bool
    has_highlight_reels: bool
    biz_user_inbox_state: int
    wa_eligibility: int
    wa_addressable: bool
    account_badges: list[Any]
    is_eligible_for_rp_safety_notice: bool
    is_eligible_for_igd_stacks: bool
    profile_pic_id: str
    has_anonymous_profile_picture: bool
    date_joined: int
    friendship_status: FriendshipStatus
    is_shared_account: bool
    is_shared_account_with_messaging_access: bool
    ai_agent_banner_type: None
    is_eligible_for_ai_bot_group_chats: bool
    ai_agent_can_participate_in_audio_call: None
    ai_agent_can_participate_in_video_call: None


class Theme(TypedDict):
    id: str


class LastSeenAtValue(TypedDict):
    item_id: str
    timestamp: str
    created_at: str
    shh_seen_state: Snippet


class ItemType(TypedDict):
    text: int


class BtvEnabledMap(TypedDict):
    item_type: ItemType
    ttlc: int
    proton: int


class IgThreadCapabilities(TypedDict):
    capabilities_0: int
    capabilities_1: int


class PaidPartnershipInfo(TypedDict):
    is_paid_partnership: bool


class Fallback(TypedDict):
    url: str


class PreviewUrlInfo(TypedDict):
    url: str
    fallback: Fallback
    url_expiration_timestamp_us: int
    width: int
    height: int


class CtaButtonsItem(TypedDict):
    title: str
    action_url: str
    cta_type: None
    xma_action: str


class XmaReelMentionItem(TypedDict):
    xma_template_type: None
    xma_layout_type: int
    preview_url: str
    preview_url_mime_type: str
    preview_width: int
    preview_height: int
    title_text: None
    max_title_num_of_lines: int
    max_subtitle_num_of_lines: int
    subtitle_text: None
    subtitle_decoration_type: int
    default_cta_type: None
    default_cta_title: None
    header_icon_url: str
    header_icon_mime_type: None
    header_icon_width: int
    header_icon_height: int
    header_title_text: None
    header_subtitle_text: None
    header_cta_type: None
    header_cta_title: None
    header_icon_layout_type: int
    header_icons_count: None
    caption_body_text: None
    group_name: None
    preview_media_fbid: int
    target_url: str
    ig_template_type: None
    playable_width: int
    playable_height: int
    playable_url: None
    video_codec: None
    video_dash_manifest: None
    playable_url_mime_type: None
    preview_url_info: PreviewUrlInfo
    header_icon_url_info: None
    header_icons_url_info: None
    playable_url_info: None
    favicon_url_info: None
    favicon_style: None
    favicons_url_info: None
    preview_image_decoration_type: int
    cta_buttons: list[CtaButtonsItem]
    is_quoted: bool
    is_borderless: None
    is_sharable: bool
    verified_type: int
    sticker_type: None
    doodle_space_height: None
    accessibility_summary_text: None
    accessibility_summary_hint: None
    collapsible_id: None
    countdown_timestamp_ms: None
    presence_source: None
    should_respect_server_preview_size: None
    accessory_preview_url_info: None
    accessory_playable_url_info: None
    playable_audio_url: None
    preview_icon_info: None
    quoted_attribution_text: None
    quoted_caption_body_text: None
    quoted_title_text: None
    quoted_favicon_url_info: None
    quoted_author_verified_type: None
    facepile_info: None
    should_refresh: bool
    audio_segment_start_time_ms: None
    audio_segment_duration_ms: None
    audio_filter: None
    preview_extra_urls_info: None
    preview_layout_type: int


class LastPermanentItem(TypedDict):
    item_id: str
    message_id: str
    user_id: int
    timestamp: int
    item_type: str
    client_context: str
    show_forward_attribution: bool
    forward_score: None
    is_shh_mode: bool
    otid: str
    is_ae_dual_send: bool
    is_ephemeral_exception: bool
    is_disappearing: bool
    is_superlative: bool
    paid_partnership_info: PaidPartnershipInfo
    is_replyable_in_bc: bool
    skip_bump_thread: bool
    can_have_attachment: bool
    is_cutout_sticker_creation_allowed: bool
    original_media_igid: int
    send_attribution: str
    is_sent_by_viewer: bool
    uq_seq_id: int
    latest_snooze_state: int
    one_click_upsell: None
    genai_params: Snippet
    system_folder: int
    auxiliary_text: str
    xma_reel_mention: list[XmaReelMentionItem]


class ThreadsItem(TypedDict):
    thread_id: str
    icebreakers: None
    icebreaker_suggestions: IcebreakerSuggestions
    snippet: Snippet
    dismiss_inbox_nudge: None
    should_upsell_nudge: bool
    public_chat_metadata: PublicChatMetadata
    is_creator_thread: bool
    is_business_thread: bool
    account_warning: None
    event_thread_metadata: None
    group_profile_id: None
    ctd_outcome_upsell_setting: None
    takedown_data: None
    is_xac_readonly: bool
    creator_agent_enabled: bool
    read_receipts_disabled: int
    unpublished_pro_page_id: None
    live_location_session_id: None
    is_pin: bool
    pinned_timestamp: None
    is_3p_api_user: bool
    typing_indicator_disabled: int
    locked_status: None
    notification_preview_controls: None
    customer_details: None
    recurring_prompt_type: None
    snoozed_messages_metadata: SnoozedMessagesMetadata
    is_verified_thread: bool
    last_mentioned_item_timestamp_us: None
    lightweight_intervention_appealable_entity_id: None
    nudge: Nudge
    nicknames: list[Any]
    nicknames_setting: list[NicknamesSettingItem]
    participant_requests_count: ParticipantRequestsCount
    is_open_group_invite_thread: bool
    scheduled_message_count: int
    must_show_in_thread_business_disclaimer: bool
    ai_agent_voice_calling_enabled: bool
    ai_agent_remixable: bool
    recent_creation_time: None
    should_show_safety_card: bool
    has_epd_restricted_user: bool
    is_new_friend_bump: None
    pinned_activity: None
    ai_agent_visibility_status: str
    hidden_chat_info: None
    is_group_readd_request: bool
    thread_title: str
    thread_label: int
    thread_languages: None
    is_group: bool
    is_spam: bool
    spam: bool
    users: list[UsersItem]
    shh_mode_enabled: bool
    canonical: bool
    relevancy_score: int
    relevancy_score_expr: int
    is_translation_enabled: bool
    last_activity_at: int
    last_non_sender_item_at: int
    marked_as_unread: bool
    approval_required_for_new_members: bool
    assigned_admin_id: int
    admin_user_ids: list[Any]
    ongoing_call_timestamp_ms: None
    pinned_messages_metadata: None
    ad_context_data: None
    dm_settings: None
    label_items: list[Any]
    shh_transport_mode: int
    shh_toggler_userid: None
    messaging_thread_key: int
    has_newer: bool
    has_older: bool
    next_cursor: str
    prev_cursor: str
    policy_violation: None
    theme: Theme
    thread_context_items: list[Any]
    professional_metadata: None
    pending: bool
    pending_user_ids: list[Any]
    last_seen_at: dict[str, LastSeenAtValue]
    smart_suggestion: None
    system_folder: int
    persistent_menu_icebreakers: None
    thread_has_audio_only_call: bool
    is_xac_thread: bool
    is_fanclub_subscriber_thread: bool
    inviter: UsersItem
    input_mode: int
    thread_v2_id: str
    has_reached_message_request_limit: bool
    last_mentioned_item_id: None
    thread_type: str
    thread_subtype: int
    btv_enabled_map: BtvEnabledMap
    translation_banner_impression_count: int
    read_state: int
    business_thread_folder: int
    is_creator_subscriber_thread: bool
    group_link_joinable_mode: int
    joinable_group_link: str
    folder: int
    encoded_server_data_info: str
    e2ee_cutover_status: int
    left_users: list[Any]
    is_appointment_booking_enabled: bool
    muted: bool
    mentions_muted: bool
    tq_seq_id: int
    named: bool
    is_close_friend_thread: bool
    vc_muted: bool
    uq_seq_id: int
    video_call_id: None
    viewer_id: int
    archived: bool
    bc_partnership: bool
    shh_replay_enabled: bool
    pals_feature_status: str
    has_shared_account_participant: bool
    other_participant_followers_10k_plus: bool
    other_participant_followers_100k_plus: bool
    other_participant_followers_1m_plus: bool
    is_top_account_thread: bool
    has_shared_account_participant_with_messaging_access: bool
    pending_users: list[Any]
    total_pending_users: int
    pending_user_expiration_timestamps: Snippet
    is_stale: bool
    ig_thread_capabilities: IgThreadCapabilities
    oldest_cursor: str
    newest_cursor: str
    last_permanent_item: LastPermanentItem
    items: list[LastPermanentItem]


class PrevCursor(TypedDict):
    cursor_thread_v2_id: int
    cursor_timestamp_seconds: int
    cursor_relevancy_score: int


class Inbox(TypedDict):
    threads: list[ThreadsItem]
    pinned_threads: list[Any]
    unseen_count: int
    unseen_count_ts: int
    prev_cursor: PrevCursor
    has_older: bool
    oldest_cursor: str
    next_cursor: PrevCursor
    blended_inbox_enabled: bool


class Viewer(TypedDict):
    strong_id__: str
    pk: int
    id: str
    fbid_v2: int
    interop_messaging_user_fbid: int
    account_badges: list[Any]
    is_verified: bool
    biz_user_inbox_state: int
    full_name: str
    username: str
    has_anonymous_profile_picture: bool
    is_private: bool
    wa_addressable: bool
    wa_eligibility: int
    pk_id: str
    profile_pic_url: str
    profile_pic_id: str
    has_encrypted_backup: bool


class DirectV2InboxResponse(TypedDict):
    inbox: Inbox
    viewer: Viewer
    seq_id: int
    snapshot_at_ms: int
    has_pending_top_requests: bool
    pending_requests_total: int
    unread_pending_requests: int
    status: str
    status_code: str
