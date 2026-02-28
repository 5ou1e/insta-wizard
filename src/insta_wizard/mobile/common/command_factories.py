from __future__ import annotations

from collections.abc import Callable
from types import MappingProxyType

from insta_wizard.mobile.commands import MediaDelete, MediaLike, MediaLikers, MediaSave
from insta_wizard.mobile.commands.account.change_profile_picture import (
    AccountChangeProfilePicture,
    AccountChangeProfilePictureHandler,
)
from insta_wizard.mobile.commands.account.check_phone_number import (
    AccountCheckPhoneNumber,
    AccountCheckPhoneNumberHandler,
)
from insta_wizard.mobile.commands.account.create_validated import (
    AccountCreateValidated,
    AccountCreateValidatedHandler,
)
from insta_wizard.mobile.commands.account.current_user import (
    AccountCurrentUser,
    AccountCurrentUserHandler,
)
from insta_wizard.mobile.commands.account.edit_profile import (
    AccountEditProfile,
    AccountEditProfileHandler,
)
from insta_wizard.mobile.commands.account.get_presence_disabled import (
    AccountGetPresenceDisabled,
    AccountGetPresenceDisabledHandler,
)
from insta_wizard.mobile.commands.account.login import (
    AccountLogin,
    AccountLoginHandler,
)
from insta_wizard.mobile.commands.account.logout import AccountsLogout, AccountsLogoutHandler
from insta_wizard.mobile.commands.account.security_info import (
    AccountSecurityInfo,
    AccountSecurityInfoHandler,
)
from insta_wizard.mobile.commands.account.send_confirm_email import (
    AccountSendConfirmEmail,
    AccountSendConfirmEmailHandler,
)
from insta_wizard.mobile.commands.account.send_confirm_phone_number import (
    AccountSendConfirmPhoneNumber,
    AccountSendConfirmPhoneNumberHandler,
)
from insta_wizard.mobile.commands.account.send_signup_sms_code import (
    AccountSendSignupSmsCode,
    AccountSendSignupSmsCodeHandler,
)
from insta_wizard.mobile.commands.account.set_biography import (
    AccountSetBiography,
    AccountSetBiographyHandler,
)
from insta_wizard.mobile.commands.account.update_profile_name import (
    AccountUpdateProfileName,
    AccountUpdateProfileNameHandler,
)
from insta_wizard.mobile.commands.account.username_suggestions import (
    AccountUsernameSuggestions,
    AccountUsernameSuggestionsHandler,
)
from insta_wizard.mobile.commands.account.validate_signup_sms_code import (
    AccountValidateSignupSmsCode,
    AccountValidateSignupSmsCodeHandler,
)
from insta_wizard.mobile.commands.android_modules.download_b_api import (
    AndroidModulesDownload,
    AndroidModulesDownloadHandler,
)
from insta_wizard.mobile.commands.attestation.create_android_keystore_b_api import (
    AttestationCreateAndroidKeystore,
    AttestationCreateAndroidKeystoreHandler,
)
from insta_wizard.mobile.commands.attestation.create_android_playintegrity import (
    AttestationCreateAndroidPlayIntegrity,
    AttestationCreateAndroidPlayIntegrityHandler,
)
from insta_wizard.mobile.commands.banyan.banyan import (
    BanyanBanyan,
    BanyanBanyanHandler,
)
from insta_wizard.mobile.commands.bloks.login_save_credentials import (
    BloksLoginSaveCredentialsBApi,
    BloksLoginSaveCredentialsBApiHandler,
)
from insta_wizard.mobile.commands.bloks.phone_number_prefill_async import (
    BloksPhoneNumberPrefillAsync,
    BloksPhoneNumberPrefillAsyncHandler,
)
from insta_wizard.mobile.commands.bloks.process_client_data_and_redirect import (
    BloksProcessClientDataAndRedirectBApi,
    BloksProcessClientDataAndRedirectBApiHandler,
)
from insta_wizard.mobile.commands.bloks.send_login_request import (
    BloksSendLoginRequest,
    BloksSendLoginRequestHandler,
)
from insta_wizard.mobile.commands.bloks.youth_regulation_delete_pregent import (
    BloksYouthRegulationDeletePregent,
    BloksYouthRegulationDeletePregentHandler,
)
from insta_wizard.mobile.commands.challenge.challenge_action import (
    ChallengeAction,
    ChallengeActionHandler,
)
from insta_wizard.mobile.commands.challenge.get_challenge_info import (
    ChallengeGetChallengeInfo,
    ChallengeGetChallengeInfoHandler,
)
from insta_wizard.mobile.commands.clips.discover_stream import (
    ClipsDiscoverStream,
    ClipsDiscoverStreamHandler,
)
from insta_wizard.mobile.commands.clips.user_share_to_fb_config import (
    ClipsUserShareToFbConfig,
    ClipsUserShareToFbConfigHandler,
)
from insta_wizard.mobile.commands.consent.get_signup_config import (
    ConsentGetSignupConfig,
    ConsentGetSignupConfigHandler,
)
from insta_wizard.mobile.commands.creatives.write_supported_capabilities import (
    CreativesWriteSupportedCapabilities,
    CreativesWriteSupportedCapabilitiesHandler,
)
from insta_wizard.mobile.commands.direct.async_get_pending_requests_preview import (
    DirectV2AsyncGetPendingRequestsPreview,
    DirectV2AsyncGetPendingRequestsPreviewHandler,
)
from insta_wizard.mobile.commands.direct.create_group_thread import (
    DirectV2CreateGroupThread,
    DirectV2CreateGroupThreadHandler,
)
from insta_wizard.mobile.commands.direct.get_pending_requests_preview import (
    DirectV2GetPendingRequestsPreview,
    DirectV2GetPendingRequestsPreviewHandler,
)
from insta_wizard.mobile.commands.direct.get_presence import (
    DirectV2GetPresence,
    DirectV2GetPresenceHandler,
)
from insta_wizard.mobile.commands.direct.get_presence_active_now import (
    DirectV2GetPresenceActiveNow,
    DirectV2GetPresenceActiveNowHandler,
)
from insta_wizard.mobile.commands.direct.has_interop_upgraded import (
    DirectV2HasInteropUpgraded,
    DirectV2HasInteropUpgradedHandler,
)
from insta_wizard.mobile.commands.direct.inbox import (
    DirectV2Inbox,
    DirectV2InboxHandler,
)
from insta_wizard.mobile.commands.direct.ranked_recipients import (
    DirectV2RankedRecipients,
    DirectV2RankedRecipientsHandler,
)
from insta_wizard.mobile.commands.direct.threads_add_user import (
    DirectV2ThreadsAddUser,
    DirectV2ThreadsAddUserHandler,
)
from insta_wizard.mobile.commands.direct.threads_approve import (
    DirectV2ThreadsApprove,
    DirectV2ThreadsApproveHandler,
)
from insta_wizard.mobile.commands.direct.threads_approve_multiple import (
    DirectV2ThreadsApproveMultiple,
    DirectV2ThreadsApproveMultipleHandler,
)
from insta_wizard.mobile.commands.direct.threads_broadcast_reaction import (
    DirectV2ThreadsBroadcastReaction,
    DirectV2ThreadsBroadcastReactionHandler,
)
from insta_wizard.mobile.commands.direct.threads_broadcast_text import (
    DirectV2ThreadsBroadcastText,
    DirectV2ThreadsBroadcastTextHandler,
)
from insta_wizard.mobile.commands.direct.threads_decline import (
    DirectV2ThreadsDecline,
    DirectV2ThreadsDeclineHandler,
)
from insta_wizard.mobile.commands.direct.threads_decline_all import (
    DirectV2ThreadsDeclineAll,
    DirectV2ThreadsDeclineAllHandler,
)
from insta_wizard.mobile.commands.direct.threads_decline_multiple import (
    DirectV2ThreadsDeclineMultiple,
    DirectV2ThreadsDeclineMultipleHandler,
)
from insta_wizard.mobile.commands.direct.threads_delete_items_locally import (
    DirectV2ThreadsDeleteItemsLocally,
    DirectV2ThreadsDeleteItemsLocallyHandler,
)
from insta_wizard.mobile.commands.direct.threads_hide import (
    DirectV2ThreadsHide,
    DirectV2ThreadsHideHandler,
)
from insta_wizard.mobile.commands.direct.threads_items_delete import (
    DirectV2ThreadsItemsDelete,
    DirectV2ThreadsItemsDeleteHandler,
)
from insta_wizard.mobile.commands.direct.threads_items_seen import (
    DirectV2ThreadsItemsSeen,
    DirectV2ThreadsItemsSeenHandler,
)
from insta_wizard.mobile.commands.direct.threads_leave import (
    DirectV2ThreadsLeave,
    DirectV2ThreadsLeaveHandler,
)
from insta_wizard.mobile.commands.direct.threads_mute import (
    DirectV2ThreadsMute,
    DirectV2ThreadsMuteHandler,
)
from insta_wizard.mobile.commands.direct.threads_unmute import (
    DirectV2ThreadsUnmute,
    DirectV2ThreadsUnmuteHandler,
)
from insta_wizard.mobile.commands.direct.threads_update_title import (
    DirectV2ThreadsUpdateTitle,
    DirectV2ThreadsUpdateTitleHandler,
)
from insta_wizard.mobile.commands.feed.get_feed_timeline_b_api import (
    FeedTimelineBApi,
    FeedTimelineBApiHandler,
)
from insta_wizard.mobile.commands.feed.get_feed_timeline_i_api import (
    FeedTimelineIApi,
    FeedTimelineIApiHandler,
)
from insta_wizard.mobile.commands.feed.get_reels_tray import (
    FeedGetReelsTray,
    FeedGetReelsTrayHandler,
)
from insta_wizard.mobile.commands.feed.injected_reels_media import (
    FeedInjectedReelsMedia,
    FeedInjectedReelsMediaHandler,
)
from insta_wizard.mobile.commands.fetch_rmd import (
    FetchRmd,
    FetchRmdHandler,
)
from insta_wizard.mobile.commands.friendships.create import (
    FriendshipsCreate,
    FriendshipsCreateHandler,
)
from insta_wizard.mobile.commands.friendships.destroy import (
    FriendshipsDestroy,
    FriendshipsDestroyHandler,
)
from insta_wizard.mobile.commands.friendships.remove_follower import (
    FriendshipsRemoveFollower,
    FriendshipsRemoveFollowerHandler,
)
from insta_wizard.mobile.commands.friendships.show import FriendshipsShow, FriendshipsShowHandler
from insta_wizard.mobile.commands.friendships.show_many import (
    FriendshipsShowMany,
    FriendshipsShowManyHandler,
)
from insta_wizard.mobile.commands.friendships.user_followers import (
    FriendshipsUserFollowers,
    FriendshipsUserFollowersHandler,
)
from insta_wizard.mobile.commands.friendships.user_following import (
    FriendshipsUserFollowing,
    FriendshipsUserFollowingHandler,
)
from insta_wizard.mobile.commands.launcher.mobile_config import (
    LauncherMobileConfig,
    LauncherMobileConfigHandler,
)
from insta_wizard.mobile.commands.launcher.mobile_config_b_api import (
    LauncherMobileConfigBApi,
    LauncherMobileConfigBApiHandler,
)
from insta_wizard.mobile.commands.live.get_good_time_for_live import (
    LiveGetGoodTimeForLive,
    LiveGetGoodTimeForLiveHandler,
)
from insta_wizard.mobile.commands.loom.fetch_config import (
    LoomFetchConfig,
    LoomFetchConfigHandler,
)
from insta_wizard.mobile.commands.media.blocked import (
    MediaBlocked,
    MediaBlockedHandler,
)
from insta_wizard.mobile.commands.media.comment import MediaComment, MediaCommentHandler
from insta_wizard.mobile.commands.media.comment_bulk_delete import (
    MediaCommentBulkDelete,
    MediaCommentBulkDeleteHandler,
)
from insta_wizard.mobile.commands.media.comment_like import (
    MediaCommentLike,
    MediaCommentLikeHandler,
)
from insta_wizard.mobile.commands.media.comment_unlike import (
    MediaCommentUnlike,
    MediaCommentUnlikeHandler,
)
from insta_wizard.mobile.commands.media.comments import MediaComments, MediaCommentsHandler
from insta_wizard.mobile.commands.media.delete import MediaDeleteHandler
from insta_wizard.mobile.commands.media.edit import MediaEdit, MediaEditHandler
from insta_wizard.mobile.commands.media.like import MediaLikeHandler
from insta_wizard.mobile.commands.media.likers import MediaLikersHandler
from insta_wizard.mobile.commands.media.save import MediaSaveHandler
from insta_wizard.mobile.commands.media.unlike import MediaUnlike, MediaUnlikeHandler
from insta_wizard.mobile.commands.media.unsave import MediaUnsave, MediaUnsaveHandler
from insta_wizard.mobile.commands.multiple_accounts.get_account_family import (
    MultipleAcountsGetAccountFamily,
    MultipleAcountsGetAccountFamilyHandler,
)
from insta_wizard.mobile.commands.news.inbox import (
    NewsInbox,
    NewsInboxHandler,
)
from insta_wizard.mobile.commands.news.inbox_seen import NewsInboxSeen, NewsInboxSeenHandler
from insta_wizard.mobile.commands.notifications.badge import (
    NotificationsBadge,
    NotificationsBadgeHandler,
)
from insta_wizard.mobile.commands.notifications.get_notification_settings import (
    NotificationsGetNotificationSettings,
    NotificationsGetNotificationSettingsHandler,
)
from insta_wizard.mobile.commands.notifications.store_client_push_permissions import (
    NotificationsStoreClientPushPermissions,
    NotificationsStoreClientPushPermissionsHandler,
)
from insta_wizard.mobile.commands.rupload_igphoto import (
    RuploadIgphoto,
    RuploadIgphotoHandler,
)
from insta_wizard.mobile.commands.user.account_details import (
    UserAccountDetails,
    UserAccountDetailsHandler,
)
from insta_wizard.mobile.commands.user.check_username import (
    UsersCheckUsername,
    UsersCheckUsernameHandler,
)
from insta_wizard.mobile.commands.user.get_limited_interactions_reminder import (
    UserGetLimitedInteractionsReminder,
    UserGetLimitedInteractionsReminderHandler,
)
from insta_wizard.mobile.commands.user.info import (
    UserInfo,
    UserInfoHandler,
)
from insta_wizard.mobile.commands.user.search import (
    UserSearch,
    UserSearchHandler,
)
from insta_wizard.mobile.commands.user.usernameinfo import (
    UserUsernameInfo,
    UserUsernameInfoHandler,
)
from insta_wizard.mobile.commands.user.web_profile_info import (
    UserWebProfileInfo,
    UserWebProfileInfoHandler,
)
from insta_wizard.mobile.commands.zr.dual_tokens import (
    ZrDualTokens,
    ZrDualTokensHandler,
)
from insta_wizard.mobile.common.command import CommandHandler
from insta_wizard.mobile.flows.bloks_login import (
    BloksLogin,
    BloksLoginHandler,
)
from insta_wizard.mobile.models.deps import ClientDeps

COMMAND_FACTORIES: dict[type, Callable[[ClientDeps], CommandHandler]] = {
    # user
    UserInfo: lambda d: UserInfoHandler(
        api=d.api,
        state=d.state,
    ),
    UserUsernameInfo: lambda d: UserUsernameInfoHandler(
        api=d.api,
        state=d.state,
    ),
    UserWebProfileInfo: lambda d: UserWebProfileInfoHandler(
        api=d.api,
        state=d.state,
    ),
    UsersCheckUsername: lambda d: UsersCheckUsernameHandler(
        api=d.api,
        state=d.state,
    ),
    UserGetLimitedInteractionsReminder: lambda d: UserGetLimitedInteractionsReminderHandler(
        api=d.api,
        state=d.state,
    ),
    UserSearch: lambda d: UserSearchHandler(
        api=d.api,
        state=d.state,
    ),
    UserAccountDetails: lambda d: UserAccountDetailsHandler(
        api=d.api,
        state=d.state,
    ),
    # zr
    ZrDualTokens: lambda d: ZrDualTokensHandler(
        api=d.api,
        state=d.state,
    ),
    # notifications
    NotificationsGetNotificationSettings: lambda d: NotificationsGetNotificationSettingsHandler(
        api=d.api,
        state=d.state,
    ),
    NotificationsBadge: lambda d: NotificationsBadgeHandler(
        api=d.api,
        state=d.state,
    ),
    NotificationsStoreClientPushPermissions: lambda d: (
        NotificationsStoreClientPushPermissionsHandler(
            api=d.api,
            state=d.state,
        )
    ),
    # news
    NewsInbox: lambda d: NewsInboxHandler(
        api=d.api,
        state=d.state,
    ),
    NewsInboxSeen: lambda d: NewsInboxSeenHandler(
        api=d.api,
        state=d.state,
    ),
    # multiple accounts
    MultipleAcountsGetAccountFamily: lambda d: MultipleAcountsGetAccountFamilyHandler(
        api=d.api,
        state=d.state,
    ),
    # media
    MediaLike: lambda d: MediaLikeHandler(
        api=d.api,
        state=d.state,
    ),
    MediaUnlike: lambda d: MediaUnlikeHandler(
        api=d.api,
        state=d.state,
    ),
    MediaDelete: lambda d: MediaDeleteHandler(
        api=d.api,
        state=d.state,
    ),
    MediaEdit: lambda d: MediaEditHandler(
        api=d.api,
        state=d.state,
    ),
    MediaLikers: lambda d: MediaLikersHandler(
        api=d.api,
        state=d.state,
    ),
    MediaSave: lambda d: MediaSaveHandler(
        api=d.api,
        state=d.state,
    ),
    MediaUnsave: lambda d: MediaUnsaveHandler(
        api=d.api,
        state=d.state,
    ),
    MediaBlocked: lambda d: MediaBlockedHandler(
        api=d.api,
        state=d.state,
    ),
    MediaComments: lambda d: MediaCommentsHandler(
        api=d.api,
        state=d.state,
    ),
    MediaComment: lambda d: MediaCommentHandler(
        api=d.api,
        state=d.state,
    ),
    MediaCommentBulkDelete: lambda d: MediaCommentBulkDeleteHandler(
        api=d.api,
        state=d.state,
    ),
    MediaCommentLike: lambda d: MediaCommentLikeHandler(
        api=d.api,
        state=d.state,
    ),
    MediaCommentUnlike: lambda d: MediaCommentUnlikeHandler(
        api=d.api,
        state=d.state,
    ),
    # loom/live
    LoomFetchConfig: lambda d: LoomFetchConfigHandler(
        api=d.api,
        state=d.state,
    ),
    LiveGetGoodTimeForLive: lambda d: LiveGetGoodTimeForLiveHandler(
        api=d.api,
        state=d.state,
    ),
    # launcher
    LauncherMobileConfig: lambda d: LauncherMobileConfigHandler(
        api=d.api,
        state=d.state,
    ),
    LauncherMobileConfigBApi: lambda d: LauncherMobileConfigBApiHandler(
        api=d.api,
        state=d.state,
    ),
    # friendships
    FriendshipsCreate: lambda d: FriendshipsCreateHandler(
        api=d.api,
        state=d.state,
    ),
    FriendshipsDestroy: lambda d: FriendshipsDestroyHandler(
        api=d.api,
        state=d.state,
    ),
    FriendshipsRemoveFollower: lambda d: FriendshipsRemoveFollowerHandler(
        api=d.api,
        state=d.state,
    ),
    FriendshipsUserFollowers: lambda d: FriendshipsUserFollowersHandler(
        api=d.api,
        state=d.state,
    ),
    FriendshipsUserFollowing: lambda d: FriendshipsUserFollowingHandler(
        api=d.api,
        state=d.state,
    ),
    FriendshipsShowMany: lambda d: FriendshipsShowManyHandler(
        api=d.api,
        state=d.state,
    ),
    # direct
    DirectV2RankedRecipients: lambda d: DirectV2RankedRecipientsHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2CreateGroupThread: lambda d: DirectV2CreateGroupThreadHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsApprove: lambda d: DirectV2ThreadsApproveHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsApproveMultiple: lambda d: DirectV2ThreadsApproveMultipleHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsDecline: lambda d: DirectV2ThreadsDeclineHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsDeclineAll: lambda d: DirectV2ThreadsDeclineAllHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsDeclineMultiple: lambda d: DirectV2ThreadsDeclineMultipleHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsItemsDelete: lambda d: DirectV2ThreadsItemsDeleteHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsItemsSeen: lambda d: DirectV2ThreadsItemsSeenHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsHide: lambda d: DirectV2ThreadsHideHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsLeave: lambda d: DirectV2ThreadsLeaveHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsAddUser: lambda d: DirectV2ThreadsAddUserHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsUpdateTitle: lambda d: DirectV2ThreadsUpdateTitleHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsMute: lambda d: DirectV2ThreadsMuteHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsUnmute: lambda d: DirectV2ThreadsUnmuteHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2GetPresence: lambda d: DirectV2GetPresenceHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2GetPendingRequestsPreview: lambda d: DirectV2GetPendingRequestsPreviewHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2Inbox: lambda d: DirectV2InboxHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2GetPresenceActiveNow: lambda d: DirectV2GetPresenceActiveNowHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2HasInteropUpgraded: lambda d: DirectV2HasInteropUpgradedHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2AsyncGetPendingRequestsPreview: lambda d: DirectV2AsyncGetPendingRequestsPreviewHandler(
        api=d.api,
        state=d.state,
    ),
    # creatives
    CreativesWriteSupportedCapabilities: lambda d: CreativesWriteSupportedCapabilitiesHandler(
        api=d.api,
        state=d.state,
    ),
    # consent
    ConsentGetSignupConfig: lambda d: ConsentGetSignupConfigHandler(
        api=d.api,
        state=d.state,
    ),
    # clips
    ClipsDiscoverStream: lambda d: ClipsDiscoverStreamHandler(
        api=d.api,
        state=d.state,
    ),
    ClipsUserShareToFbConfig: lambda d: ClipsUserShareToFbConfigHandler(
        api=d.api,
        state=d.state,
    ),
    # challenge
    ChallengeGetChallengeInfo: lambda d: ChallengeGetChallengeInfoHandler(
        api=d.api,
        state=d.state,
    ),
    ChallengeAction: lambda d: ChallengeActionHandler(
        api=d.api,
        state=d.state,
    ),
    # banyan
    BanyanBanyan: lambda d: BanyanBanyanHandler(
        api=d.api,
        state=d.state,
    ),
    # attestation
    AttestationCreateAndroidKeystore: lambda d: AttestationCreateAndroidKeystoreHandler(
        api=d.api,
        state=d.state,
    ),
    AttestationCreateAndroidPlayIntegrity: lambda d: AttestationCreateAndroidPlayIntegrityHandler(
        api=d.api,
        state=d.state,
    ),
    # android modules
    AndroidModulesDownload: lambda d: AndroidModulesDownloadHandler(
        api=d.api,
        state=d.state,
    ),
    # account
    AccountCurrentUser: lambda d: AccountCurrentUserHandler(
        api=d.api,
        state=d.state,
    ),
    AccountEditProfile: lambda d: AccountEditProfileHandler(
        api=d.api,
        state=d.state,
    ),
    AccountUpdateProfileName: lambda d: AccountUpdateProfileNameHandler(
        api=d.api,
        state=d.state,
    ),
    AccountSetBiography: lambda d: AccountSetBiographyHandler(
        api=d.api,
        state=d.state,
    ),
    AccountChangeProfilePicture: lambda d: AccountChangeProfilePictureHandler(
        api=d.api,
        state=d.state,
    ),
    AccountGetPresenceDisabled: lambda d: AccountGetPresenceDisabledHandler(
        api=d.api,
        state=d.state,
    ),
    AccountLogin: lambda d: AccountLoginHandler(
        api=d.api,
        state=d.state,
    ),
    AccountsLogout: lambda d: AccountsLogoutHandler(
        api=d.api,
        state=d.state,
    ),
    AccountCheckPhoneNumber: lambda d: AccountCheckPhoneNumberHandler(
        api=d.api,
        state=d.state,
    ),
    AccountSendSignupSmsCode: lambda d: AccountSendSignupSmsCodeHandler(
        api=d.api,
        state=d.state,
    ),
    AccountValidateSignupSmsCode: lambda d: AccountValidateSignupSmsCodeHandler(
        api=d.api,
        state=d.state,
    ),
    AccountUsernameSuggestions: lambda d: AccountUsernameSuggestionsHandler(
        api=d.api,
        state=d.state,
    ),
    AccountCreateValidated: lambda d: AccountCreateValidatedHandler(
        api=d.api,
        state=d.state,
    ),
    AccountSecurityInfo: lambda d: AccountSecurityInfoHandler(
        api=d.api,
        state=d.state,
    ),
    AccountSendConfirmEmail: lambda d: AccountSendConfirmEmailHandler(
        api=d.api,
        state=d.state,
    ),
    AccountSendConfirmPhoneNumber: lambda d: AccountSendConfirmPhoneNumberHandler(
        api=d.api,
        state=d.state,
    ),
    # feed
    FeedTimelineIApi: lambda d: FeedTimelineIApiHandler(
        api=d.api,
        state=d.state,
    ),
    FeedTimelineBApi: lambda d: FeedTimelineBApiHandler(
        api=d.api,
        state=d.state,
    ),
    FeedGetReelsTray: lambda d: FeedGetReelsTrayHandler(
        api=d.api,
        state=d.state,
    ),
    FeedInjectedReelsMedia: lambda d: FeedInjectedReelsMediaHandler(
        api=d.api,
        state=d.state,
    ),
    # bloks (commands)
    BloksSendLoginRequest: lambda d: BloksSendLoginRequestHandler(
        api=d.api,
        state=d.state,
    ),
    BloksProcessClientDataAndRedirectBApi: lambda d: BloksProcessClientDataAndRedirectBApiHandler(
        api=d.api,
        state=d.state,
    ),
    BloksPhoneNumberPrefillAsync: lambda d: BloksPhoneNumberPrefillAsyncHandler(
        api=d.api,
        state=d.state,
    ),
    BloksLoginSaveCredentialsBApi: lambda d: BloksLoginSaveCredentialsBApiHandler(
        api=d.api,
        state=d.state,
    ),
    BloksYouthRegulationDeletePregent: lambda d: BloksYouthRegulationDeletePregentHandler(
        api=d.api,
        state=d.state,
    ),
    # misc
    RuploadIgphoto: lambda d: RuploadIgphotoHandler(
        request_executor=d.req,
        state=d.state,
        headers=d.headers,
    ),
    FetchRmd: lambda d: FetchRmdHandler(
        request_executor=d.req,
        state=d.state,
    ),
    # flows
    BloksLogin: lambda d: BloksLoginHandler(
        state=d.state,
        api=d.api,
        bus=d.bus,
    ),
    # ----------- NEW ----------
    FriendshipsShow: lambda d: FriendshipsShowHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsDeleteItemsLocally: lambda d: DirectV2ThreadsDeleteItemsLocallyHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsBroadcastReaction: lambda d: DirectV2ThreadsBroadcastReactionHandler(
        api=d.api,
        state=d.state,
    ),
    DirectV2ThreadsBroadcastText: lambda d: DirectV2ThreadsBroadcastTextHandler(
        api=d.api,
        state=d.state,
    ),
}

COMMAND_FACTORIES = MappingProxyType(COMMAND_FACTORIES)
