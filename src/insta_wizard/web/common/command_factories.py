from __future__ import annotations

from collections.abc import Callable
from types import MappingProxyType

from insta_wizard.web.commands.account.check_age_eligibility import (
    CheckAgeEligibility,
    CheckAgeEligibilityHandler,
)
from insta_wizard.web.commands.account.edit import AccountsEdit, AccountsEditHandler
from insta_wizard.web.commands.account.edit_web_form_data import (
    AccountsEditWebFormData,
    AccountsEditWebFormDataHandler,
)
from insta_wizard.web.commands.account.get_email_signup_page import (
    GetEmailSignupPage,
    GetEmailSignupPageHandler,
)
from insta_wizard.web.commands.account.login_ajax import (
    AccountsLoginAjax,
    AccountsLoginAjaxHandler,
)
from insta_wizard.web.commands.account.logout_ajax import AccountsLogoutAjax, AccountsLogoutAjaxHandler
from insta_wizard.web.commands.account.recovery_send_ajax import (
    AccountRecoverySendAjax,
    AccountRecoverySendAjaxHandler,
)
from insta_wizard.web.commands.account.send_sms_code_ajax import (
    SendSignupSmsCodeAjax,
    SendSignupSmsCodeAjaxHandler,
)
from insta_wizard.web.commands.account.web_create_ajax import (
    WebCreateAjax,
    WebCreateAjaxHandler,
)
from insta_wizard.web.commands.account.web_create_ajax_attempt import (
    WebCreateAjaxAttempt,
    WebCreateAjaxAttemptHandler,
)
from insta_wizard.web.commands.auth_platform.code_entry_view_query import (
    AuthPlatformCodeEntryViewQuery,
    AuthPlatformCodeEntryViewQueryHandler,
)
from insta_wizard.web.commands.auth_platform.send_code_again import (
    UseAuthPlatformSendCodeAgainMutation,
    UseAuthPlatformSendCodeAgainMutationHandler,
)
from insta_wizard.web.commands.auth_platform.submit_code import (
    UseAuthPlatformSubmitCodeMutation,
    UseAuthPlatformSubmitCodeMutationHandler,
)
from insta_wizard.web.commands.challenge.bloks_navigation import (
    BloksNavigationTakeChallenge,
    BloksNavigationTakeChallengeHandler,
)
from insta_wizard.web.commands.challenge.challenge_web import (
    ChallengeWeb,
    ChallengeWebHandler,
)
from insta_wizard.web.commands.comments.comments_add import CommentsAdd, CommentsAddHandler
from insta_wizard.web.commands.comments.comments_like import CommentsLike, CommentsLikeHandler
from insta_wizard.web.commands.comments.comments_unlike import CommentsUnlike, CommentsUnlikeHandler
from insta_wizard.web.commands.friendships.create import (
    FriendshipsCreate,
    FriendshipsCreateHandler,
)
from insta_wizard.web.commands.friendships.follow import (
    FriendshipsFollow,
    FriendshipsFollowHandler,
)
from insta_wizard.web.commands.likes.likes_like import LikesLike, LikesLikeHandler
from insta_wizard.web.commands.likes.likes_unlike import LikesUnlike, LikesUnlikeHandler
from insta_wizard.web.commands.navigation.get_home_page import (
    GetInstagramHomePage,
    GetInstagramHomePageHandler,
)
from insta_wizard.web.commands.navigation.get_shared_data import (
    GetSharedData,
    GetSharedDataHandler,
)
from insta_wizard.web.commands.navigation.get_web_mid import (
    GetWebMid,
    GetWebMidHandler,
)
from insta_wizard.web.commands.navigation.navigate import (
    Navigate,
    NavigateHandler,
)
from insta_wizard.web.commands.search.polaris_search_box import (
    PolarisSearchBoxRefetchableQuery,
    PolarisSearchBoxRefetchableQueryHandler,
)
from insta_wizard.web.common.command import CommandHandler
from insta_wizard.web.flows.login import Login, LoginHandler
from insta_wizard.web.models.deps import ClientDeps

COMMAND_FACTORIES: dict[type, Callable[[ClientDeps], CommandHandler]] = {
    Navigate: lambda d: NavigateHandler(
        navigator=d.navigator,
        state=d.state,
    ),
    GetInstagramHomePage: lambda d: GetInstagramHomePageHandler(
        navigator=d.navigator,
        state=d.state,
    ),
    GetEmailSignupPage: lambda d: GetEmailSignupPageHandler(
        navigator=d.navigator,
        state=d.state,
    ),
    GetWebMid: lambda d: GetWebMidHandler(
        navigator=d.navigator,
        state=d.state,
    ),
    GetSharedData: lambda d: GetSharedDataHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    ChallengeWeb: lambda d: ChallengeWebHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    BloksNavigationTakeChallenge: lambda d: BloksNavigationTakeChallengeHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    AccountRecoverySendAjax: lambda d: AccountRecoverySendAjaxHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    AccountsLoginAjax: lambda d: AccountsLoginAjaxHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    AccountsLogoutAjax: lambda d: AccountsLogoutAjaxHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    AccountsEdit: lambda d: AccountsEditHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    FriendshipsCreate: lambda d: FriendshipsCreateHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    FriendshipsFollow: lambda d: FriendshipsFollowHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    CommentsAdd: lambda d: CommentsAddHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    CommentsLike: lambda d: CommentsLikeHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    CommentsUnlike: lambda d: CommentsUnlikeHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    LikesLike: lambda d: LikesLikeHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    LikesUnlike: lambda d: LikesUnlikeHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    AccountsEditWebFormData: lambda d: AccountsEditWebFormDataHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    WebCreateAjaxAttempt: lambda d: WebCreateAjaxAttemptHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    CheckAgeEligibility: lambda d: CheckAgeEligibilityHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    SendSignupSmsCodeAjax: lambda d: SendSignupSmsCodeAjaxHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    WebCreateAjax: lambda d: WebCreateAjaxHandler(api_requester=d.api_requester, state=d.state),
    AuthPlatformCodeEntryViewQuery: lambda d: AuthPlatformCodeEntryViewQueryHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    UseAuthPlatformSubmitCodeMutation: lambda d: UseAuthPlatformSubmitCodeMutationHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    UseAuthPlatformSendCodeAgainMutation: lambda d: UseAuthPlatformSendCodeAgainMutationHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    PolarisSearchBoxRefetchableQuery: lambda d: PolarisSearchBoxRefetchableQueryHandler(
        api_requester=d.api_requester,
        state=d.state,
    ),
    Login: lambda d: LoginHandler(state=d.state, initializer=d.initializer, bus=d.bus),
}

COMMAND_FACTORIES = MappingProxyType(COMMAND_FACTORIES)
