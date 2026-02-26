import re

WWW_INSTAGRAM_URL = "https://www.instagram.com/"

WBLOKS_FETCH_URL = "https://www.instagram.com/async/wbloks/fetch/"
SHARED_DATA_URL = "https://www.instagram.com/data/shared_data/"
WEB_MID_URL = "https://www.instagram.com/web/__mid/"
SUSPENDED_URL = "https://www.instagram.com/accounts/suspended/"
BLOKS_ACCOUNT_SECURITY_PASSWORD_RESET_SUBMIT_ACTION_HANDLER_URL = "https://www.instagram.com/api/v1/bloks/apps/com.instagram.account_security.password_reset_submit_action_handler/"
WEB_ACCOUNTS_LOGIN_AJAX_URL = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
WEB_ACCOUNTS_LOGOUT_AJAX_URL = "https://www.instagram.com/api/v1/web/accounts/logout/ajax/"
ACCOUNT_RECOVERY_SEND_AJAX_URL = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
ACCOUNTS_EDIT_WEB_FORM_DATA_URL = "https://www.instagram.com/api/v1/accounts/edit/web_form_data/"
ACCOUNTS_EDIT_URL = "https://www.instagram.com/api/v1/web/accounts/edit/"

WEB_CONSENT_CHECK_AGE_ELIGIBILITY = (
    "https://www.instagram.com/api/v1/web/consent/check_age_eligibility/"
)
WEB_API_GRAPHQL_URL = "https://www.instagram.com/api/graphql"
BLOKS_NAVIGATION_TAKE_CHALLENGE_URL = (
    "https://www.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
)
CHALLENGE_WEB_URL = "https://www.instagram.com/api/v1/challenge/web/"

FRIENDSHIPS_FOLLOW_URL = "https://www.instagram.com/web/friendships/{user_id}/follow/"
FRIENDSHIPS_CREATE_URL = "https://www.instagram.com/api/v1/friendships/create/{user_id}/"
FRIENDSHIPS_DESTROY_URL = "https://www.instagram.com/api/v1/friendships/destroy/{user_id}/"

ACCOUNTS_EMAIL_SIGNUP_URL = "https://www.instagram.com/accounts/emailsignup/"
ACCOUNTS_SEND_SIGNUP_SMS_CODE_AJAX_URL = (
    "https://www.instagram.com/api/v1/web/accounts/send_signup_sms_code_ajax/"
)
WEB_ACCOUNTS_WEB_CREATE_AJAX_URL = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/"
WEB_ACCOUNTS_WEB_CREATE_AJAX_ATTEMPT_URL = (
    "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"
)

COMMENTS_ADD_URL = "https://www.instagram.com/api/v1/web/comments/{media_id}/add/"
COMMENTS_DELETE_URL = (
    "https://www.instagram.com/api/v1/web/comments/{media_id}/delete/{comment_id}/"
)
COMMENTS_LIKE_URL = "https://www.instagram.com/api/v1/web/comments/like/{comment_id}/"
COMMENTS_UNLIKE_URL = "https://www.instagram.com/api/v1/web/comments/unlike/{comment_id}/"

LIKES_LIKE_URL = "https://www.instagram.com/api/v1/web/likes/{media_id}/like/"
LIKES_UNLIKE_URL = "https://www.instagram.com/api/v1/web/likes/{media_id}/like/"

MASKED_EMAIL_PATTERN = re.compile(
    r"[a-z0-9\*._%+-]+@[a-z0-9\*.-]+\.[a-z]{2,}",
    re.IGNORECASE,
)
