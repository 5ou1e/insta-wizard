from dataclasses import dataclass


class InstaWizardError(Exception):
    """Базовый класс ошибок InstaWizard"""

    pass


@dataclass(kw_only=True, slots=True)
class AuthPlatformChallengeCodeNotFound(InstaWizardError):
    def __str__(self):
        return "Код на почте не найден"


@dataclass(kw_only=True, slots=True)
class ChallengeHandlingFailedError(InstaWizardError):
    msg: str

    def __str__(self):
        return f"Не удалось пройти чекпоинт: {self.msg}"


class SmsCodeTimeout(InstaWizardError):
    pass
