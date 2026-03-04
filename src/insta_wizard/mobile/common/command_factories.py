from __future__ import annotations

from collections.abc import Callable
from types import MappingProxyType

from insta_wizard.mobile.commands import MediaDelete, MediaLike, MediaLikers, MediaSave
from insta_wizard.mobile.commands.account.change_profile_picture import (
    AccountChangeProfilePicture,
    AccountChangeProfilePictureHandler,
)
from insta_wizard.mobile.commands.account.check_confirmation_code import (
    AccountCheckConfirmationCode,
    AccountCheckConfirmationCodeHandler,
)
from insta_wizard.mobile.commands.account.check_phone_number import (
    AccountCheckPhoneNumber,
    AccountCheckPhoneNumberHandler,
)
from insta_wizard.mobile.commands.account.create import AccountCreate, AccountCreateHandler
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
from insta_wizard.mobile.commands.account.send_verify_email import (
    AccountSendVerifyEmail,
    AccountSendVerifyEmailHandler,
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
from insta_wizard.mobile.commands.media.configure_sidecar import (
    MediaConfigureSidecar,
    MediaConfigureSidecarHandler,
)
from insta_wizard.mobile.commands.media.configure_timeline import (
    MediaConfigure,
    MediaConfigureHandler,
)
from insta_wizard.mobile.commands.media.configure_to_clips import (
    MediaConfigureToClips,
    MediaConfigureToClipsHandler,
)
from insta_wizard.mobile.commands.media.configure_to_story import (
    MediaConfigureToStory,
    MediaConfigureToStoryHandler,
)
from insta_wizard.mobile.commands.media.delete import MediaDeleteHandler
from insta_wizard.mobile.commands.media.edit import MediaEdit, MediaEditHandler
from insta_wizard.mobile.commands.media.info import MediaInfo, MediaInfoHandler
from insta_wizard.mobile.commands.media.like import MediaLikeHandler
from insta_wizard.mobile.commands.media.likers import MediaLikersHandler
from insta_wizard.mobile.commands.media.save import MediaSaveHandler
from insta_wizard.mobile.commands.media.unlike import MediaUnlike, MediaUnlikeHandler
from insta_wizard.mobile.commands.media.unsave import MediaUnsave, MediaUnsaveHandler
from insta_wizard.mobile.commands.media.upload_finish import (
    MediaUploadFinish,
    MediaUploadFinishHandler,
)
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
from insta_wizard.mobile.commands.rupload_igvideo import (
    RuploadIgvideo,
    RuploadIgvideoHandler,
)
from insta_wizard.mobile.commands.user.account_details import (
    UserAccountDetails,
    UserAccountDetailsHandler,
)
from insta_wizard.mobile.commands.user.check_email import UsersCheckEmail, UsersCheckEmailHandler
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
from insta_wizard.mobile.flows.publish_album import (
    PublishAlbum,
    PublishAlbumHandler,
)
from insta_wizard.mobile.flows.publish_photo import (
    PublishPhoto,
    PublishPhotoHandler,
)
from insta_wizard.mobile.flows.publish_reel import (
    PublishReel,
    PublishReelHandler,
)
from insta_wizard.mobile.flows.publish_story_photo import (
    PublishStoryPhoto,
    PublishStoryPhotoHandler,
)
from insta_wizard.mobile.flows.publish_story_video import (
    PublishStoryVideo,
    PublishStoryVideoHandler,
)
from insta_wizard.mobile.flows.publish_video import (
    PublishVideo,
    PublishVideoHandler,
)
from insta_wizard.mobile.flows.register_account_email import (
    RegisterAccountEmailFlow,
    RegisterAccountEmailFlowHandler,
)
from insta_wizard.mobile.flows.register_account_sms import (
    RegisterAccountSMSFlow,
    RegisterAccountSMSFlowHandler,
)
from insta_wizard.mobile.models.deps import ClientDeps

COMMAND_FACTORIES: dict[type, Callable[[ClientDeps], CommandHandler]] = {
    # user
    UserInfo: lambda d: UserInfoHandler(
        requester=d.requester,
        state=d.state,
    ),
    UserUsernameInfo: lambda d: UserUsernameInfoHandler(
        requester=d.requester,
        state=d.state,
    ),
    UserWebProfileInfo: lambda d: UserWebProfileInfoHandler(
        requester=d.requester,
        state=d.state,
    ),
    UsersCheckUsername: lambda d: UsersCheckUsernameHandler(
        requester=d.requester,
        state=d.state,
    ),
    UsersCheckEmail: lambda d: UsersCheckEmailHandler(
        requester=d.requester,
        state=d.state,
    ),
    UserGetLimitedInteractionsReminder: lambda d: UserGetLimitedInteractionsReminderHandler(
        requester=d.requester,
        state=d.state,
    ),
    UserSearch: lambda d: UserSearchHandler(
        requester=d.requester,
        state=d.state,
    ),
    UserAccountDetails: lambda d: UserAccountDetailsHandler(
        requester=d.requester,
        state=d.state,
    ),
    # zr
    ZrDualTokens: lambda d: ZrDualTokensHandler(
        requester=d.requester,
        state=d.state,
    ),
    # notifications
    NotificationsGetNotificationSettings: lambda d: NotificationsGetNotificationSettingsHandler(
        requester=d.requester,
        state=d.state,
    ),
    NotificationsBadge: lambda d: NotificationsBadgeHandler(
        requester=d.requester,
        state=d.state,
    ),
    NotificationsStoreClientPushPermissions: lambda d: (
        NotificationsStoreClientPushPermissionsHandler(
            requester=d.requester,
            state=d.state,
        )
    ),
    # news
    NewsInbox: lambda d: NewsInboxHandler(
        requester=d.requester,
        state=d.state,
    ),
    NewsInboxSeen: lambda d: NewsInboxSeenHandler(
        requester=d.requester,
        state=d.state,
    ),
    # multiple accounts
    MultipleAcountsGetAccountFamily: lambda d: MultipleAcountsGetAccountFamilyHandler(
        requester=d.requester,
        state=d.state,
    ),
    # media
    MediaInfo: lambda d: MediaInfoHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaLike: lambda d: MediaLikeHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaUnlike: lambda d: MediaUnlikeHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaDelete: lambda d: MediaDeleteHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaEdit: lambda d: MediaEditHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaLikers: lambda d: MediaLikersHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaSave: lambda d: MediaSaveHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaUnsave: lambda d: MediaUnsaveHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaBlocked: lambda d: MediaBlockedHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaComments: lambda d: MediaCommentsHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaComment: lambda d: MediaCommentHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaCommentBulkDelete: lambda d: MediaCommentBulkDeleteHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaCommentLike: lambda d: MediaCommentLikeHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaCommentUnlike: lambda d: MediaCommentUnlikeHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaUploadFinish: lambda d: MediaUploadFinishHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaConfigure: lambda d: MediaConfigureHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaConfigureToStory: lambda d: MediaConfigureToStoryHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaConfigureToClips: lambda d: MediaConfigureToClipsHandler(
        requester=d.requester,
        state=d.state,
    ),
    MediaConfigureSidecar: lambda d: MediaConfigureSidecarHandler(
        requester=d.requester,
        state=d.state,
    ),
    # loom/live
    LoomFetchConfig: lambda d: LoomFetchConfigHandler(
        requester=d.requester,
        state=d.state,
    ),
    LiveGetGoodTimeForLive: lambda d: LiveGetGoodTimeForLiveHandler(
        requester=d.requester,
        state=d.state,
    ),
    # launcher
    LauncherMobileConfig: lambda d: LauncherMobileConfigHandler(
        requester=d.requester,
        state=d.state,
    ),
    LauncherMobileConfigBApi: lambda d: LauncherMobileConfigBApiHandler(
        requester=d.requester,
        state=d.state,
    ),
    # friendships
    FriendshipsCreate: lambda d: FriendshipsCreateHandler(
        requester=d.requester,
        state=d.state,
    ),
    FriendshipsDestroy: lambda d: FriendshipsDestroyHandler(
        requester=d.requester,
        state=d.state,
    ),
    FriendshipsRemoveFollower: lambda d: FriendshipsRemoveFollowerHandler(
        requester=d.requester,
        state=d.state,
    ),
    FriendshipsUserFollowers: lambda d: FriendshipsUserFollowersHandler(
        requester=d.requester,
        state=d.state,
    ),
    FriendshipsUserFollowing: lambda d: FriendshipsUserFollowingHandler(
        requester=d.requester,
        state=d.state,
    ),
    FriendshipsShowMany: lambda d: FriendshipsShowManyHandler(
        requester=d.requester,
        state=d.state,
    ),
    # direct
    DirectV2RankedRecipients: lambda d: DirectV2RankedRecipientsHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2CreateGroupThread: lambda d: DirectV2CreateGroupThreadHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsApprove: lambda d: DirectV2ThreadsApproveHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsApproveMultiple: lambda d: DirectV2ThreadsApproveMultipleHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsDecline: lambda d: DirectV2ThreadsDeclineHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsDeclineAll: lambda d: DirectV2ThreadsDeclineAllHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsDeclineMultiple: lambda d: DirectV2ThreadsDeclineMultipleHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsItemsDelete: lambda d: DirectV2ThreadsItemsDeleteHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsItemsSeen: lambda d: DirectV2ThreadsItemsSeenHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsHide: lambda d: DirectV2ThreadsHideHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsLeave: lambda d: DirectV2ThreadsLeaveHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsAddUser: lambda d: DirectV2ThreadsAddUserHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsUpdateTitle: lambda d: DirectV2ThreadsUpdateTitleHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsMute: lambda d: DirectV2ThreadsMuteHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsUnmute: lambda d: DirectV2ThreadsUnmuteHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2GetPresence: lambda d: DirectV2GetPresenceHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2GetPendingRequestsPreview: lambda d: DirectV2GetPendingRequestsPreviewHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2Inbox: lambda d: DirectV2InboxHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2GetPresenceActiveNow: lambda d: DirectV2GetPresenceActiveNowHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2HasInteropUpgraded: lambda d: DirectV2HasInteropUpgradedHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2AsyncGetPendingRequestsPreview: lambda d: DirectV2AsyncGetPendingRequestsPreviewHandler(
        requester=d.requester,
        state=d.state,
    ),
    # creatives
    CreativesWriteSupportedCapabilities: lambda d: CreativesWriteSupportedCapabilitiesHandler(
        requester=d.requester,
        state=d.state,
    ),
    # consent
    ConsentGetSignupConfig: lambda d: ConsentGetSignupConfigHandler(
        requester=d.requester,
        state=d.state,
    ),
    # clips
    ClipsDiscoverStream: lambda d: ClipsDiscoverStreamHandler(
        requester=d.requester,
        state=d.state,
    ),
    ClipsUserShareToFbConfig: lambda d: ClipsUserShareToFbConfigHandler(
        requester=d.requester,
        state=d.state,
    ),
    # challenge
    ChallengeGetChallengeInfo: lambda d: ChallengeGetChallengeInfoHandler(
        requester=d.requester,
        state=d.state,
    ),
    ChallengeAction: lambda d: ChallengeActionHandler(
        requester=d.requester,
        state=d.state,
    ),
    # banyan
    BanyanBanyan: lambda d: BanyanBanyanHandler(
        requester=d.requester,
        state=d.state,
    ),
    # attestation
    AttestationCreateAndroidKeystore: lambda d: AttestationCreateAndroidKeystoreHandler(
        requester=d.requester,
        state=d.state,
    ),
    AttestationCreateAndroidPlayIntegrity: lambda d: AttestationCreateAndroidPlayIntegrityHandler(
        requester=d.requester,
        state=d.state,
    ),
    # android modules
    AndroidModulesDownload: lambda d: AndroidModulesDownloadHandler(
        requester=d.requester,
        state=d.state,
    ),
    # account
    AccountCurrentUser: lambda d: AccountCurrentUserHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountEditProfile: lambda d: AccountEditProfileHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountUpdateProfileName: lambda d: AccountUpdateProfileNameHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountSetBiography: lambda d: AccountSetBiographyHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountChangeProfilePicture: lambda d: AccountChangeProfilePictureHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountGetPresenceDisabled: lambda d: AccountGetPresenceDisabledHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountLogin: lambda d: AccountLoginHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountsLogout: lambda d: AccountsLogoutHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountCheckPhoneNumber: lambda d: AccountCheckPhoneNumberHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountSendSignupSmsCode: lambda d: AccountSendSignupSmsCodeHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountSendVerifyEmail: lambda d: AccountSendVerifyEmailHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountCheckConfirmationCode: lambda d: AccountCheckConfirmationCodeHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountValidateSignupSmsCode: lambda d: AccountValidateSignupSmsCodeHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountUsernameSuggestions: lambda d: AccountUsernameSuggestionsHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountCreate: lambda d: AccountCreateHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountCreateValidated: lambda d: AccountCreateValidatedHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountSecurityInfo: lambda d: AccountSecurityInfoHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountSendConfirmEmail: lambda d: AccountSendConfirmEmailHandler(
        requester=d.requester,
        state=d.state,
    ),
    AccountSendConfirmPhoneNumber: lambda d: AccountSendConfirmPhoneNumberHandler(
        requester=d.requester,
        state=d.state,
    ),
    # feed
    FeedTimelineIApi: lambda d: FeedTimelineIApiHandler(
        requester=d.requester,
        state=d.state,
    ),
    FeedTimelineBApi: lambda d: FeedTimelineBApiHandler(
        requester=d.requester,
        state=d.state,
    ),
    FeedGetReelsTray: lambda d: FeedGetReelsTrayHandler(
        requester=d.requester,
        state=d.state,
    ),
    FeedInjectedReelsMedia: lambda d: FeedInjectedReelsMediaHandler(
        requester=d.requester,
        state=d.state,
    ),
    # bloks (commands)
    BloksSendLoginRequest: lambda d: BloksSendLoginRequestHandler(
        requester=d.requester,
        state=d.state,
    ),
    BloksProcessClientDataAndRedirectBApi: lambda d: BloksProcessClientDataAndRedirectBApiHandler(
        requester=d.requester,
        state=d.state,
    ),
    BloksPhoneNumberPrefillAsync: lambda d: BloksPhoneNumberPrefillAsyncHandler(
        requester=d.requester,
        state=d.state,
    ),
    BloksLoginSaveCredentialsBApi: lambda d: BloksLoginSaveCredentialsBApiHandler(
        requester=d.requester,
        state=d.state,
    ),
    BloksYouthRegulationDeletePregent: lambda d: BloksYouthRegulationDeletePregentHandler(
        requester=d.requester,
        state=d.state,
    ),
    # misc
    RuploadIgphoto: lambda d: RuploadIgphotoHandler(
        requester=d.requester,
        state=d.state,
    ),
    RuploadIgvideo: lambda d: RuploadIgvideoHandler(
        requester=d.requester,
        state=d.state,
    ),
    FetchRmd: lambda d: FetchRmdHandler(
        requester=d.requester,
        state=d.state,
    ),
    # flows
    BloksLogin: lambda d: BloksLoginHandler(
        state=d.state,
        requester=d.requester,
        bus=d.bus,
    ),
    PublishPhoto: lambda d: PublishPhotoHandler(
        bus=d.bus,
    ),
    PublishVideo: lambda d: PublishVideoHandler(
        bus=d.bus,
    ),
    PublishStoryPhoto: lambda d: PublishStoryPhotoHandler(
        bus=d.bus,
    ),
    PublishAlbum: lambda d: PublishAlbumHandler(
        bus=d.bus,
    ),
    PublishReel: lambda d: PublishReelHandler(
        bus=d.bus,
    ),
    PublishStoryVideo: lambda d: PublishStoryVideoHandler(
        bus=d.bus,
    ),
    RegisterAccountSMSFlow: lambda d: RegisterAccountSMSFlowHandler(
        state=d.state,
        bus=d.bus,
        logger=d.logger,
    ),
    RegisterAccountEmailFlow: lambda d: RegisterAccountEmailFlowHandler(
        state=d.state,
        bus=d.bus,
        logger=d.logger,
    ),
    # ----------- NEW ----------
    FriendshipsShow: lambda d: FriendshipsShowHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsDeleteItemsLocally: lambda d: DirectV2ThreadsDeleteItemsLocallyHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsBroadcastReaction: lambda d: DirectV2ThreadsBroadcastReactionHandler(
        requester=d.requester,
        state=d.state,
    ),
    DirectV2ThreadsBroadcastText: lambda d: DirectV2ThreadsBroadcastTextHandler(
        requester=d.requester,
        state=d.state,
    ),
}

COMMAND_FACTORIES = MappingProxyType(COMMAND_FACTORIES)
