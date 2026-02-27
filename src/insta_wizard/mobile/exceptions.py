from dataclasses import dataclass

from insta_wizard.common.exceptions import InstaWizardError
from insta_wizard.common.transport.models import ResponseInfo
from insta_wizard.mobile.models.challenge import (
    ChallengeRequiredData,
    FeedbackRequiredData,
)


@dataclass(kw_only=True, slots=True)
class MobileClientError(InstaWizardError):
    def __str__(self) -> str:
        return "Mobile IG client error"


@dataclass(kw_only=True, slots=True)
class ResponseJsonDecodeError(MobileClientError):
    def __str__(self) -> str:
        return "Error converting response to JSON format"


@dataclass(kw_only=True, slots=True)
class ResponseParsingError(MobileClientError):
    """Raised when parsing values from Instagram response fails."""

    msg: str

    def __str__(self) -> str:
        return self.msg


@dataclass(kw_only=True, slots=True)
class NetworkError(MobileClientError):
    message: str

    def __str__(self) -> str:
        return "Network error"


@dataclass(kw_only=True, slots=True)
class InstagramResponseError(MobileClientError):
    response: ResponseInfo

    def __str__(self) -> str:
        return f"InstagramResponseError, status_code={self.response.status}, response={self.response.response_string[:100]}..."


@dataclass(kw_only=True, slots=True)
class UnexpectedResponseContentTypeError(MobileClientError):
    response: ResponseInfo
    expected: str
    returned: str

    def __str__(self) -> str:
        return f"Instagram returned response in unexpected format: expected={self.expected}, returned={self.returned}, status_code={self.response.status}"


@dataclass(kw_only=True, slots=True)
class AuthorizationMissingError(MobileClientError):
    def __str__(self) -> str:
        return "Authorization header is missing"


@dataclass(kw_only=True, slots=True)
class ChallengeRequiredError(MobileClientError):
    response_json: dict
    challenge_data: ChallengeRequiredData

    def __str__(self) -> str:
        return f"Challenge required, api_path={self.challenge_data.api_path}"


@dataclass(kw_only=True, slots=True)
class LoginRequiredError(InstagramResponseError):
    def __str__(self) -> str:
        return "Login required error"


@dataclass(kw_only=True, slots=True)
class NotFoundError(InstagramResponseError):
    def __str__(self) -> str:
        return "Resource not found"


@dataclass(kw_only=True, slots=True)
class BadRequestError(InstagramResponseError):
    def __str__(self) -> str:
        return f"Bad request, status_code={self.response.status}, response={self.response.response_string[:100]}..."


@dataclass(kw_only=True, slots=True)
class TooManyRequestsError(InstagramResponseError):
    def __str__(self) -> str:
        return "Too many requests (status_code=429)"


@dataclass(kw_only=True, slots=True)
class LoginError(MobileClientError):
    response_json: dict

    def __str__(self) -> str:
        return "Authorization error"


@dataclass(kw_only=True, slots=True)
class LoginBadPasswordError(LoginError):
    response_json: dict

    def __str__(self) -> str:
        return "Wrong password"


@dataclass(kw_only=True, slots=True)
class LoginUnknownError(LoginError):
    response_json: dict

    def __str__(self) -> str:
        return "Unknown authorization error"


@dataclass(kw_only=True, slots=True)
class BloksLoginError(MobileClientError):
    response_json: dict

    def __str__(self) -> str:
        return "Authorization error"


@dataclass(kw_only=True, slots=True)
class BloksLoginBadPasswordError(BloksLoginError):
    response_json: dict

    def __str__(self) -> str:
        return "Authorization error: wrong password"


@dataclass(kw_only=True, slots=True)
class BloksLoginAssistiveLoginConfirmationNeededError(BloksLoginError):
    response_json: dict

    def __str__(self) -> str:
        return "Authorization error: Instagram requires assistive_login_confirmation"


@dataclass(kw_only=True, slots=True)
class BloksLoginAuthenticationConfiramtionRequiredError(BloksLoginBadPasswordError):
    response_json: dict
    masked_email: str | None = None

    def __str__(self) -> str:
        return f"Authorization error: wrong password. To sign in, use the link we sent to... (email extracted from response: {self.masked_email})"


@dataclass(kw_only=True, slots=True)
class BloksLoginBloksCAAAccountRecoveryAuthMethodControllerError(BloksLoginBadPasswordError):
    response_json: dict

    def __str__(self) -> str:
        return "Authorization error: Instagram suggests account recovery/confirmation via method (SMS/email/other)"


@dataclass(kw_only=True, slots=True)
class BloksLoginUnknownError(BloksLoginError):
    response_json: dict

    def __str__(self) -> str:
        return "Unknown authorization error"


@dataclass(kw_only=True, slots=True)
class BloksLoginAccountNotFoundError(BloksLoginError):
    response_json: dict

    def __str__(self) -> str:
        return "Authorization error: account with this username not found"


@dataclass(kw_only=True, slots=True)
class LoginChallengeRequiredError(MobileClientError):
    """Login challenge required"""

    response_json: dict

    def __str__(self) -> str:
        return "Login challenge required"


@dataclass(kw_only=True, slots=True)
class LoginTwoStepVerificationRequiredError(LoginChallengeRequiredError):
    """Two-step verification challenge required during login"""

    response_json: dict

    def __str__(self) -> str:
        return "Two step verification challenge required during login"


@dataclass(kw_only=True, slots=True)
class LoginUnknownChallengeRequiredError(LoginChallengeRequiredError):
    """Unknown challenge during login"""

    response_json: dict
    challenge_data: ChallengeRequiredData

    def __str__(self) -> str:
        return "Unknown challenge during login"


@dataclass(kw_only=True, slots=True)
class UnauthorizedError(InstagramResponseError):
    def __str__(self) -> str:
        return "Unauthorized"


@dataclass(kw_only=True, slots=True)
class OopsAnErrorOccurred(InstagramResponseError):
    def __str__(self) -> str:
        return "Oops, an error occurred"


@dataclass(kw_only=True, slots=True)
class UserIdNotFound(MobileClientError):
    def __str__(self) -> str:
        return "User with this ID not found"


@dataclass(kw_only=True, slots=True)
class UserNotFoundError(MobileClientError):
    response_json: dict

    def __str__(self) -> str:
        return "User not found"


@dataclass(kw_only=True, slots=True)
class FeedbackRequiredError(InstagramResponseError):
    data: FeedbackRequiredData

    def __str__(self) -> str:
        return "Action is blocked"


@dataclass(kw_only=True, slots=True)
class InstagramBackend572Error(InstagramResponseError):
    def __str__(self) -> str:
        return "InstagramBackend572Error"


@dataclass(kw_only=True, slots=True)
class PayloadReturnedIsNullError(InstagramResponseError):
    def __str__(self) -> str:
        return "PayloadReturnedIsNullError"


@dataclass(kw_only=True, slots=True)
class NodeTaoSystemExceptionError(InstagramResponseError):
    """Instagram backend error - {"message":"NodeTaoSystemException: tao_errno=6307..."""

    def __str__(self) -> str:
        return "NodeTaoSystemException"


@dataclass(kw_only=True, slots=True)
class MethodNotAllowedError(InstagramResponseError):
    def __str__(self) -> str:
        return "MethodNotAllowedError"


@dataclass(kw_only=True, slots=True)
class AuthPlatformCheckpointWrongOrIncorrectCodeError(MobileClientError):
    def __str__(self) -> str:
        return "Invalid code or code has expired"


@dataclass(kw_only=True, slots=True)
class BloksRegistrationError(MobileClientError):
    msg: str

    def __str__(self) -> str:
        return f"Registration error: {self.msg}"
