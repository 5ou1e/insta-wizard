from dataclasses import dataclass


class InstaWizardError(Exception):
    """Base InstaWizard error class."""

    pass


@dataclass(kw_only=True, slots=True)
class AuthPlatformChallengeCodeNotFound(InstaWizardError):
    def __str__(self):
        return "Code not found in email"


@dataclass(kw_only=True, slots=True)
class ChallengeHandlingFailedError(InstaWizardError):
    msg: str

    def __str__(self):
        return f"Failed to pass checkpoint: {self.msg}"


class SmsCodeTimeout(InstaWizardError):
    pass
