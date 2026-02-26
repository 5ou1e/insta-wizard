from dataclasses import dataclass

from insta_wizard.common.exceptions import InstaWizardError
from insta_wizard.common.transport.models import ResponseInfo
from insta_wizard.web.models.other import CheckpointRequiredErrorData


@dataclass(kw_only=True, slots=True)
class WebClientError(InstaWizardError):
    def __str__(self) -> str:
        return "Web IG client error"


@dataclass(kw_only=True, slots=True)
class StateParametersMissingError(WebClientError):
    """Raised when the state is missing required parameters for executing requests."""

    msg: str

    def __str__(self) -> str:
        return self.msg


@dataclass(kw_only=True, slots=True)
class ChallengeHandlingError(WebClientError):
    msg: str

    def __str__(self) -> str:
        return self.msg


@dataclass(kw_only=True, slots=True)
class ResponseParsingError(WebClientError):
    """Raised when parsing values from Instagram responses fails."""

    msg: str

    def __str__(self) -> str:
        return self.msg


@dataclass(kw_only=True, slots=True)
class NetworkError(WebClientError):
    message: str

    def __str__(self) -> str:
        return "Network error"


@dataclass(kw_only=True, slots=True)
class InstagramResponseError(WebClientError):
    response: ResponseInfo

    def __str__(self) -> str:
        return f"InstagramResponseError, status_code={self.response.status}, response={self.response.response_string[:100]}..."

@dataclass(kw_only=True, slots=True)
class NotFoundError(InstagramResponseError):
    request_url: str | None = None

    def __str__(self) -> str:
        return f"Resource not found, request_url={self.request_url}"


@dataclass(kw_only=True, slots=True)
class UnexpectedResponseContentTypeError(WebClientError):
    response: ResponseInfo
    expected: str
    returned: str

    def __str__(self) -> str:
        return f"Instagram returned response in unexpected format: expected={self.expected}, returned={self.returned}, status_code={self.response.status}"


@dataclass(kw_only=True, slots=True)
class UnexpectedRedirectResponseError(InstagramResponseError):
    response: ResponseInfo
    request_url: str
    location: str | None = None

    def __str__(self) -> str:
        return f"Unexpected redirect from Instagram for request url: {self.request_url}, redirect_location={self.location}"


@dataclass(kw_only=True, slots=True)
class BadRequestError(WebClientError):
    response: ResponseInfo


@dataclass(kw_only=True, slots=True)
class CheckpointRequiredError(InstagramResponseError):
    checkpoint_data: CheckpointRequiredErrorData

    def __str__(self) -> str:
        return "CheckpointRequired"


@dataclass(kw_only=True, slots=True)
class ResetPasswordLinkExpiredError(WebClientError):
    message: str

    def __str__(self) -> str:
        return "Password reset link is invalid"


@dataclass(kw_only=True, slots=True)
class UserNotFoundError(WebClientError):
    response_json: dict

    def __str__(self) -> str:
        return "User not found"


@dataclass(kw_only=True, slots=True)
class LoginError(WebClientError):
    response_json: dict

    def __str__(self) -> str:
        return "Authorization error"


@dataclass(kw_only=True, slots=True)
class LoginBadPasswordError(LoginError):
    response_json: dict

    def __str__(self) -> str:
        return "Authorization error: wrong password"


@dataclass(kw_only=True, slots=True)
class UnknownLoginError(LoginError):
    response_json: dict

    def __str__(self) -> str:
        return "Unknown authorization error"


@dataclass(kw_only=True, slots=True)
class ResetPasswordLinkNotSentError(WebClientError):
    response_json: dict

    def __str__(self) -> str:
        return "Instagram did not send the reset link to email"


@dataclass(kw_only=True, slots=True)
class SessionIDMissingError(WebClientError):
    def __str__(self) -> str:
        return "Session ID is missing"


@dataclass(kw_only=True, slots=True)
class TooManyRequestsError(InstagramResponseError):
    def __str__(self) -> str:
        return "Too many requests (429)"
