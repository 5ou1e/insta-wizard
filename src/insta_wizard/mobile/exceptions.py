from dataclasses import dataclass

from insta_wizard.common.exceptions import InstaWizardError
from insta_wizard.common.transport.models import ResponseInfo
from insta_wizard.mobile.models.challenge import (
    ChallengeRequiredData,
    FeedbackRequiredData,
)


@dataclass(kw_only=True, slots=True)
class MobileClientError(InstaWizardError):
    @property
    def title(self) -> str:
        return "Ошибка Mobile IG-клиента"

    def __str__(self) -> str:
        return self.title


@dataclass(kw_only=True, slots=True)
class ResponseJsonDecodeError(MobileClientError):
    @property
    def title(self) -> str:
        return "Ошибка при конвертации ответа в JSON формат"


@dataclass(kw_only=True, slots=True)
class ResponseParsingError(MobileClientError):
    """Ошибка парсинга значений из ответа от инстаграм"""

    msg: str

    @property
    def title(self) -> str:
        return self.msg


@dataclass(kw_only=True, slots=True)
class NetworkError(MobileClientError):
    message: str

    @property
    def title(self) -> str:
        return "Ошибка сети"


@dataclass(kw_only=True, slots=True)
class InstagramResponseError(MobileClientError):
    response: ResponseInfo


@dataclass(kw_only=True, slots=True)
class UnexpectedResponseContentTypeError(MobileClientError):
    response: ResponseInfo
    expected: str
    returned: str

    @property
    def title(self) -> str:
        return f"Инстаграм вернул ответ не в том виде, который ожидался: expected={self.expected}, returned={self.returned}, status_code={self.response.status}"


@dataclass(kw_only=True, slots=True)
class AuthorizationMissingError(MobileClientError):
    @property
    def title(self) -> str:
        return "Отсутствует authorization-header"


@dataclass(kw_only=True, slots=True)
class BadResponseError(MobileClientError):
    @property
    def title(self) -> str:
        return "Некорректный ответ от Instagram"


# --------------------------------------------


@dataclass(kw_only=True, slots=True)
class ChallengeRequiredError(MobileClientError):
    response_json: dict
    challenge_data: ChallengeRequiredData | None = None

    @property
    def title(self) -> str:
        return f"ChallengeRequired, api_path={self.challenge_data.api_path}"


# --------------------------------------------


@dataclass(kw_only=True, slots=True)
class LoginRequiredError(InstagramResponseError):
    @property
    def title(self) -> str:
        return "Инстаграм сбросил авторизацию"


@dataclass(kw_only=True, slots=True)
class NotFoundError(InstagramResponseError):
    @property
    def title(self) -> str:
        return "Ресурс не найден"


@dataclass(kw_only=True, slots=True)
class BadRequestError(InstagramResponseError):
    @property
    def title(self) -> str:
        return "Некорректный запрос"


@dataclass(kw_only=True, slots=True)
class TooManyRequestsError(InstagramResponseError):
    @property
    def title(self) -> str:
        return "Слишком частые запросы (status_code=429)"


@dataclass(kw_only=True, slots=True)
class LoginError(MobileClientError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Ошибка при авторизации"


@dataclass(kw_only=True, slots=True)
class LoginBadPasswordError(LoginError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Неверный пароль"


@dataclass(kw_only=True, slots=True)
class LoginUnknownError(LoginError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Неизвестная ошибка авторизации"


@dataclass(kw_only=True, slots=True)
class BloksLoginError(MobileClientError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Ошибка авторизации: TwoStepVerificationRequired"


@dataclass(kw_only=True, slots=True)
class BloksLoginBadPasswordError(BloksLoginError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Ошибка авторизации: неверный пароль"


@dataclass(kw_only=True, slots=True)
class BloksLoginAssistiveLoginConfirmationNeededError(BloksLoginError):
    response_json: dict

    @property
    def title(self) -> str:
        return (
            "Ошибка авторизации: инстаграм просит пройти подтверждение assistive_login_confirmation"
        )


@dataclass(kw_only=True, slots=True)
class BloksLoginAuthenticationConfiramtionRequiredError(BloksLoginBadPasswordError):
    response_json: dict
    masked_email: str | None = None

    @property
    def title(self) -> str:
        return f"Ошибка авторизации: Пароль, который вы ввели, неправильный. Чтобы войти, используйте ссылку, которую мы отправили на..., (извлеченный из ответа email - {self.masked_email})"


@dataclass(kw_only=True, slots=True)
class BloksLoginBloksCAAAccountRecoveryAuthMethodControllerError(BloksLoginBadPasswordError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Ошибка авторизации: инстаграм предлагает восстановление/подтверждение через метод (SMS/почта/другое)"


@dataclass(kw_only=True, slots=True)
class BloksLoginUnknownError(BloksLoginError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Неизвестная ошибка авторизации"


@dataclass(kw_only=True, slots=True)
class BloksLoginAccountNotFoundError(BloksLoginError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Ошибка авторизации: аккаунт с таким юзернеймом не найден"


@dataclass(kw_only=True, slots=True)
class BloksLoginTwoStepVerificationRequiredError(BloksLoginError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Ошибка авторизации: TwoStepVerificationRequired"


@dataclass(kw_only=True, slots=True)
class UnauthorizedError(InstagramResponseError):
    @property
    def title(self) -> str:
        return "Unauthorized"


@dataclass(kw_only=True, slots=True)
class OopsAnErrorOccurred(InstagramResponseError):
    @property
    def title(self) -> str:
        return "Oops an error occured"


@dataclass(kw_only=True, slots=True)
class UserIdNotFound(NotFoundError):
    @property
    def title(self) -> str:
        return "Пользователь с таким ID не найден"


@dataclass(kw_only=True, slots=True)
class UserNotFoundError(MobileClientError):
    response_json: dict

    @property
    def title(self) -> str:
        return "Пользователь не найден"


@dataclass(kw_only=True, slots=True)
class FeedbackRequiredError(InstagramResponseError):
    data: FeedbackRequiredData

    @property
    def title(self) -> str:
        return "Действие заблокировано"


# @dataclass(kw_only=True, slots=True)
# class NodeTaoSystemExceptionError(MobileClientError):
#
#     @property
#     def title(self) -> str:
#         return f"NodeTaoSystemException"


@dataclass(kw_only=True, slots=True)
class InstagramBackend572Error(InstagramResponseError):
    @property
    def title(self) -> str:
        return "InstagramBackend572Error"


@dataclass(kw_only=True, slots=True)
class PayloadReturnedIsNullError(InstagramResponseError):
    @property
    def title(self) -> str:
        return "PayloadReturnedIsNullError"


@dataclass(kw_only=True, slots=True)
class MethodNotAllowedError(InstagramResponseError):
    @property
    def title(self) -> str:
        return "MethodNotAllowedError"


@dataclass(kw_only=True, slots=True)
class AuthPlatformCheckpointWrongOrIncorrectCodeError(MobileClientError):
    @property
    def title(self) -> str:
        return "Неверный код или срок действия кода истек"


@dataclass(kw_only=True, slots=True)
class BloksRegistrationError(MobileClientError):
    msg: str

    @property
    def title(self) -> str:
        return f"Ошибка регистрации: {self.msg}"
