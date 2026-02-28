from typing import Literal

from insta_wizard.common.entities import (
    Account,
    Comment,
    DirectThread,
    FriendshipStatus,
    FriendshipStatusShort,
    SentDirectMessage,
    User,
)
from insta_wizard.common.entities.account import AccountSecurity
from insta_wizard.mobile.commands import (
    MediaDelete,
    MediaEdit,
    MediaLike,
    MediaLikers,
    MediaSave,
    MediaUnlike,
    MediaUnsave,
)
from insta_wizard.mobile.commands.account.change_profile_picture import (
    AccountChangeProfilePicture,
)
from insta_wizard.mobile.commands.account.check_phone_number import (
    AccountCheckPhoneNumber,
)
from insta_wizard.mobile.commands.account.create_validated import (
    AccountCreateValidated,
)
from insta_wizard.mobile.commands.account.current_user import (
    AccountCurrentUser,
)
from insta_wizard.mobile.commands.account.edit_profile import (
    AccountEditProfile,
)
from insta_wizard.mobile.commands.account.get_presence_disabled import (
    AccountGetPresenceDisabled,
)
from insta_wizard.mobile.commands.account.logout import AccountsLogout
from insta_wizard.mobile.commands.account.security_info import AccountSecurityInfo
from insta_wizard.mobile.commands.account.send_confirm_email import AccountSendConfirmEmail
from insta_wizard.mobile.commands.account.send_confirm_phone_number import (
    AccountSendConfirmPhoneNumber,
)
from insta_wizard.mobile.commands.account.send_signup_sms_code import (
    AccountSendSignupSmsCode,
)
from insta_wizard.mobile.commands.account.set_biography import (
    AccountSetBiography,
)
from insta_wizard.mobile.commands.account.update_profile_name import (
    AccountUpdateProfileName,
)
from insta_wizard.mobile.commands.account.username_suggestions import (
    AccountUsernameSuggestions,
)
from insta_wizard.mobile.commands.account.validate_signup_sms_code import (
    AccountValidateSignupSmsCode,
)
from insta_wizard.mobile.commands.clips.discover_stream import (
    ClipsDiscoverStream,
)
from insta_wizard.mobile.commands.direct.async_get_pending_requests_preview import (
    DirectV2AsyncGetPendingRequestsPreview,
)
from insta_wizard.mobile.commands.direct.create_group_thread import (
    DirectV2CreateGroupThread,
)
from insta_wizard.mobile.commands.direct.get_pending_requests_preview import (
    DirectV2GetPendingRequestsPreview,
)
from insta_wizard.mobile.commands.direct.get_presence import (
    DirectV2GetPresence,
)
from insta_wizard.mobile.commands.direct.get_presence_active_now import (
    DirectV2GetPresenceActiveNow,
)
from insta_wizard.mobile.commands.direct.has_interop_upgraded import (
    DirectV2HasInteropUpgraded,
)
from insta_wizard.mobile.commands.direct.inbox import (
    DirectV2Inbox,
)
from insta_wizard.mobile.commands.direct.ranked_recipients import (
    DirectV2RankedRecipients,
)
from insta_wizard.mobile.commands.direct.threads_add_user import (
    DirectV2ThreadsAddUser,
)
from insta_wizard.mobile.commands.direct.threads_approve import (
    DirectV2ThreadsApprove,
)
from insta_wizard.mobile.commands.direct.threads_approve_multiple import (
    DirectV2ThreadsApproveMultiple,
)
from insta_wizard.mobile.commands.direct.threads_broadcast_reaction import (
    DirectV2ThreadsBroadcastReaction,
)
from insta_wizard.mobile.commands.direct.threads_broadcast_text import (
    DirectV2ThreadsBroadcastText,
)
from insta_wizard.mobile.commands.direct.threads_decline import (
    DirectV2ThreadsDecline,
)
from insta_wizard.mobile.commands.direct.threads_decline_all import (
    DirectV2ThreadsDeclineAll,
)
from insta_wizard.mobile.commands.direct.threads_decline_multiple import (
    DirectV2ThreadsDeclineMultiple,
)
from insta_wizard.mobile.commands.direct.threads_delete_items_locally import (
    DirectV2ThreadsDeleteItemsLocally,
)
from insta_wizard.mobile.commands.direct.threads_hide import (
    DirectV2ThreadsHide,
)
from insta_wizard.mobile.commands.direct.threads_items_delete import (
    DirectV2ThreadsItemsDelete,
)
from insta_wizard.mobile.commands.direct.threads_items_seen import (
    DirectV2ThreadsItemsSeen,
)
from insta_wizard.mobile.commands.direct.threads_leave import (
    DirectV2ThreadsLeave,
)
from insta_wizard.mobile.commands.direct.threads_mute import (
    DirectV2ThreadsMute,
)
from insta_wizard.mobile.commands.direct.threads_unmute import (
    DirectV2ThreadsUnmute,
)
from insta_wizard.mobile.commands.direct.threads_update_title import (
    DirectV2ThreadsUpdateTitle,
)
from insta_wizard.mobile.commands.feed.get_reels_tray import (
    FeedGetReelsTray,
)
from insta_wizard.mobile.commands.friendships.create import (
    FriendshipsCreate,
)
from insta_wizard.mobile.commands.friendships.destroy import FriendshipsDestroy
from insta_wizard.mobile.commands.friendships.remove_follower import FriendshipsRemoveFollower
from insta_wizard.mobile.commands.friendships.show import FriendshipsShow
from insta_wizard.mobile.commands.friendships.show_many import FriendshipsShowMany
from insta_wizard.mobile.commands.friendships.user_followers import (
    FriendshipsUserFollowers,
)
from insta_wizard.mobile.commands.friendships.user_following import FriendshipsUserFollowing
from insta_wizard.mobile.commands.live.get_good_time_for_live import (
    LiveGetGoodTimeForLive,
)
from insta_wizard.mobile.commands.media.blocked import (
    MediaBlocked,
)
from insta_wizard.mobile.commands.media.comment import MediaComment
from insta_wizard.mobile.commands.media.comment_bulk_delete import MediaCommentBulkDelete
from insta_wizard.mobile.commands.media.comment_like import MediaCommentLike
from insta_wizard.mobile.commands.media.comment_unlike import MediaCommentUnlike
from insta_wizard.mobile.commands.media.comments import MediaComments
from insta_wizard.mobile.commands.news.inbox import (
    NewsInbox,
)
from insta_wizard.mobile.commands.notifications.badge import (
    NotificationsBadge,
)
from insta_wizard.mobile.commands.notifications.get_notification_settings import (
    NotificationsGetNotificationSettings,
)
from insta_wizard.mobile.commands.user.account_details import (
    UserAccountDetails,
)
from insta_wizard.mobile.commands.user.get_limited_interactions_reminder import (
    UserGetLimitedInteractionsReminder,
)
from insta_wizard.mobile.commands.user.info import (
    UserInfo,
)
from insta_wizard.mobile.commands.user.search import (
    UserSearch,
)
from insta_wizard.mobile.commands.user.usernameinfo import (
    UserUsernameInfo,
)
from insta_wizard.mobile.commands.user.web_profile_info import (
    UserWebProfileInfo,
)
from insta_wizard.mobile.common.command import CommandBus
from insta_wizard.mobile.flows import BloksLogin
from insta_wizard.mobile.models.state import MobileClientState
from insta_wizard.mobile.responses.account.account_check_phone_number import (
    AccountCheckPhoneNumberResponse,
)
from insta_wizard.mobile.responses.account.account_create_validated import (
    AccountCreateValidatedResponse,
)
from insta_wizard.mobile.responses.account.account_get_presence_disabled import (
    AccountGetPresenceDisabledResponse,
)
from insta_wizard.mobile.responses.account.account_send_confirm_email import (
    AccountSendConfirmEmailResponse,
)
from insta_wizard.mobile.responses.account.account_send_confirm_phone_number import (
    AccountSendConfirmPhoneNumberResponse,
)
from insta_wizard.mobile.responses.account.account_send_signup_sms_code import (
    AccountSendSignupSmsCodeResponse,
)
from insta_wizard.mobile.responses.account.account_validate_signup_sms_code import (
    AccountValidateSignupSmsCodeResponse,
)
from insta_wizard.mobile.responses.clips.discover_stream import ClipsDiscoverStreamResponse
from insta_wizard.mobile.responses.direct.async_get_pending_requests_preview import (
    DirectV2AsyncGetPendingRequestsPreviewResponse,
)
from insta_wizard.mobile.responses.direct.create_group_thread import (
    DirectV2CreateGroupThreadResponse,
)
from insta_wizard.mobile.responses.direct.get_pending_requests_preview import (
    DirectV2GetPendingRequestsPreviewResponse,
)
from insta_wizard.mobile.responses.direct.get_presence import DirectV2GetPresenceResponse
from insta_wizard.mobile.responses.direct.get_presence_active_now import (
    DirectV2GetPresenceActiveNowResponse,
)
from insta_wizard.mobile.responses.direct.has_interop_upgraded import (
    DirectV2HasInteropUpgradedResponse,
)
from insta_wizard.mobile.responses.direct.ranked_recipients import DirectV2RankedRecipientsResponse
from insta_wizard.mobile.responses.feed.reels_tray import FeedGetReelsTrayResponse
from insta_wizard.mobile.responses.news.inbox import NewsInboxResponse
from insta_wizard.mobile.responses.notifications.badge import NotificationsBadgeResponse
from insta_wizard.mobile.responses.notifications.get_notification_settings import (
    NotificationsGetNotificationSettingsResponse,
)
from insta_wizard.mobile.responses.user.account_details import UserAccountDetailsResponse
from insta_wizard.mobile.responses.user.get_limited_interactions_reminder import (
    UserGetLimitedInteractionsReminderResponse,
)
from insta_wizard.mobile.responses.user.web_profile_info import UserWebProfileInfoResponse


class BaseSection:
    def __init__(
        self,
        state: MobileClientState,
        bus: CommandBus,
    ):
        self.state = state
        self.bus = bus


class AccountSection(BaseSection):
    async def get_current_user(self) -> Account:
        """Get current user info (requires authentication)"""
        raw = await self.bus.execute(AccountCurrentUser())
        return Account.model_validate(raw["user"])

    async def get_security_info(self) -> AccountSecurity:
        raw = await self.bus.execute(AccountSecurityInfo())
        return AccountSecurity.model_validate(raw)

    async def edit_profile(
        self,
        username,
        first_name,
        biography,
        external_url,
        email,
        phone_number,
        gender,
    ) -> None:
        """Edit account info (requires authentication)"""
        await self.bus.execute(
            AccountEditProfile(
                username=username,
                first_name=first_name,
                biography=biography,
                external_url=external_url,
                email=email,
                phone_number=phone_number,
                gender=gender,
            )
        )

    async def update_profile_name(self, first_name: str) -> None:
        """Update account profile name"""
        await self.bus.execute(AccountUpdateProfileName(first_name=first_name))

    async def set_bio(self, bio_text: str) -> None:
        """Update account biography"""
        await self.bus.execute(AccountSetBiography(bio_text=bio_text))

    async def set_profile_picture(self, upload_id) -> None:
        """Set account profile picture (requires upload_id)"""
        await self.bus.execute(AccountChangeProfilePicture(upload_id=str(upload_id)))

    async def get_presence_disabled(self) -> AccountGetPresenceDisabledResponse:
        return await self.bus.execute(AccountGetPresenceDisabled())

    async def login(self, username: str, password: str) -> None:
        """Log in with username and password"""
        await self.bus.execute(BloksLogin(username=username, password=password))

    async def logout(self) -> None:
        """Logout of account"""
        if not self.state.local_data.authorization:
            return
        await self.bus.execute(AccountsLogout())

    async def check_phone_number(self, phone_number: str) -> AccountCheckPhoneNumberResponse:
        """Check if phone number is available"""
        return await self.bus.execute(AccountCheckPhoneNumber(phone_number=phone_number))

    async def send_signup_sms_code(self, phone_number: str) -> AccountSendSignupSmsCodeResponse:
        """Request SMS code for account registration"""
        return await self.bus.execute(AccountSendSignupSmsCode(phone_number=phone_number))

    async def validate_signup_sms_code(
        self, phone_number: str, code: int | str
    ) -> AccountValidateSignupSmsCodeResponse:
        """Submit SMS verification code during account registration"""
        return await self.bus.execute(
            AccountValidateSignupSmsCode(phone_number=phone_number, code=code)
        )

    async def get_username_suggestions(self, username: str):
        return await self.bus.execute(AccountUsernameSuggestions(username=username))

    async def create_validated(
        self,
        username: str,
        password: str,
        first_name: str,
        code: int | str,
        phone_number: str,
        day: int,
        month: int,
        year: int,
        tos_version: str = "row",
    ) -> AccountCreateValidatedResponse:
        return await self.bus.execute(
            AccountCreateValidated(
                username=username,
                password=password,
                first_name=first_name,
                code=code,
                phone_number=phone_number,
                day=day,
                month=month,
                year=year,
                tos_version=tos_version,
            )
        )

    async def send_confirm_email(self, email: str) -> AccountSendConfirmEmailResponse:
        """Set account email and send confirmation link"""
        return await self.bus.execute(AccountSendConfirmEmail(email=email))

    async def send_confirm_phone_number(
        self, phone_number: str
    ) -> AccountSendConfirmPhoneNumberResponse:
        """Set account phone number and send confirmation code"""
        return await self.bus.execute(AccountSendConfirmPhoneNumber(phone_number=phone_number))


class ClipSection(BaseSection):
    async def get_stream(self) -> ClipsDiscoverStreamResponse:
        return await self.bus.execute(ClipsDiscoverStream())


class DirectSection(BaseSection):
    async def get_inbox(self) -> list[DirectThread]:
        """Get direct inbox threads"""
        raw = await self.bus.execute(DirectV2Inbox())
        return [DirectThread.model_validate(t) for t in raw["inbox"]["threads"]]

    async def get_pending(self) -> DirectV2GetPendingRequestsPreviewResponse:
        return await self.bus.execute(DirectV2GetPendingRequestsPreview())

    async def get_presence(self) -> DirectV2GetPresenceResponse:
        return await self.bus.execute(DirectV2GetPresence())

    async def get_presence_active_now(self) -> DirectV2GetPresenceActiveNowResponse:
        return await self.bus.execute(DirectV2GetPresenceActiveNow())

    async def get_ranked_recipients(
        self, mode: Literal["raven", "reshare"] = "raven"
    ) -> DirectV2RankedRecipientsResponse:
        return await self.bus.execute(DirectV2RankedRecipients(mode=mode))

    async def create_group_thread(
        self, recipient_users: list[str], thread_title: str
    ) -> DirectV2CreateGroupThreadResponse:
        return await self.bus.execute(
            DirectV2CreateGroupThread(
                recipient_users=recipient_users,
                thread_title=thread_title,
            )
        )

    async def approve_thread(self, thread_id: str) -> None:
        await self.bus.execute(DirectV2ThreadsApprove(thread_id=thread_id))

    async def approve_multiple_threads(self, thread_ids: list[str]) -> None:
        await self.bus.execute(DirectV2ThreadsApproveMultiple(thread_ids=thread_ids))

    async def decline_thread(self, thread_id: str) -> None:
        await self.bus.execute(DirectV2ThreadsDecline(thread_id=thread_id))

    async def decline_multiple_threads(self, thread_ids: list[str]) -> None:
        await self.bus.execute(DirectV2ThreadsDeclineMultiple(thread_ids=thread_ids))

    async def decline_all_threads(self, thread_ids: list[str]) -> None:
        await self.bus.execute(DirectV2ThreadsDeclineAll(thread_ids=thread_ids))

    async def delete_thread_item(self, thread_id: str, item_id: str) -> None:
        await self.bus.execute(DirectV2ThreadsItemsDelete(thread_id=thread_id, item_id=item_id))

    async def mark_thread_item_seen(self, thread_id: str, item_id: str) -> None:
        await self.bus.execute(DirectV2ThreadsItemsSeen(thread_id=thread_id, item_id=item_id))

    async def leave_thread(self, thread_id: str) -> None:
        await self.bus.execute(DirectV2ThreadsLeave(thread_id=thread_id))

    async def mute_thread(self, thread_id: str) -> None:
        await self.bus.execute(DirectV2ThreadsMute(thread_id=thread_id))

    async def unmute_thread(self, thread_id: str) -> None:
        await self.bus.execute(DirectV2ThreadsUnmute(thread_id=thread_id))

    async def hide_thread(self, thread_id: str) -> None:
        await self.bus.execute(DirectV2ThreadsHide(thread_id=thread_id))

    async def update_thread_title(self, thread_id: str, title: str) -> None:
        await self.bus.execute(DirectV2ThreadsUpdateTitle(thread_id=thread_id, title=title))

    async def add_user_to_thread(self, thread_id: str, user_ids: list[str | int]) -> None:
        await self.bus.execute(DirectV2ThreadsAddUser(thread_id=thread_id, user_ids=user_ids))

    async def send_message(self, user_ids: list[str], text: str) -> SentDirectMessage:
        """Send a text message to users"""
        raw = await self.bus.execute(
            DirectV2ThreadsBroadcastText(recipient_users=user_ids, text=text)
        )
        return SentDirectMessage.model_validate(raw["payload"])

    async def send_reaction(
        self,
        thread_ids: list[str],
        item_id: str,
        reaction_type: str,
        reaction_action_source: str,
    ) -> None:
        await self.bus.execute(
            DirectV2ThreadsBroadcastReaction(
                thread_ids=thread_ids,
                item_id=item_id,
                reaction_type=reaction_type,
                reaction_action_source=reaction_action_source,
            )
        )

    async def delete_thread_items_locally(self, thread_id: str, item_ids: list[str]) -> None:
        await self.bus.execute(
            DirectV2ThreadsDeleteItemsLocally(thread_id=thread_id, item_ids=item_ids)
        )

    async def get_pending_async(self) -> DirectV2AsyncGetPendingRequestsPreviewResponse:
        return await self.bus.execute(DirectV2AsyncGetPendingRequestsPreview())

    async def has_interop_upgraded(self) -> DirectV2HasInteropUpgradedResponse:
        return await self.bus.execute(DirectV2HasInteropUpgraded())


class FeedSection(BaseSection):
    async def get_stories_tray(self) -> FeedGetReelsTrayResponse:
        return await self.bus.execute(FeedGetReelsTray())

    # async def get_timeline(self) -> FeedTimelineIApiResponse:
    #     return await self.bus.execute(FeedTimelineIApi())

    # async def get_suggested_reels(self):
    #     return await self.bus.execute(FeedInjectedReelsMedia())


class FriendshipsSection(BaseSection):
    async def follow(self, user_id: str) -> None:
        """Follow a user"""
        await self.bus.execute(FriendshipsCreate(user_id=user_id))

    async def unfollow(self, user_id: str) -> None:
        """Unfollow a user"""
        await self.bus.execute(FriendshipsDestroy(user_id=user_id))

    async def remove_follower(self, user_id: str) -> None:
        """Remove a user from your followers"""
        await self.bus.execute(FriendshipsRemoveFollower(user_id=user_id))

    async def get_user_followers(
        self,
        user_id: str,
        query: str | None = None,
        max_id: int | None = None,
    ) -> list[User]:
        """Get user followers (supports search via query parameter)"""
        raw = await self.bus.execute(
            FriendshipsUserFollowers(
                user_id=user_id,
                query=query,
                max_id=max_id,
            )
        )
        return [User.model_validate(u) for u in raw["users"]]

    async def get_user_following(
        self,
        user_id: str,
        query: str | None = None,
        max_id: int | None = None,
    ) -> list[User]:
        """Get user following list (supports search via query parameter)"""
        raw = await self.bus.execute(
            FriendshipsUserFollowing(
                user_id=user_id,
                query=query,
                max_id=max_id,
            )
        )
        return [User.model_validate(u) for u in raw["users"]]

    async def get_status(self, user_id: str) -> FriendshipStatus:
        """Get friendship status with a user"""
        raw = await self.bus.execute(FriendshipsShow(user_id=user_id))
        return FriendshipStatus.model_validate(raw)

    async def get_status_many(self, user_ids: list[str]) -> dict[str, FriendshipStatusShort]:
        """Get friendship status for multiple users"""
        raw = await self.bus.execute(FriendshipsShowMany(user_ids=user_ids))
        return {
            user_id: FriendshipStatusShort.model_validate(status)
            for user_id, status in raw["friendship_statuses"].items()
        }


class LiveSection(BaseSection):
    async def get_good_time_for_live(self) -> None:
        await self.bus.execute(LiveGetGoodTimeForLive())


class MediaSection(BaseSection):
    async def like(self, media_id: str) -> None:
        """Like the media"""
        await self.bus.execute(MediaLike(media_id=media_id))

    async def unlike(self, media_id: str) -> None:
        """Unlike the media"""
        await self.bus.execute(MediaUnlike(media_id=media_id))

    async def delete(self, media_id: str) -> None:
        """Delete the media"""
        await self.bus.execute(MediaDelete(media_id=media_id))

    async def edit(self, media_id: str, caption_text: str) -> None:
        """Edit the media"""
        await self.bus.execute(MediaEdit(media_id=media_id, caption_text=caption_text))

    async def save(self, media_id: str) -> None:
        """Save the media"""
        await self.bus.execute(MediaSave(media_id=media_id))

    async def unsave(self, media_id: str) -> None:
        """Unsave the media"""
        await self.bus.execute(MediaUnsave(media_id=media_id))

    async def get_likers(self, media_id: str) -> list[User]:
        """Get media likers"""
        raw = await self.bus.execute(MediaLikers(media_id=media_id))
        return [User.model_validate(u) for u in raw["users"]]

    async def get_blocked(self) -> list[str]:
        """Get blocked media (list of media ids)"""
        raw = await self.bus.execute(MediaBlocked())
        return [media_id for media_id in raw["media_ids"]]

    async def get_comments(
        self,
        media_id: str,
        min_id: str = None,
        max_id: str = None,
    ) -> list[Comment]:
        """Get comments for a media"""
        raw = await self.bus.execute(
            MediaComments(
                media_id=media_id,
                min_id=min_id,
                max_id=max_id,
            )
        )
        return [Comment.model_validate(c) for c in raw["comments"]]

    async def add_comment(
        self,
        media_id: str,
        text: str,
        replied_to_comment_id: str | None = None,
    ) -> Comment:
        """Post a comment on a media"""
        raw = await self.bus.execute(
            MediaComment(
                media_id=media_id,
                text=text,
                replied_to_comment_id=replied_to_comment_id,
            )
        )
        return Comment.model_validate(raw["comment"])

    async def delete_comments(self, media_id: str, comment_ids: list[str]) -> None:
        """Delete comments on media"""
        await self.bus.execute(MediaCommentBulkDelete(media_id=media_id, comment_ids=comment_ids))

    async def like_comment(self, comment_id: str) -> None:
        """Like a comment"""
        await self.bus.execute(MediaCommentLike(comment_id=comment_id))

    async def unlike_comment(self, comment_id: str) -> None:
        """Unlike a comment"""
        await self.bus.execute(MediaCommentUnlike(comment_id=comment_id))


class NewsSection(BaseSection):
    async def get_inbox(self) -> NewsInboxResponse:
        return await self.bus.execute(NewsInbox())


class NotificationSection(BaseSection):
    async def get_settings(self) -> NotificationsGetNotificationSettingsResponse:
        return await self.bus.execute(NotificationsGetNotificationSettings())

    async def get_badge(self) -> NotificationsBadgeResponse:
        return await self.bus.execute(NotificationsBadge())


class UserSection(BaseSection):
    async def get_info(self, user_id: str) -> User:
        """Get user info by user_id"""
        raw = await self.bus.execute(UserInfo(user_id=user_id))
        return User.model_validate(raw["user"])

    async def get_info_by_username(self, username: str) -> User:
        """Get user info by username"""
        raw = await self.bus.execute(UserUsernameInfo(username=username))
        return User.model_validate(raw["user"])

    async def get_web_profile(self, username: str) -> UserWebProfileInfoResponse:
        """Get user info by username (webprofileinfo)"""
        return await self.bus.execute(UserWebProfileInfo(username=username))

    async def search(self, query: str, count: int = 30) -> list[User]:
        """Search users by query"""
        raw = await self.bus.execute(UserSearch(query=query, count=count))
        return [User.model_validate(u) for u in raw["users"]]

    async def get_details(self, user_id: str | int) -> UserAccountDetailsResponse:
        return await self.bus.execute(UserAccountDetails(user_id=user_id))

    async def get_limited_interactions_reminder(self) -> UserGetLimitedInteractionsReminderResponse:
        return await self.bus.execute(UserGetLimitedInteractionsReminder())
