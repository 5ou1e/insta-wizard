from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.web.commands.account.check_age_eligibility import (
    CheckAgeEligibility,
)
from insta_wizard.web.commands.account.edit import (
    AccountsEdit,
)
from insta_wizard.web.commands.account.edit_web_form_data import (
    AccountsEditWebFormData,
)
from insta_wizard.web.commands.account.login_ajax import (
    AccountsLoginAjax,
)
from insta_wizard.web.commands.account.recovery_send_ajax import (
    AccountRecoverySendAjax,
)
from insta_wizard.web.commands.account.send_sms_code_ajax import (
    SendSignupSmsCodeAjax,
)
from insta_wizard.web.commands.account.web_create_ajax import (
    WebCreateAjax,
)
from insta_wizard.web.commands.account.web_create_ajax_attempt import (
    WebCreateAjaxAttempt,
)
from insta_wizard.web.commands.comments.comments_add import (
    CommentsAdd,
)
from insta_wizard.web.commands.comments.comments_like import (
    CommentsLike,
)
from insta_wizard.web.commands.comments.comments_unlike import (
    CommentsUnlike,
)
from insta_wizard.web.commands.friendships.create import (
    FriendshipsCreate,
)
from insta_wizard.web.commands.friendships.destroy import (
    FriendshipsDestroy,
)
from insta_wizard.web.commands.friendships.follow import (
    FriendshipsFollow,
)
from insta_wizard.web.commands.likes.likes_like import (
    LikesLike,
)
from insta_wizard.web.commands.likes.likes_unlike import (
    LikesUnlike,
)
from insta_wizard.web.commands.navigation.get_email_signup_page import (
    GetEmailSignupPage,
)
from insta_wizard.web.commands.navigation.get_home_page import (
    GetInstagramHomePage,
)
from insta_wizard.web.commands.navigation.get_shared_data import (
    GetSharedData,
)
from insta_wizard.web.commands.navigation.get_web_mid import (
    GetWebMid,
)
from insta_wizard.web.commands.navigation.navigate import (
    Navigate,
)
from insta_wizard.web.common.command import CommandBus
from insta_wizard.web.responses.account.check_age_eligibility import CheckAgeEligibilityResponse
from insta_wizard.web.responses.account.edit_web_form_data import AccountsEditWebFormDataResponse
from insta_wizard.web.responses.account.recovery_send_ajax import AccountRecoverySendAjaxResponse
from insta_wizard.web.responses.account.send_sms_code_ajax import SendSignupSmsCodeAjaxResponse
from insta_wizard.web.responses.account.web_create_ajax import WebCreateAjaxResponse
from insta_wizard.web.responses.account.web_create_ajax_attempt import WebCreateAjaxAttemptResponse
from insta_wizard.web.responses.comments.comments_add import CommentsAddResponse
from insta_wizard.web.responses.navigation.get_shared_data import GetSharedDataResponse


class BaseSection:
    def __init__(
        self,
        logger: InstagramClientLogger,
        bus: CommandBus,
    ):
        self.logger = logger
        self.bus = bus


class AccountSection(BaseSection):
    async def edit(
        self,
        biography: str | None,
        chaining_enabled: bool,
        external_url: str | None,
        first_name: str,
        username: str,
    ) -> None:
        """Edit account profile"""
        await self.bus.execute(
            AccountsEdit(
                biography=biography,
                chaining_enabled=chaining_enabled,
                external_url=external_url,
                first_name=first_name,
                username=username,
            )
        )

    async def get_edit_form_data(self) -> AccountsEditWebFormDataResponse:
        """Get account data from the profile edit page"""
        return await self.bus.execute(AccountsEditWebFormData())

    async def check_age_eligibility(
        self, day: int, month: int, year: int
    ) -> CheckAgeEligibilityResponse:
        """Check if registration is allowed with the given birthdate"""
        return await self.bus.execute(CheckAgeEligibility(day=day, month=month, year=year))

    async def recovery_send_ajax(self, email_or_username: str) -> AccountRecoverySendAjaxResponse:
        """Send password recovery link to email"""
        return await self.bus.execute(AccountRecoverySendAjax(email_or_username=email_or_username))

    async def login_ajax(self, username: str, enc_password: str, jazoest: str) -> None:
        """Log in with username and password"""
        await self.bus.execute(
            AccountsLoginAjax(
                username=username,
                enc_password=enc_password,
                jazoest=jazoest,
            )
        )

    async def send_sms_code_ajax(
        self,
        phone_number: str,
        captcha_token: str | None = None,
    ) -> SendSignupSmsCodeAjaxResponse:
        """Send SMS code during registration"""
        return await self.bus.execute(
            SendSignupSmsCodeAjax(
                phone_number=phone_number,
                captcha_token=captcha_token,
            )
        )

    async def web_create_ajax(
        self,
        username: str,
        password: str,
        first_name: str,
        phone_number: str,
        day: int,
        month: int,
        year: int,
        sms_code: int | str,
    ) -> WebCreateAjaxResponse:
        """Final account registration request"""
        return await self.bus.execute(
            WebCreateAjax(
                username=username,
                password=password,
                first_name=first_name,
                phone_number=phone_number,
                day=day,
                month=month,
                year=year,
                sms_code=sms_code,
            )
        )

    async def web_create_ajax_attempt(
        self,
        username: str,
        password: str,
        first_name: str,
        phone_number: str,
    ) -> WebCreateAjaxAttemptResponse:
        """Send account registration attempt request"""
        return await self.bus.execute(
            WebCreateAjaxAttempt(
                username=username,
                password=password,
                first_name=first_name,
                phone_number=phone_number,
            )
        )


class CommentsSection(BaseSection):
    async def add(
        self,
        media_id: str,
        text: str,
        replied_to_comment_id: str | None = None,
    ) -> CommentsAddResponse:
        """Add a comment to a media post"""
        return await self.bus.execute(
            CommentsAdd(
                media_id=media_id,
                replied_to_comment_id=replied_to_comment_id,
                text=text,
            )
        )

    async def like(self, comment_id: str) -> None:
        """Like a comment on a media post"""
        await self.bus.execute(CommentsLike(comment_id=comment_id))

    async def unlike(self, comment_id: str) -> None:
        """Unlike a comment on a media post"""
        await self.bus.execute(CommentsUnlike(comment_id=comment_id))


class FriendshipsSection(BaseSection):
    async def create(self, user_id: str) -> None:
        """Follow a user"""
        await self.bus.execute(FriendshipsCreate(user_id=user_id))

    async def follow(self, user_id: str) -> None:
        """Follow a user"""
        await self.bus.execute(FriendshipsFollow(user_id=user_id))

    async def unfollow(self, user_id: str) -> None:
        """Unfollow a user"""
        await self.bus.execute(FriendshipsDestroy(user_id=user_id))


class LikesSection(BaseSection):
    async def like(self, media_id: str) -> None:
        """Like a media post"""
        await self.bus.execute(LikesLike(media_id=media_id))

    async def unlike(self, media_id: str) -> None:
        """Unlike a media post"""
        await self.bus.execute(LikesUnlike(media_id=media_id))


class NavigationSection(BaseSection):
    async def navigate(self, url: str) -> str:
        """Navigate to some url"""
        return await self.bus.execute(Navigate(url=url))

    async def get_home_page(self) -> str:
        """Navigate to the Instagram home page"""
        return await self.bus.execute(GetInstagramHomePage())

    async def get_shared_data(self) -> GetSharedDataResponse:
        """Get SharedData configs"""
        return await self.bus.execute(GetSharedData())

    async def get_web_mid(self) -> str:
        return await self.bus.execute(GetWebMid())

    async def get_email_signup_page(self) -> str:
        """Navigate to the registration page"""
        return await self.bus.execute(GetEmailSignupPage())
