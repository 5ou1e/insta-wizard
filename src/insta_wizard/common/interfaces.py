from datetime import datetime
from typing import Protocol

from insta_wizard.common.models.proxy import ProxyInfo


class ProxyProvider(Protocol):
    async def provide_new(self) -> ProxyInfo | None:
        """Must returns ProxyInfo | None"""
        ...


class PhoneSmsCodeProvider(Protocol):
    async def provide_number(self, new: bool = False) -> str:
        """Must returns phone number string starts with +"""
        ...

    async def provide_code(self) -> str:
        """
        Must returns code like "123456"
        raises SmsCodeTimeout if code waiting timed out
        """
        ...


class CaptchaSolver:
    async def solve_normal(self, image_b64: str) -> str:
        """Must returns solution-text string"""
        ...


class SelfiePhotoProvider(Protocol):
    async def provide(self) -> str | None:
        """Must returns b64 encoded image data"""
        ...


class EmailCodeProvider(Protocol):
    async def provide_code(self, masked_email: str, from_datetime: datetime) -> str:
        """Must returns code from email"""
        ...

    async def provide_code_without_known_email(self, from_datetime: datetime) -> str:
        """Must returns code from email"""
        ...


class EmailCodeSignupProvider(Protocol):
    async def provide_email(self) -> str:
        """Returns email address to register with"""
        ...

    async def provide_code(self, email: str, from_datetime: datetime) -> str:
        """Returns verification code from email"""
        ...


class ResetPasswordLinkProvider(Protocol):
    async def provide_link(self, masked_email: str, from_datetime: datetime) -> str:
        """Must returns link from email for account password recovery"""
        ...


class ManualPhoneSmsCodeProvider(PhoneSmsCodeProvider):
    async def provide_number(self, new: bool = False) -> str:
        return input("Enter phone number: ")

    async def provide_code(self) -> str:
        return input("Enter the code from the SMS: ")


class ManualEmailCodeSignupProvider(EmailCodeSignupProvider):
    async def provide_email(self) -> str:
        return input("Enter email address: ")

    async def provide_code(self, email: str, from_datetime: datetime) -> str:
        return input(f"Enter the code sent to {email}: ")
