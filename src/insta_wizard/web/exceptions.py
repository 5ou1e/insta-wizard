from dataclasses import dataclass

from insta_wizard.common.exceptions import InstaWizardError
from insta_wizard.common.transport.models import ResponseInfo
from insta_wizard.web.models.other import CheckpointRequiredErrorData


@dataclass(kw_only=True, slots=True)
class WebClientError(InstaWizardError):
    @property
    def title(self) -> str:
        return "Ошибка WEB IG-клиента"

    def __str__(self) -> str:
        return self.title


@dataclass(kw_only=True, slots=True)
class StateParametersMissingError(WebClientError):
    """Ошибка при отсутствии в state необходимых параметров для выполнения запросов"""

    msg: str

    @property
    def title(self) -> str:
        return self.msg


@dataclass(kw_only=True, slots=True)
class ChallengeHandlingError(WebClientError):
    msg: str

    @property
    def title(self) -> str:
        return self.msg


@dataclass(kw_only=True, slots=True)
class ResponseParsingError(WebClientError):
    """Ошибки парсинга различных значений из ответов инстаграм"""

    msg: str

    @property
    def title(self) -> str:
        return self.msg


@dataclass(kw_only=True, slots=True)
class NetworkError(WebClientError):
    message: str

    @property
    def title(self) -> str:
        return "Ошибка сети"


@dataclass(kw_only=True, slots=True)
class InstagramResponseError(WebClientError):
    response: ResponseInfo


@dataclass(kw_only=True, slots=True)
class NotFoundError(InstagramResponseError):
    request_url: str | None = None

    @property
    def title(self) -> str:
        return f"Ресурс не найден, request_url={self.request_url}"


@dataclass(kw_only=True, slots=True)
class UnexpectedResponseContentTypeError(WebClientError):
    response: ResponseInfo
    expected: str
    returned: str

    @property
    def title(self) -> str:
        return f"Инстаграм вернул ответ не в том виде, который ожидался: expected={self.expected}, returned={self.returned}, status_code={self.response.status}"


@dataclass(kw_only=True, slots=True)
class UnexpectedRedirectResponseError(InstagramResponseError):
    response: ResponseInfo
    request_url: str
    location: str | None = None

    @property
    def title(self) -> str:
        return f"Неожиданный редирект от инстаграм при запросе на url: {self.request_url}, redirect_location={self.location}"


@dataclass(kw_only=True, slots=True)
class BadRequestError(WebClientError):
    response: ResponseInfo


@dataclass(kw_only=True, slots=True)
class CheckpointRequiredError(InstagramResponseError):
    checkpoint_data: CheckpointRequiredErrorData

    @property
    def title(self) -> str:
        return "CheckpointRequired"


@dataclass(kw_only=True, slots=True)
class ResetPasswordLinkExpiredError(WebClientError):
    message: str

    @property
    def title(self) -> str:
        return "Ссылка для смены пароля недействительна"


@dataclass(kw_only=True, slots=True)
class UserNotFoundError(WebClientError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Пользователь не найден"


@dataclass(kw_only=True, slots=True)
class LoginError(WebClientError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Ошибка авторизации"


@dataclass(kw_only=True, slots=True)
class LoginBadPasswordError(LoginError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Ошибка авторизации: неверный пароль"


@dataclass(kw_only=True, slots=True)
class UnknownLoginError(LoginError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Неизвестная ошибка авторизации"


@dataclass(kw_only=True, slots=True)
class ResetPasswordLinkNotSentError(WebClientError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Инстаграм не отправил ссылку на почту"


@dataclass(kw_only=True, slots=True)
class SessionIDMissingError(WebClientError):
    @property
    def title(self) -> str:
        return "Отсутствует sessionid"


@dataclass(kw_only=True, slots=True)
class TooManyRequestsError(InstagramResponseError):
    @property
    def title(self) -> str:
        return "Слишком частые запросы (429)"
