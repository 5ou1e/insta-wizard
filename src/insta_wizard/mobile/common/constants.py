BASE_INSTAGRAM_URL = "https://i.instagram.com"
BASE_INSTAGRAM_API_URL = BASE_INSTAGRAM_URL + "/api"
INSTAGRAM_API_V1_URL = BASE_INSTAGRAM_API_URL + "/v1"

BASE_INSTAGRAM_B_URL = "https://b.i.instagram.com"
BASE_INSTAGRAM_API_B_URL = BASE_INSTAGRAM_B_URL + "/api"
INSTAGRAM_API_B_V1_URL = BASE_INSTAGRAM_API_B_URL + "/v1"

GRAPHQL_QUERY_URL = "https://i.instagram.com/graphql/query"
GRAPHQL_WWW_URL = "https://i.instagram.com/graphql_www"

RUPLOAD_IGPHOTO_URL = "https://i.instagram.com/rupload_igphoto/{name}"


BLOKS_SEND_LOGIN_REQUEST_URI = (
    "bloks/async_action/com.bloks.www.bloks.caa.login.async.send_login_request/"
)
BLOKS_PROCESS_CLIENT_DATA_AND_REDIRECT_URI = (
    "bloks/async_action/com.bloks.www.bloks.caa.login.process_client_data_and_redirect/"
)
BLOKS_YOUTH_REGULATION_DELETE_PREGENT_URI = (
    "bloks/async_action/com.bloks.www.bloks.caa.reg.youthregulation.deletepregent.async/"
)
BLOKS_PHONE_NUMBER_PREFILL_ASYNC_URI = (
    "bloks/async_action/com.bloks.www.bloks.caa.phone.number.prefill.async.controller/"
)
BLOKS_LOGIN_SAVE_CREDENTIALS_URI = "bloks/apps/com.bloks.www.caa.login.save-credentials/"
BLOKS_REG_AYMH_CREATE_ACCOUNT_BUTTON_ASYNC = (
    "bloks/async_action/com.bloks.www.bloks.caa.reg.aymh_create_account_button.async/"
)
BLOKS_REG_CONTACTPOINT_PHONE = "bloks/apps/com.bloks.www.bloks.caa.reg.contactpoint_phone/"
BLOKS_REG_CONFIRMATION_MO_SMS_FALLBACK_ASYNC_URI = (
    "bloks/async_action/com.bloks.www.bloks.caa.reg.confirmation.mo_sms_fallback.async/"
)
BLOKS_REG_CONTACTPOINT_PHONE_ASYNC = (
    "bloks/async_action/com.bloks.www.bloks.caa.reg.async.contactpoint_phone.async/"
)
BLOKS_REG_SEND_CONFIRMATION_ASYNC = (
    "bloks/async_action/com.bloks.www.bloks.caa.reg.send_confirmation.async/"
)
BLOKS_REG_CONFIRMATION_ASYNC = "bloks/async_action/com.bloks.www.bloks.caa.reg.confirmation.async/"
BLOKS_APPS_REG_CONFIRMATION = "bloks/apps/com.bloks.www.bloks.caa.reg.confirmation/"
BLOKS_APPS_REG_CONFIRMATION_MEDIUM_SELECTION_ASYNC_URI = "bloks/async_action/com.bloks.www.bloks.caa.reg.confirmation.medium_selection.async/"
BLOKS_REG_PASSWORD_ASYNC = "bloks/async_action/com.bloks.www.bloks.caa.reg.password.async/"
BLOKS_REG_BIRTHDAY_ASYNC = "bloks/async_action/com.bloks.www.bloks.caa.reg.birthday.async/"
BLOKS_REG_NAME_IG_ASYNC = "bloks/async_action/com.bloks.www.bloks.caa.reg.name_ig.async/"
BLOKS_REG_NAME_IG_AND_SOAP_ASYNC = (
    "bloks/async_action/com.bloks.www.bloks.caa.reg.name_ig_and_soap.async/"
)
BLOKS_REG_USERNAME_ASYNC = "bloks/async_action/com.bloks.www.bloks.caa.reg.username.async/"
BLOKS_REG_CREATE_ACCOUNT_ASYNC = (
    "bloks/async_action/com.bloks.www.bloks.caa.reg.create.account.async/"
)
BLOKS_APPS_REG_CONFIRMATION_IG_BOTTOMSHEET = (
    "bloks/apps/com.bloks.www.bloks.caa.reg.confirmation.ig.bottomsheet/"
)
BLOKS_REG_CONFIRMATION_IG_BOTTOMSHEET_ASYNC = (
    "bloks/async_action/com.bloks.www.bloks.caa.reg.confirmation.ig.bottomsheet.async/"
)


ACCOUNTS_CURRENT_USER_URI = "accounts/current_user/"
ACCOUNTS_EDIT_PROFILE_URI = "accounts/edit_profile/"
ACCOUNTS_UPDATE_PROFILE_NAME_URI = "accounts/update_profile_name/"
ACCOUNTS_SET_BIOGRAPHY_URI = "accounts/set_biography/"
ACCOUNTS_CHANGE_PROFILE_PICTURE_URI = "accounts/change_profile_picture/"
ACCOUNTS_GET_PRESENCE_DISABLED_URI = "accounts/get_presence_disabled/"
ACCOUNTS_LOGIN_URI = "accounts/login/"
ACCOUNTS_CHECK_PHONE_NUMBER_URI = "accounts/check_phone_number/"
ACCOUNTS_SEND_SIGNUP_SMS_CODE_URI = "accounts/send_signup_sms_code/"
ACCOUNTS_VALIDATE_SIGNUP_SMS_CODE_URI = "accounts/validate_signup_sms_code/"
ACCOUNTS_USERNAME_SUGGESTIONS_URI = "accounts/username_suggestions/"
ACCOUNTS_CREATE_VALIDATED_URI = "accounts/create_validated/"
ACCOUNTS_SECURITY_INFO_URI = "accounts/account_security_info/"
ACCOUNTS_SEND_CONFIRM_EMAIL_URI = "accounts/send_confirm_email/"
ACCOUNTS_SEND_CONFIRM_PHONE_NUMBER_URI = "accounts/initiate_phone_number_confirmation/"


ANDROID_MODULES_DOWNLOAD_URI = "android_modules/download/"

ATTESTATION_CREATE_ANDROID_KEYSTORE_URI = "attestation/create_android_keystore/"
ATTESTATION_CREATE_ANDROID_PLAYINTEGRITY_URI = "attestation/create_android_playintegrity/"

BANYAN_BANYAN_URI = "banyan/banyan/"

CLIPS_DISCOVER_STREAM_URI = "clips/discover/stream/"
CLIPS_USER_SHARE_TO_FB_CONFIG_URI = "clips/user/share_to_fb_config/"

CONSENT_GET_SIGNUP_CONFIG_URI = "consent/get_signup_config/"

CREATIVES_WRITE_SUPPORTED_CAPABILITIES_URI = "creatives/write_supported_capabilities/"

DIRECT_V2_GET_PRESENCE_URI = "direct_v2/get_presence/"
DIRECT_V2_GET_PRESENCE_ACTIVE_NOW_URI = "direct_v2/get_presence_active_now/"
DIRECT_V2_GET_PENDING_REQUESTS_PREVIEW_URI = "direct_v2/async_get_pending_requests_preview/"
DIRECT_V2_INBOX_URI = "direct_v2/inbox/"

DIRECT_V2_HAS_INTEROP_UPGRADED = "direct_v2/has_interop_upgraded/"
DIRECT_V2_ASYNC_GET_PENDING_REQUESTS_PREVIEW_URI = "direct_v2/async_get_pending_requests_preview/"
DIRECT_V2_GET_RANKED_RECIPIENTS_URI = "direct_v2/ranked_recipients/"
DIRECT_V2_GET_CREATE_GROUP_THREAD_URI = "direct_v2/create_group_thread/"
DIRECT_V2_GET_THREADS_APPROVE_URI = "direct_v2/threads/{thread_id}/approve/"
DIRECT_V2_GET_THREADS_APPROVE_MULTIPLE_URI = "direct_v2/threads/approve_multiple/"
DIRECT_V2_GET_THREADS_DECLINE_URI = "direct_v2/threads/{thread_id}/decline/"
DIRECT_V2_GET_THREADS_DECLINE_MULTIPLE_URI = "direct_v2/threads/decline_multiple/"
DIRECT_V2_GET_THREADS_DECLINE_ALL_URI = "direct_v2/threads/decline_all/"
DIRECT_V2_THREADS_ITEMS_DELETE_URI = "direct_v2/threads/{thread_id}/items/{item_id}/delete/"
DIRECT_V2_THREADS_DELETE_ITEMS_LOCALLY_URI = "direct_v2/threads/{thread_id}/delete_items_locally/"
DIRECT_V2_THREADS_ITEMS_SEEN_URI = "direct_v2/threads/{thread_id}/items/{item_id}/seen/"
DIRECT_V2_THREADS_HIDE_URI = "direct_v2/threads/{thread_id}/hide/"
DIRECT_V2_THREADS_LEAVE_URI = "direct_v2/threads/{thread_id}/leave/"
DIRECT_V2_THREADS_ADD_USER_URI = "direct_v2/threads/{thread_id}/add_user/"
DIRECT_V2_THREADS_UPDATE_TITLE_URI = "direct_v2/threads/{thread_id}/update_title/"
DIRECT_V2_THREADS_MUTE_URI = "direct_v2/threads/{thread_id}/mute/"
DIRECT_V2_THREADS_UNMUTE_URI = "direct_v2/threads/{thread_id}/unmute/"
DIRECT_V2_THREADS_BROADCAST_REACTION_URI = "direct_v2/threads/broadcast/reaction/"
DIRECT_V2_THREADS_BROADCAST_TEXT_URI = "direct_v2/threads/broadcast/text/"

FEED_TIMELINE_URI = "feed/timeline/"
FEED_REELS_TRAY_URI = "feed/reels_tray/"
FEED_INJECTED_REELS_MEDIA_URI = "feed/injected_reels_media/"

FRIENDSHIPS_CREATE_URI = "friendships/create/{user_id}/"
FRIENDSHIPS_DESTROY_URI = "friendships/destroy/{user_id}/"
FRIENDSHIPS_REMOVE_FOLLOWER_URI = "friendships/remove_follower/{user_id}/"
FRIENDSHIPS_USER_FOLLOWERS_URI = "friendships/{user_id}/followers/"
FRIENDSHIPS_USER_FOLLOWING_URI = "friendships/{user_id}/following/"
FRIENDSHIPS_SHOW_URI = "friendships/show/{user_id}/"
FRIENDSHIPS_SHOW_MANY_URI = "friendships/show_many/"
LAUNCHER_MOBILE_CONFIG_URI = "launcher/mobileconfig/"

LIVE_GET_GOOD_TIME_FOR_LIVE_URI = "live/get_good_time_for_live/"

LOOM_FETCH_CONFIG_URI = "loom/fetch_config/"

MEDIA_BLOCKED_URI = "media/blocked/"
MEDIA_COMMENTS_URI = "media/{media_id}/comments/"
MEDIA_COMMENT_URI = "media/{media_id}/comment/"
MEDIA_COMMENT_LIKE_URI = "media/{comment_id}/comment_like/"
MEDIA_COMMENT_UNLIKE_URI = "media/{comment_id}/comment_unlike/"

MULTIPLE_ACCOUNTS_GET_ACCOUNT_FAMILY_URI = "multiple_accounts/get_account_family/"

NEWS_INBOX_URI = "news/inbox/"

NOTIFICATIONS_GET_NOTIFICATION_SETTINGS_URI = "notifications/get_notification_settings/"
NOTIFICATIONS_BADGE_URI = "notifications/badge/"

USERS_USER_INFO_URI = "users/{user_id}/info/"
USERS_USERNAME_INFO_URI = "users/{username}/usernameinfo/"
USERS_SEARCH_URI = "users/search/"
USERS_ACCOUNT_DETAILS_URI = "users/{user_id}/account_details/"
USERS_WEB_PROFILE_INFO = "users/web_profile_info/"
USERS_CHECK_USERNAME = "users/check_username/"

USERS_GET_LIMITED_INTERACTIONS_REMINDER_URI = "users/get_limited_interactions_reminder/"

ZR_DUAL_TOKENS_URI = "zr/dual_tokens/"
