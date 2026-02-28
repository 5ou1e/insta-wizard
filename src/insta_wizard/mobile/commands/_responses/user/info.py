from typing import TypedDict, Any


class _SupervisionInfo(TypedDict):
    auto_approval_enabled: None
    cannes_setting_badge_type: None
    daily_time_limit_without_extensions_seconds: None
    fc_url: str
    has_guardian: bool
    has_stated_age: bool
    is_blocked_list_enabled: bool
    is_daily_limit_non_blocking: None
    is_eligible_for_supervision: bool
    is_guardian_of_viewer: bool
    is_guardian_user: bool
    is_modify_privacy_settings_enabled: bool
    is_quiet_time_feature_enabled: bool
    is_quiet_time_non_blocking: None
    is_supervised_by_viewer: bool
    is_supervised_in_general_supervision_or_in_cooldown: bool
    is_supervised_or_in_cooldown: bool
    is_supervised_user: bool
    screen_time_daily_limit_description: None
    screen_time_daily_limit_seconds: None
    is_supervised_by_feta_viewer: bool
    is_feta_guardian_user: bool
    latest_valid_time_limit_extension_request: None
    quiet_time_intervals: None
    feature_controls: None


class _FanClubInfo(TypedDict):
    autosave_to_exclusive_highlight: None
    connected_member_count: None
    fan_club_id: None
    fan_club_name: None
    has_created_ssc: None
    has_enough_subscribers_for_ssc: None
    is_fan_club_gifting_eligible: None
    is_fan_club_referral_eligible: None
    is_free_trial_eligible: None
    largest_public_bc_id: None
    subscriber_count: None
    should_show_playlists_in_profile_tab: None
    fan_consideration_page_revamp_eligiblity: None


class _HdProfilePicUrlInfo(TypedDict):
    height: int
    url: str
    width: int


class _MetaVerifiedBenefitsInfo(TypedDict):
    active_meta_verified_benefits: list[Any]
    is_eligible_for_meta_verified_content_protection: bool
    is_eligible_for_ig_meta_verified_label: bool


class _BiographyWithEntities(TypedDict):
    raw_text: str
    entities: list[Any]


class _RingCreatorMetadata(TypedDict):
    pass


class _ActiveStandaloneFundraisers(TypedDict):
    total_count: int
    fundraisers: list[Any]


class _AvatarStatus(TypedDict):
    has_avatar: bool


class _CreatorShoppingInfo(TypedDict):
    linked_merchant_accounts: list[Any]


class _ProfileOverlayInfo(TypedDict):
    overlay_format: str
    bloks_payload: None


class _AvailableThemeColorsItem(TypedDict):
    display_label: str
    int_value: int


class _ThemeColor(TypedDict):
    available_theme_colors: list[_AvailableThemeColorsItem]
    selected_theme_color: _AvailableThemeColorsItem


class _Nametag(TypedDict):
    available_theme_colors: list[int]
    background_image_url: str
    emoji: str
    emoji_color: int
    gradient: int
    is_background_image_blurred: bool
    mode: int
    selected_theme_color: int
    selfie_sticker: int
    selfie_url: str
    theme_color: _ThemeColor


class _NotMetaVerifiedFrictionInfo(TypedDict):
    label_friction_content: str
    is_eligible_for_label_friction: bool


class _PinnedChannelsInfo(TypedDict):
    has_public_channels: bool
    pinned_channels_list: list[Any]


class _TranslateFromPreferenceItem(TypedDict):
    language: str
    enabled: bool


class _User(TypedDict):
    strong_id__: str
    fbid_v2: int
    full_name: str
    pk_id: str
    pk: int
    allowed_commenter_type: str
    eligible_for_text_app_activation_badge: bool
    feed_post_reshare_disabled: bool
    has_ever_selected_topics: bool
    has_nme_badge: bool
    is_muted_words_spamscam_enabled: bool
    reel_auto_archive: str
    show_insights_terms: bool
    third_party_downloads_enabled: int
    can_follow_hashtag: bool
    can_see_support_inbox: bool
    show_fb_link_on_profile: bool
    show_fb_page_link_on_profile: bool
    show_wa_link_on_profile: bool
    can_hide_category: bool
    break_reminder_interval: int
    can_hide_public_contacts: bool
    existing_user_age_collection_enabled: bool
    has_public_tab_threads: bool
    has_user_ever_set_break: bool
    is_eligible_for_meta_verified_label: bool
    is_opal_enabled: bool
    is_parenting_account: bool
    last_seen_timezone: str
    primary_profile_link_type: int
    show_post_insights_entry_point: bool
    is_recon_ad_cta_on_profile_eligible_with_viewer: bool
    account_type: int
    highlights_tray_type: str
    current_catalog_id: None
    mini_shop_seller_onboarding_status: None
    ads_incentive_expiration_date: None
    ads_page_id: None
    ads_page_name: None
    about_your_account_bloks_entrypoint_enabled: bool
    account_category: str
    aggregate_promote_engagement: bool
    can_add_fb_group_link_on_profile: bool
    can_use_affiliate_partnership_messaging_as_creator: bool
    can_use_affiliate_partnership_messaging_as_brand: bool
    has_gen_ai_personas_for_profile_banner: bool
    has_guides: bool
    highlight_reshare_disabled: bool
    include_direct_blacklist_status: bool
    is_direct_roll_call_enabled: bool
    is_eligible_for_meta_verified_links_in_reels: bool
    is_eligible_for_post_boost_mv_upsell: bool
    is_meta_verified_related_accounts_display_enabled: bool
    is_new_to_instagram: bool
    is_new_to_instagram_30d: bool
    is_profile_broadcast_sharing_enabled: bool
    is_secondary_account_creation: bool
    profile_type: int
    usertag_review_enabled: bool
    is_coppa_enforced: bool
    is_auto_confirm_enabled_for_all_reciprocal_follow_requests: bool
    views_on_grid_status: str
    id: str
    supervision_info: _SupervisionInfo
    latest_reel_media: int
    latest_besties_reel_media: int
    is_ring_creator: bool
    has_onboarded_to_text_post_app: bool
    account_badges: list[Any]
    has_highlight_reels: bool
    is_creator_agent_enabled: bool
    is_private: bool
    interop_messaging_user_fbid: int
    is_verified: bool
    profile_pic_id: str
    has_anonymous_profile_picture: bool
    profile_pic_url: str
    username: str
    can_boost_post: bool
    can_see_organic_insights: bool
    fan_club_info: _FanClubInfo
    has_private_collections: bool
    hd_profile_pic_url_info: _HdProfilePicUrlInfo
    hd_profile_pic_versions: list[_HdProfilePicUrlInfo]
    is_active_on_text_post_app: bool
    is_cannes: bool
    is_facebook_onboarded_charity: bool
    show_account_transparency_details: bool
    transparency_product_enabled: bool
    text_app_last_visited_time: None
    follower_count: int
    following_count: int
    has_fan_club_subscriptions: bool
    is_api_user: bool
    is_eligible_for_slide: bool
    meta_verified_benefits_info: _MetaVerifiedBenefitsInfo
    page_id: None
    besties_count: int
    biography: str
    biography_with_entities: _BiographyWithEntities
    can_link_entities_in_bio: bool
    daily_time_limit: int
    has_disallowed_media_notes_reshare: bool
    has_music_on_profile: bool
    has_videos: bool
    has_views_fetching: bool
    is_call_to_action_enabled: None
    is_category_tappable: bool
    is_eligible_for_creator_product_links: bool
    is_eligible_for_schools_search_upsell: bool
    is_hiding_stories_from_someone: bool
    is_muted_words_custom_enabled: bool
    is_needy: bool
    is_pause_push_notifications_enabled: bool
    limited_interactions_enabled: bool
    num_of_admined_pages: None
    page_name: None
    professional_conversion_suggested_account_type: int
    show_besties_badge: bool
    smb_support_partner: None
    ring_creator_metadata: _RingCreatorMetadata
    is_onboarding_account: bool
    is_business: bool
    is_prime_onboarding_account: bool
    is_profile_picture_expansion_enabled: bool
    linked_fb_info: _RingCreatorMetadata
    show_all_highlights_as_selected_in_management_screen: bool
    show_schools_badge: None
    trial_clips_enabled: bool
    enable_add_school_in_edit_profile: bool
    eligible_shopping_signup_entrypoints: list[Any]
    is_igd_product_picker_enabled: bool
    eligible_shopping_formats: list[Any]
    is_shopping_settings_enabled: bool
    is_shopping_community_content_enabled: bool
    is_shopping_auto_highlight_eligible: bool
    is_shopping_catalog_source_selection_enabled: bool
    shopping_post_onboard_nux_type: None
    displayed_action_button_partner: None
    smb_delivery_partner: None
    smb_support_delivery_partner: None
    displayed_action_button_type: None
    category: None
    external_url: str
    has_biography_translation: bool
    active_standalone_fundraisers: _ActiveStandaloneFundraisers
    additional_business_addresses: list[Any]
    allow_automatic_previews_setting: bool
    allow_manage_memorialization: bool
    allow_mention_setting: str
    allow_tag_setting: str
    audio_go_dark_events: list[Any]
    auto_expand_chaining: bool
    avatar_status: _AvatarStatus
    bio_links: list[Any]
    can_be_tagged_as_sponsor: bool
    can_convert_to_business: bool
    can_create_new_standalone_fundraiser: bool
    can_create_new_standalone_personal_fundraiser: bool
    can_create_sponsor_tags: bool
    can_tag_products_from_merchants: bool
    can_see_support_inbox_v1: bool
    can_use_branded_content_discovery_as_brand: bool
    can_use_branded_content_discovery_as_creator: bool
    can_use_paid_partnership_messaging_as_creator: bool
    chaining_upsell_cards: list[Any]
    creator_shopping_info: _CreatorShoppingInfo
    follow_friction_type: int
    has_chaining: bool
    has_collab_collections: bool
    has_exclusive_feed_content: bool
    has_ig_reposts_enabled: bool
    has_legacy_bb_pending_profile_picture_update: bool
    has_mv4b_pending_profile_picture_update: bool
    has_onboarded_to_basel: bool
    has_placed_orders: bool
    has_saved_items: bool
    hide_trials_from_profile_enabled: bool
    hide_like_and_view_counts: bool
    instagram_pk: str
    is_allowed_to_create_standalone_nonprofit_fundraisers: bool
    is_profile_search_enabled: bool
    is_eligible_for_meta_verified_links_in_post: bool
    is_eligible_for_meta_verified_enhanced_link_sheet: bool
    is_eligible_for_meta_verified_enhanced_link_sheet_consumption: bool
    is_eligible_for_meta_verified_multiple_addresses_creation: bool
    is_eligible_for_meta_verified_multiple_addresses_consumption: bool
    is_eligible_for_meta_verified_related_accounts: bool
    is_mv4b_application_matured_for_profile_edit: bool
    is_mv4b_biz_asset_profile_locked: bool
    is_mv4b_max_profile_edit_reached: bool
    meta_verified_related_accounts_count: int
    is_eligible_to_show_fb_cross_sharing_nux: bool
    is_hide_more_comment_enabled: bool
    is_in_canada: bool
    is_interest_account: bool
    is_memorialized: bool
    is_muted_words_global_enabled: bool
    is_aggregated_time_tracking_enabled: bool
    is_potential_business: bool
    is_regulated_news_in_viewer_location: bool
    is_remix_setting_enabled_for_posts: bool
    is_remix_setting_enabled_for_reels: bool
    is_profile_action_needed: bool
    is_quiet_mode_enabled: bool
    is_regulated_c18: bool
    profile_overlay_info: _ProfileOverlayInfo
    is_stories_teaser_muted: bool
    is_tooltip_disabled_param: bool
    is_supervision_features_enabled: bool
    is_whatsapp_linked: bool
    is_vowel_eligible: bool
    media_count: int
    nametag: _Nametag
    not_meta_verified_friction_info: _NotMetaVerifiedFrictionInfo
    open_external_url_with_in_app_browser: bool
    pinned_channels_info: _PinnedChannelsInfo
    profile_pic_genai_tool_info: list[Any]
    pronouns: list[Any]
    relevant_news_regulation_locations: list[Any]
    request_contact_enabled: bool
    show_blue_badge_on_main_profile: bool
    show_conversion_edit_entry: bool
    disable_profile_shop_cta: bool
    show_text_post_app_badge: bool
    spam_follower_setting_enabled: bool
    total_ar_effects: int
    total_clips_count: int
    upcoming_events: list[Any]
    whatsapp_number: str
    adjusted_banners_order: list[Any]
    has_visible_media_notes: bool
    is_open_to_collab: bool
    is_daily_limit_blocking: bool
    ig_text_post_app_onboarding_default_privacy: str
    threads_profile_glyph_url: str
    is_oregon_custom_gender_consented: bool
    translate_from_preference: list[_TranslateFromPreferenceItem]
    is_force_migrated_h2g: bool
    profile_reels_sorting_eligibility: str
    nonpro_can_maybe_see_profile_hypercard: bool
    should_show_tagged_tab: bool
    birthday_today_visibility_for_viewer: str
    is_eligible_for_meta_verified_ig_self_profile_not_verified_badge: bool
    is_guardian_r_account_cannes_pair: bool
    short_drama_creator: None
    moonshot_joiner_number: None
    qa_freeform_banner: None
    qa_freeform_banner_available_prompts: list[Any]


class UserInfoResponse(TypedDict):
    user: _User
    status: str
