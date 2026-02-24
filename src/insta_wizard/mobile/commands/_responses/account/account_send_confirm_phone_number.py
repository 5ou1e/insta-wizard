from typing import TypedDict


class AccountSendConfirmPhoneNumberResponsePhoneVerificationSettings(TypedDict):
    max_sms_count: int
    resend_sms_delay_sec: int
    robocall_count_down_time_sec: int
    robocall_after_max_sms: bool


class AccountSendConfirmPhoneNumberResponse(TypedDict):
    action: str
    phone_verification_settings: AccountSendConfirmPhoneNumberResponsePhoneVerificationSettings
    status: str
