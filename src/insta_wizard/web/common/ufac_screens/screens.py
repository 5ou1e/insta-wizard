import re
from typing import TypeAlias

import orjson

from insta_wizard.web.common.ufac_screens.screen_errors_parser import (
    extract_all_generic_errors,
)
from insta_wizard.web.exceptions import ResponseParsingError


class BaseUfacCheckpointScreen:
    """Базовый класс для всех экранов UFAC чекпоинта"""

    step_name: str

    def __init__(self, response: dict):
        self.response = response
        self.response_string = str(response)

    def errors(self) -> list:
        return extract_all_generic_errors(self.response)

    def has_errors(self) -> bool:
        return bool(self.errors())


class UfacIntroCheckpointScreen(BaseUfacCheckpointScreen):
    """чтобы использовать свой аккаунт, подтвердите, что вы — человек"""

    step_name: str = "начальный экран"

    @staticmethod
    def match(response: dict) -> bool:
        return "com.bloks.www.checkpoint.ufac.complete_intro" in str(response)


class UfacSubmitCaptchaCheckpointScreen(BaseUfacCheckpointScreen):
    """Подтвердите, что вы человек, введите код на изображении"""

    step_name: str = "решите капчу"

    def __init__(self, response: dict):
        super().__init__(response)
        self._captcha_persist_data: str | None = None
        self._facebook_captcha_image_url: str | None = None

    @staticmethod
    def match(response: dict) -> bool:
        return "com.bloks.www.checkpoint.ufac.bot_captcha.submit" in str(response)

    @property
    def is_recaptcha(self) -> bool:
        return "bk.components.ig.ufac.Recaptcha" in self.response_string

    @property
    def is_text_captcha(self) -> bool:
        return "https://www.facebook.com/captcha/tfbimage" in self.response_string

    @property
    def persisted_data_for_recaptcha(self) -> str:
        # ищем: array.Make(keys...persisted_data...) потом array.Make(values...) где первое значение — persisted_data
        p = (
            r'array\.Make,\s*(?:\\")?persisted_data(?:\\")?.*?\)\)\s*,\s*'
            r'\(bk\.action\.array\.Make,\s*(?:\\")?([A-Za-z0-9_-]{20,})(?:\\")?'
        )
        m = re.search(p, self.response_string, flags=re.DOTALL)
        return m.group(1) if m else None

    @property
    def captcha_persist_data(self) -> str:
        if self._captcha_persist_data is None:
            m = re.search(r"captcha_persist_data=([^&\"\s)]+)", self.response_string)
            value = m.group(1) if m else None
            if not value:
                raise ResponseParsingError(
                    msg="Не удалось спарсить значение captcha_persist_data из ответа инстаграм"
                )
            self._captcha_persist_data = value
        return self._captcha_persist_data

    @property
    def facebook_captcha_image_url(self) -> str:
        if self._facebook_captcha_image_url is None:
            pattern = re.compile(
                r"(https://www\.facebook\.com/captcha/tfbimage/[^\"\s]*)",
                re.IGNORECASE,
            )
            m = pattern.search(self.response_string)
            url = m.group(1) if m else None
            if not url:
                raise ResponseParsingError(
                    msg="Не удалось спарсить facebook_captcha_tfbimage url из ответа инстаграм"
                )
            self._facebook_captcha_image_url = url
        return self._facebook_captcha_image_url


class UfacSetContactPointCheckpointScreen(BaseUfacCheckpointScreen):
    """
    Введите свой номер мобильного телефона
    Вам необходимо подтвердить этот номер мобильного телефона с помощью кода в SMS или WhatsApp.
    """

    step_name: str = "ввод номера телефона"

    @staticmethod
    def match(response: dict) -> bool:
        return "com.bloks.www.checkpoint.ufac.set_contact_point.submit" in str(response)


class UfacContactPointCodeSubmitCheckpointScreen(BaseUfacCheckpointScreen):
    """
    Данный экран может быть в двух состояниях - когда код отправлен на WhatsApp или в SMS.
    Примеры:

    Мы отправили код в WhatsApp
    Введите 6-значный код подтверждения, который мы отправили в WhatsApp на номер +79159999999. Код может прийти в течение минуты.

    или

    Введите код подтверждения
    Введите 6-значный код подтверждения, который мы отправили в SMS на номер +79159999999. Код может прийти в течение минуты.

    """

    step_name: str = "ввод кода из смс"

    @staticmethod
    def match(response: dict) -> bool:
        checks = [
            "com.bloks.www.checkpoint.ufac.contact_point.submit_code" in str(response),
            "com.bloks.www.checkpoint.ufac.contact_point.resend_code" in str(response),
            "com.bloks.www.checkpoint.ufac.contact_point.unset" in str(response),
        ]
        return all(checks)

    def is_sent_to_whatsapp(self) -> bool:
        return "WhatsApp" in str(self.response)


class UfacUploadSelfiePhotoCheckpointScreen(BaseUfacCheckpointScreen):
    """
    Загрузите селфи для подтверждения аккаунта
    Загрузите фото, на котором четко видно ваше лицо. Фото должно быть сделано при достаточном освещении и не должно быть размытым. В кадре не должно быть никого, кроме вас.
    """

    step_name: str = "загрузка селфи-фото"

    @staticmethod
    def match(response: dict) -> bool:
        return (
            "com.bloks.www.checkpoint.ufac.image_upload.upload_identity_verification_photo"
            in str(response)
        )


class UfacAppealRequestSentCheckpointScreen(BaseUfacCheckpointScreen):
    """
    Вы отправили запрос на обжалование 30 января 2026.
    Обычно проверка информации занимает около часа. Загляните позже.
    Ваш аккаунт не показывается в Instagram, и вы не можете использовать его.
    """

    step_name: str = "запрос отправлен на рассмотрение"

    @staticmethod
    def match(response: dict) -> bool:
        # Тут пока что определяем по наличию ссылки на картинку с часами - https://static.cdninstagram.com/rsrc.php/v4/y9/r/IxAbsKZvuu-.png
        return "IxAbsKZvuu-.png" in str(response) or "T8WHkc4LL_k.webp" in str(response)


class UfacAccountUnblockedCheckpointScreen(BaseUfacCheckpointScreen):
    """
    Вы снова можете использовать Instagram
    Ваш аккаунт разблокирован.
    Мы проверили ваш аккаунт и убедились, что он не нарушает наши Нормы сообщества.
    """

    step_name: str = "аккаунт разблокирован"

    @staticmethod
    def match(response: dict) -> bool:
        return "com.bloks.www.checkpoint.ufac.complete_outro" in str(response)


class UfacCloseAndClearChallengeCheckpointScreen(BaseUfacCheckpointScreen):
    """
    Пустой экран при успешном завершении челенджа
    """

    step_name: str = "аккаунт разблокирован"

    @staticmethod
    def match(response: dict) -> bool:
        return "ig.action.navigation.ClearChallenge" in str(
            response
        ) and "bk.action.screen.CloseScreen" in str(response)


UfacCheckpointScreen: TypeAlias = (
    UfacIntroCheckpointScreen
    | UfacSubmitCaptchaCheckpointScreen
    | UfacSetContactPointCheckpointScreen
    | UfacContactPointCodeSubmitCheckpointScreen
    | UfacUploadSelfiePhotoCheckpointScreen
    | UfacAppealRequestSentCheckpointScreen
    | UfacAccountUnblockedCheckpointScreen
    | UfacCloseAndClearChallengeCheckpointScreen
)


def screen_from_response(
    response: dict,
) -> UfacCheckpointScreen:
    screens = [
        UfacIntroCheckpointScreen,
        UfacSubmitCaptchaCheckpointScreen,
        UfacSetContactPointCheckpointScreen,
        UfacContactPointCodeSubmitCheckpointScreen,
        UfacUploadSelfiePhotoCheckpointScreen,
        UfacAppealRequestSentCheckpointScreen,
        UfacAccountUnblockedCheckpointScreen,
        UfacCloseAndClearChallengeCheckpointScreen,
    ]

    for cls in screens:
        if cls.match(response=response):
            return cls(response=response)

    raise ResponseParsingError(
        msg=f"Неизвестный экран UFAC-чекпоинта: response={orjson.dumps(response).decode('utf-8')}"
    )
