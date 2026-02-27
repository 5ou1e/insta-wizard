from typing import Literal

from insta_wizard.mobile.commands import (
    MediaLike,
    MediaUnlike,
    MediaDelete,
    MediaEdit,
    MediaLikers,
    MediaSave,
)
from insta_wizard.mobile.commands._responses.friendships.friendships_user_followers import (
    FriendshipsUserFollowersResponse,
)
from insta_wizard.mobile.commands._responses.friendships.friendships_user_following import (
    FriendshipsUserFollowingResponse,
)
from insta_wizard.mobile.commands._responses.user.user_info import (
    UserInfoResponse,
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
from insta_wizard.mobile.commands.feed.get_feed_timeline_i_api import (
    FeedGetFeedTimelineIApi,
)
from insta_wizard.mobile.commands.feed.get_reels_tray import (
    FeedGetReelsTray,
)
from insta_wizard.mobile.commands.feed.injected_reels_media import (
    FeedInjectedReelsMedia,
)
from insta_wizard.mobile.commands.friendships.create import (
    FriendshipsCreate,
)
from insta_wizard.mobile.commands.friendships.destroy import FriendshipsDestroy
from insta_wizard.mobile.commands.friendships.remove_follower import FriendshipsRemoveFollower
from insta_wizard.mobile.commands.friendships.show import FriendshipsShow
from insta_wizard.mobile.commands.friendships.show_many import (
    FriendshipsShowMany,
    FriendshipsShowManyResponse,
)
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
from insta_wizard.mobile.commands.news.news_inbox import (
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
from insta_wizard.mobile.commands.user.get_user_info_by_id import (
    UserInfo,
)
from insta_wizard.mobile.commands.user.get_user_info_by_username import (
    UserUsernameInfo,
)
from insta_wizard.mobile.commands.user.search import (
    UserSearchUsers,
)
from insta_wizard.mobile.commands.user.web_profile_info import (
    UserWebProfileInfo,
)
from insta_wizard.mobile.common.command import CommandBus
from insta_wizard.mobile.flows import BloksLogin
from insta_wizard.mobile.models.state import MobileClientState


class BaseSection:
    def __init__(
        self,
        state: MobileClientState,
        bus: CommandBus,
    ):
        self.state = state
        self.bus = bus


class AccountSection(BaseSection):
    async def get_current_user(self):
        """Get current user info (requires authentication)"""
        return await self.bus.execute(AccountCurrentUser())

    async def edit_profile(
        self,
        username,
        first_name,
        biography,
        external_url,
        email,
        phone_number,
        gender,
    ):
        """Edit account info (requires authentication)"""
        return await self.bus.execute(
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

    async def update_profile_name(self, first_name: str):
        """Update account profile name"""
        return await self.bus.execute(AccountUpdateProfileName(first_name=first_name))

    async def set_bio(self, bio_text: str):
        """Update account biography"""
        return await self.bus.execute(AccountSetBiography(bio_text=bio_text))

    async def set_profile_picture(self, upload_id):
        """Set account profile picture (requires upload_id)"""
        return await self.bus.execute(AccountChangeProfilePicture(upload_id=str(upload_id)))

    async def get_presence_disabled(self):
        return await self.bus.execute(AccountGetPresenceDisabled())

    async def login(self, username: str, password: str) -> None:
        """Log in with username and password"""
        await self.bus.execute(BloksLogin(username=username, password=password))

    async def logout(self) -> None:
        """Logout of account"""
        if not self.state.local_data.authorization:
            return
        await self.bus.execute(AccountsLogout())

    async def check_phone_number(self, phone_number: str):
        """Check if phone number is available"""
        return await self.bus.execute(AccountCheckPhoneNumber(phone_number=phone_number))

    async def send_signup_sms_code(self, phone_number: str):
        """Request SMS code for account registration"""
        return await self.bus.execute(AccountSendSignupSmsCode(phone_number=phone_number))

    async def validate_signup_sms_code(self, phone_number: str, code: int | str):
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
    ):
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

    async def get_security_info(self):
        return await self.bus.execute(AccountSecurityInfo())

    async def send_confirm_email(self, email: str):
        """Set account email and send confirmation link"""
        return await self.bus.execute(AccountSendConfirmEmail(email=email))

    async def send_confirm_phone_number(self, phone_number: str) -> dict:
        """Set account phone number and send confirmation code"""
        return await self.bus.execute(AccountSendConfirmPhoneNumber(phone_number=phone_number))


class ClipSection(BaseSection):
    async def get_stream(self):
        return await self.bus.execute(ClipsDiscoverStream())


class DirectSection(BaseSection):
    async def get_presence(self):
        return await self.bus.execute(DirectV2GetPresence())

    async def get_pending(self):
        return await self.bus.execute(DirectV2GetPendingRequestsPreview())

    async def get_inbox(self):
        return await self.bus.execute(DirectV2Inbox())

    async def get_presence_active_now(self):
        return await self.bus.execute(DirectV2GetPresenceActiveNow())

    async def get_ranked_recipients(self, mode: Literal["raven", "reshare"] = "raven"):
        return await self.bus.execute(DirectV2RankedRecipients(mode=mode))

    async def create_group_thread(self, recipient_users: list[str], thread_title: str):
        return await self.bus.execute(
            DirectV2CreateGroupThread(
                recipient_users=recipient_users,
                thread_title=thread_title,
            )
        )

    async def approve_thread(self, thread_id: str):
        return await self.bus.execute(DirectV2ThreadsApprove(thread_id=thread_id))

    async def approve_multiple_threads(self, thread_ids: list[str]):
        return await self.bus.execute(DirectV2ThreadsApproveMultiple(thread_ids=thread_ids))

    async def decline_thread(self, thread_id: str):
        return await self.bus.execute(DirectV2ThreadsDecline(thread_id=thread_id))

    async def decline_multiple_threads(self, thread_ids: list[str]):
        return await self.bus.execute(DirectV2ThreadsDeclineMultiple(thread_ids=thread_ids))

    async def decline_all_threads(self, thread_ids: list[str]):
        return await self.bus.execute(DirectV2ThreadsDeclineAll(thread_ids=thread_ids))

    async def hide_thread(self, thread_id: str):
        return await self.bus.execute(DirectV2ThreadsHide(thread_id=thread_id))

    async def delete_thread_item(self, thread_id: str, item_id: str):
        return await self.bus.execute(
            DirectV2ThreadsItemsDelete(thread_id=thread_id, item_id=item_id)
        )

    async def mark_thread_item_seen(self, thread_id: str, item_id: str):
        return await self.bus.execute(
            DirectV2ThreadsItemsSeen(thread_id=thread_id, item_id=item_id)
        )

    async def leave_thread(self, thread_id: str):
        return await self.bus.execute(DirectV2ThreadsLeave(thread_id=thread_id))

    async def mute_thread(self, thread_id: str):
        return await self.bus.execute(DirectV2ThreadsMute(thread_id=thread_id))

    async def unmute_thread(self, thread_id: str):
        return await self.bus.execute(DirectV2ThreadsUnmute(thread_id=thread_id))

    async def update_thread_title(self, thread_id: str, title: str):
        return await self.bus.execute(DirectV2ThreadsUpdateTitle(thread_id=thread_id, title=title))

    async def add_user_to_thread(self, thread_id: str, user_ids: list[str | int]):
        return await self.bus.execute(
            DirectV2ThreadsAddUser(thread_id=thread_id, user_ids=user_ids)
        )

    async def send_message(self, recipient_users: list[str], text: str):
        """Send a text message to users"""
        return await self.bus.execute(
            DirectV2ThreadsBroadcastText(recipient_users=recipient_users, text=text)
        )

    async def send_reaction(
        self,
        thread_ids: list[str],
        item_id: str,
        reaction_type: str,
        reaction_action_source: str,
    ):
        return await self.bus.execute(
            DirectV2ThreadsBroadcastReaction(
                thread_ids=thread_ids,
                item_id=item_id,
                reaction_type=reaction_type,
                reaction_action_source=reaction_action_source,
            )
        )

    async def delete_thread_items_locally(self, thread_id: str, item_ids: list[str]):
        return await self.bus.execute(
            DirectV2ThreadsDeleteItemsLocally(thread_id=thread_id, item_ids=item_ids)
        )

    async def get_pending_async(self):
        return await self.bus.execute(DirectV2AsyncGetPendingRequestsPreview())

    async def has_interop_upgraded(self):
        return await self.bus.execute(DirectV2HasInteropUpgraded())


class FeedSection(BaseSection):
    async def get_timeline(self):
        return await self.bus.execute(FeedGetFeedTimelineIApi())

    async def get_stories_tray(self):
        return await self.bus.execute(FeedGetReelsTray())

    async def get_suggested_reels(self):
        return await self.bus.execute(FeedInjectedReelsMedia())


class FriendshipsSection(BaseSection):
    async def follow(self, user_id: str):
        """Follow a user"""
        return await self.bus.execute(FriendshipsCreate(user_id=user_id))

    async def unfollow(self, user_id: str):
        """Unfollow a user"""
        return await self.bus.execute(FriendshipsDestroy(user_id=user_id))

    async def remove_follower(self, user_id: str):
        """Remove a user from your followers"""
        return await self.bus.execute(FriendshipsRemoveFollower(user_id=user_id))

    async def get_user_followers(
        self,
        user_id: str,
        query: str | None = None,
        max_id: int | None = None,
    ) -> FriendshipsUserFollowersResponse:
        """Get user followers (supports search via query parameter)"""
        return await self.bus.execute(
            FriendshipsUserFollowers(
                user_id=user_id,
                query=query,
                max_id=max_id,
            )
        )

    async def get_user_following(
        self,
        user_id: str,
        query: str | None = None,
        max_id: int | None = None,
    ) -> FriendshipsUserFollowingResponse:
        """Get user following list (supports search via query parameter)"""
        return await self.bus.execute(
            FriendshipsUserFollowing(
                user_id=user_id,
                query=query,
                max_id=max_id,
            )
        )

    async def get_status(self, user_ids: list[str | int]) -> FriendshipsShowManyResponse:
        """Get friendship status for multiple users"""
        return await self.bus.execute(FriendshipsShowMany(user_ids=user_ids))

    async def get_status_single(self, user_id: str | int):
        """Get friendship status with a user"""
        return await self.bus.execute(FriendshipsShow(user_id=user_id))


class LiveSection(BaseSection):
    async def get_good_time(self):
        return await self.bus.execute(LiveGetGoodTimeForLive())


class MediaSection(BaseSection):
    async def like(self, media_id: str):
        """Like the media"""
        return await self.bus.execute(MediaLike(media_id=media_id))

    async def unlike(self, media_id: str):
        """Unlike the media"""
        return await self.bus.execute(MediaUnlike(media_id=media_id))

    async def delete(self, media_id: str):
        """Delete the media"""
        return await self.bus.execute(MediaDelete(media_id=media_id))

    async def edit(self, media_id: str, caption_text: str):
        """Edit the media"""
        return await self.bus.execute(MediaEdit(media_id=media_id, caption_text=caption_text))

    async def save(self, media_id: str):
        """Save the media"""
        return await self.bus.execute(MediaSave(media_id=media_id))

    async def get_likers(self, media_id: str):
        """Get media likers"""
        return await self.bus.execute(MediaLikers(media_id=media_id))

    async def get_blocked(self):
        return await self.bus.execute(MediaBlocked())

    async def get_comments(
        self,
        media_id: str,
        min_id: str = None,
        max_id: str = None,
    ):
        """Get comments for a media post"""
        return await self.bus.execute(
            MediaComments(
                media_id=media_id,
                min_id=min_id,
                max_id=max_id,
            )
        )

    async def add_comment(
        self,
        media_id: str,
        comment_text: str,
        replied_to_comment_id: str | None = None,
    ):
        """Post a comment on a media"""
        await self.bus.execute(
            MediaComment(
                media_id=media_id,
                comment_text=comment_text,
                replied_to_comment_id=replied_to_comment_id,
            )
        )

    async def delete_comments(self, media_id: str, comment_ids: list[str]):
        """Delete comments on media"""
        return await self.bus.execute(
            MediaCommentBulkDelete(media_id=media_id, comment_ids=comment_ids)
        )

    async def like_comment(self, comment_id: int):
        """Like a comment"""
        return await self.bus.execute(MediaCommentLike(comment_id=comment_id))

    async def unlike_comment(self, comment_id: int):
        """Unlike a comment"""
        return await self.bus.execute(MediaCommentUnlike(comment_id=comment_id))


class NewsSection(BaseSection):
    async def get_inbox(self):
        return await self.bus.execute(NewsInbox())


class NotificationSection(BaseSection):
    async def get_settings(self):
        return await self.bus.execute(NotificationsGetNotificationSettings())

    async def get_badge(self):
        return await self.bus.execute(NotificationsBadge())


class UserSection(BaseSection):
    async def get_info(self, user_id: str) -> UserInfoResponse:
        """Get user info by user_id"""
        return await self.bus.execute(UserInfo(user_id=user_id))

    async def get_info_by_username(self, username: str):
        """Get user info by username"""
        return await self.bus.execute(UserUsernameInfo(username=username))

    async def get_web_profile(self, username: str):
        """Get user info by username (webprofileinfo)"""
        return await self.bus.execute(UserWebProfileInfo(username=username))

    async def get_limited_interactions_reminder(self):
        return await self.bus.execute(UserGetLimitedInteractionsReminder())

    async def search(self, username: str, count: int = 30):
        return await self.bus.execute(UserSearchUsers(query=username, count=count))

    async def get_details(self, user_id: str | int):
        return await self.bus.execute(UserAccountDetails(user_id=user_id))
