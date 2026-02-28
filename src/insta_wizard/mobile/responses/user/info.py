from typing import Any, TypedDict


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


class _RecsFromFriends(TypedDict):
    enable_recs_from_friends: bool
    recs_from_friends_entry_point_type: str


class _MetaVerifiedBenefitsInfo(TypedDict):
    active_meta_verified_benefits: list[Any]
    is_eligible_for_meta_verified_content_protection: bool
    is_eligible_for_ig_meta_verified_label: bool


class _User(TypedDict):
    strong_id__: str
    fbid_v2: int
    pk_id: str
    pk: int
    eligible_for_text_app_activation_badge: bool
    feed_post_reshare_disabled: bool
    has_ever_selected_topics: bool
    has_nme_badge: bool
    third_party_downloads_enabled: int
    show_fb_link_on_profile: bool
    show_fb_page_link_on_profile: bool
    can_hide_category: bool
    can_hide_public_contacts: bool
    is_opal_enabled: bool
    primary_profile_link_type: int
    is_recon_ad_cta_on_profile_eligible_with_viewer: bool
    account_type: int
    highlights_tray_type: str
    current_catalog_id: None
    mini_shop_seller_onboarding_status: None
    ads_incentive_expiration_date: None
    ads_page_id: None
    ads_page_name: None
    account_category: str
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
    is_profile_broadcast_sharing_enabled: bool
    is_secondary_account_creation: bool
    profile_type: int
    is_coppa_enforced: bool
    is_auto_confirm_enabled_for_all_reciprocal_follow_requests: bool
    views_on_grid_status: str
    id: str
    is_bestie: bool
    latest_reel_media: int
    latest_besties_reel_media: int
    is_ring_creator: bool
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
    full_name: str
    fan_club_info: _FanClubInfo
    hd_profile_pic_url_info: _HdProfilePicUrlInfo
    hd_profile_pic_versions: list[_HdProfilePicUrlInfo]
    is_active_on_text_post_app: bool
    is_cannes: bool
    is_facebook_onboarded_charity: bool
    is_favorite: bool
    show_account_transparency_details: bool
    transparency_product_enabled: bool
    text_app_last_visited_time: None
    follower_count: int
    following_count: int
    is_eligible_for_slide: bool
    live_subscription_status: str
    page_id: None
    biography: str
    biography_with_entities: _BiographyWithEntities
    has_music_on_profile: bool
    has_videos: bool
    has_views_fetching: bool
    is_call_to_action_enabled: None
    is_category_tappable: bool
    is_eligible_for_creator_product_links: bool
    is_eligible_for_schools_search_upsell: bool
    num_of_admined_pages: None
    page_name: None
    professional_conversion_suggested_account_type: int
    profile_context: str
    smb_support_partner: None
    ring_creator_metadata: _RingCreatorMetadata
    is_onboarding_account: bool
    is_business: bool
    is_prime_onboarding_account: bool
    is_profile_picture_expansion_enabled: bool
    show_all_highlights_as_selected_in_management_screen: bool
    show_schools_badge: None
    trial_clips_enabled: bool
    enable_add_school_in_edit_profile: bool
    shopping_post_onboard_nux_type: None
    displayed_action_button_partner: None
    smb_delivery_partner: None
    smb_support_delivery_partner: None
    displayed_action_button_type: None
    category: None
    external_url: str
    active_standalone_fundraisers: _ActiveStandaloneFundraisers
    additional_business_addresses: list[Any]
    allow_manage_memorialization: bool
    auto_expand_chaining: bool
    avatar_status: _AvatarStatus
    bio_links: list[Any]
    can_use_branded_content_discovery_as_brand: bool
    can_use_branded_content_discovery_as_creator: bool
    can_use_paid_partnership_messaging_as_creator: bool
    chaining_upsell_cards: list[Any]
    creator_shopping_info: _CreatorShoppingInfo
    follow_friction_type: int
    has_chaining: bool
    has_collab_collections: bool
    has_exclusive_feed_content: bool
    instagram_pk: str
    is_profile_search_enabled: bool
    is_eligible_for_meta_verified_links_in_post: bool
    is_eligible_for_meta_verified_enhanced_link_sheet: bool
    is_eligible_for_meta_verified_enhanced_link_sheet_consumption: bool
    is_eligible_for_meta_verified_multiple_addresses_creation: bool
    is_eligible_for_meta_verified_multiple_addresses_consumption: bool
    is_eligible_for_meta_verified_related_accounts: bool
    meta_verified_related_accounts_count: int
    is_favorite_for_clips: bool
    is_favorite_for_highlights: bool
    is_in_canada: bool
    is_interest_account: bool
    is_memorialized: bool
    is_potential_business: bool
    is_regulated_news_in_viewer_location: bool
    is_remix_setting_enabled_for_posts: bool
    is_remix_setting_enabled_for_reels: bool
    is_regulated_c18: bool
    profile_overlay_info: _ProfileOverlayInfo
    is_stories_teaser_muted: bool
    is_supervision_features_enabled: bool
    is_whatsapp_linked: bool
    media_count: int
    mutual_followers_count: int
    nametag: _Nametag
    not_meta_verified_friction_info: _NotMetaVerifiedFrictionInfo
    open_external_url_with_in_app_browser: bool
    pinned_channels_info: _PinnedChannelsInfo
    profile_context_facepile_users: list[Any]
    profile_context_links_with_user_ids: list[Any]
    profile_pic_genai_tool_info: list[Any]
    pronouns: list[Any]
    relevant_news_regulation_locations: list[Any]
    remove_message_entrypoint: bool
    request_contact_enabled: bool
    show_blue_badge_on_main_profile: bool
    disable_profile_shop_cta: bool
    show_text_post_app_badge: bool
    spam_follower_setting_enabled: bool
    total_ar_effects: int
    upcoming_events: list[Any]
    recs_from_friends: _RecsFromFriends
    adjusted_banners_order: list[Any]
    has_visible_media_notes: bool
    is_open_to_collab: bool
    is_daily_limit_blocking: bool
    threads_profile_glyph_url: str
    is_oregon_custom_gender_consented: bool
    profile_reels_sorting_eligibility: str
    nonpro_can_maybe_see_profile_hypercard: bool
    should_show_tagged_tab: bool
    posts_subscription_status: str
    reels_subscription_status: str
    stories_subscription_status: str
    birthday_today_visibility_for_viewer: str
    is_eligible_for_meta_verified_ig_self_profile_not_verified_badge: bool
    has_private_collections: bool
    is_guardian_r_account_cannes_pair: bool
    has_fan_club_subscriptions: bool
    show_wa_link_on_profile: bool
    meta_verified_benefits_info: _MetaVerifiedBenefitsInfo
    existing_user_age_collection_enabled: bool
    has_public_tab_threads: bool
    is_eligible_for_meta_verified_label: bool
    is_favorite_for_stories: bool
    is_parenting_account: bool
    show_post_insights_entry_point: bool
    short_drama_creator: None
    moonshot_joiner_number: None
    school_affiliated_account_viewer_status: None
    qa_freeform_banner: None
    qa_freeform_banner_available_prompts: list[Any]


class UserInfoResponse(TypedDict):
    user: _User
    status: str
