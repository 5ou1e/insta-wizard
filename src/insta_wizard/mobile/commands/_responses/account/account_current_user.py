from __future__ import annotations

from typing import Any, TypedDict


class BiographyEntity(TypedDict, total=False):
    # structure in your sample is empty; keep flexible
    # add fields if you later see them
    pass


class BiographyWithEntities(TypedDict):
    raw_text: str
    entities: list[BiographyEntity]


class ImageInfo(TypedDict):
    height: int
    url: str
    width: int


class ProfilePicVersion(TypedDict):
    height: int
    url: str
    width: int


class ProfileEditField(TypedDict):
    confirmation_dialog_text: str
    disclaimer_text: str
    is_pending_review: bool
    should_show_confirmation_dialog: bool


class ProfileEditParams(TypedDict):
    full_name: ProfileEditField
    username: ProfileEditField


class SupervisionInfo(TypedDict):
    auto_approval_enabled: bool | None
    cannes_setting_badge_type: str | None
    daily_time_limit_without_extensions_seconds: int | None
    fc_url: str
    has_guardian: bool
    has_stated_age: bool
    is_blocked_list_enabled: bool
    is_daily_limit_non_blocking: bool | None
    is_eligible_for_supervision: bool
    is_guardian_of_viewer: bool
    is_guardian_user: bool
    is_modify_privacy_settings_enabled: bool
    is_quiet_time_feature_enabled: bool
    is_quiet_time_non_blocking: bool | None
    is_supervised_by_viewer: bool
    is_supervised_in_general_supervision_or_in_cooldown: bool
    is_supervised_or_in_cooldown: bool
    is_supervised_user: bool
    screen_time_daily_limit_description: str | None
    screen_time_daily_limit_seconds: int | None
    is_supervised_by_feta_viewer: bool
    is_feta_guardian_user: bool
    latest_valid_time_limit_extension_request: Any | None
    quiet_time_intervals: Any | None
    feature_controls: Any | None


class AccountCurrentUserResponseUser(TypedDict):
    strong_id__: str
    primary_profile_link_type: int
    show_fb_link_on_profile: bool
    show_fb_page_link_on_profile: bool
    can_hide_category: bool
    can_hide_public_contacts: bool
    account_type: int

    ads_page_id: int | None
    ads_page_name: str | None

    can_add_fb_group_link_on_profile: bool
    last_seen_timezone: str
    account_category: str
    allowed_commenter_type: str

    fbid_v2: int
    has_gen_ai_personas_for_profile_banner: bool
    is_coppa_enforced: bool
    is_muted_words_spamscam_enabled: bool
    has_nme_badge: bool

    pk: int
    pk_id: str
    reel_auto_archive: str
    id: str

    biography: str
    biography_with_entities: BiographyWithEntities
    can_link_entities_in_bio: bool
    external_url: str
    has_biography_translation: bool

    category: str
    should_show_category: bool
    category_id: str
    is_category_tappable: bool
    should_show_public_contacts: bool

    is_eligible_for_smb_support_flow: bool
    is_eligible_for_lead_center: bool
    lead_details_app_id: str

    is_business: bool
    professional_conversion_suggested_account_type: int
    direct_messaging: str

    fb_page_call_to_action_id: str
    can_claim_page: bool
    can_crosspost_without_fb_token: bool

    instagram_location_id: str
    address_street: str
    business_contact_method: str
    city_id: str
    city_name: str
    contact_phone_number: str
    is_profile_audio_call_enabled: bool
    latitude: float
    longitude: float

    public_email: str
    public_phone_country_code: str
    public_phone_number: str
    zip: str

    displayed_action_button_partner: Any | None
    smb_delivery_partner: Any | None
    smb_support_delivery_partner: Any | None
    displayed_action_button_type: Any | None
    smb_support_partner: Any | None

    is_call_to_action_enabled: bool
    num_of_admined_pages: int
    page_id: int
    page_name: str

    bio_links: list[Any]
    is_quiet_mode_enabled: bool
    account_badges: list[Any]

    birthday: str
    birthday_today_visibility_for_viewer: str
    custom_gender: str
    enable_add_school_in_edit_profile: bool
    email: str
    gender: int

    has_anonymous_profile_picture: bool
    hd_profile_pic_url_info: ImageInfo
    hd_profile_pic_versions: list[ProfilePicVersion]

    interop_messaging_user_fbid: int

    is_daily_limit_blocking: bool
    is_hide_more_comment_enabled: bool
    is_muted_words_custom_enabled: bool
    is_muted_words_global_enabled: bool
    is_mv4b_biz_asset_profile_locked: bool

    has_legacy_bb_pending_profile_picture_update: bool
    text_app_should_see_autoimported_ig_profile_picture_dialog: bool
    has_mv4b_pending_profile_picture_update: bool
    is_mv4b_max_profile_edit_reached: bool
    is_mv4b_application_matured_for_profile_edit: bool
    is_profile_wa_calling_enabled: bool
    is_showing_birthday_selfie: bool
    is_supervision_features_enabled: bool
    is_verified: bool
    has_active_mv4b_application: bool

    phone_number: str
    profile_pic_id: str
    profile_pic_url: str

    profile_edit_params: ProfileEditParams
    pronouns: list[Any]

    show_conversion_edit_entry: bool
    show_schools_badge: Any | None
    show_teen_education_banner: bool

    supervision_info: SupervisionInfo

    trusted_username: str
    trust_days: int
    username: str

    text_app_cover_photo_url: str | None
    wa_calling_option_for_wa_linked: int
    wa_calling_option_for_legacy_num: int
    full_name: str
    is_private: bool


class AccountCurrentUserResponse(TypedDict):
    user: AccountCurrentUserResponseUser
    status: str
