import base64
import random
import uuid
from dataclasses import dataclass

import orjson
from mashumaro import DataClassDictMixin

from insta_wizard.common.generators import generate_waterfall_id


@dataclass(kw_only=True, slots=True)
class MobileClientLocalData(DataClassDictMixin):
    authorization_data: dict
    user_id: str | None = None
    mid: str | None = None
    csrftoken: str | None = None
    shbid: str | None = None
    shbts: str | None = None
    rur: str | None = None
    www_claim: str | None = None
    public_key: str | None = None  # /api/v1/launcher/mobileconfig/
    public_key_id: int | None = None  # /api/v1/launcher/mobileconfig/

    pigeon_session_id: str  # UFS-{uuid.uuid4()}-0 / Меняется полностью при открытии\закрытии приложении и при сворачивании\разворачивании увеличивается счетчик
    waterfall_id: str  # UUID v4 , Генерирует клиент , меняется при каждом открытии приложения и для разных запросов тоже меняется
    session_flush_nonce: str | None = None  # Нужна для /logout

    # Сбрасываются при перезапуске приложения
    requests_count: int = 0
    total_bytes: float = 0
    total_time_ms: float = 0

    @classmethod
    def create(
        cls,
        authorization_data: dict | None = None,
        user_id: str | None = None,
        pigeon_session_id: str | None = None,
        mid: str | None = None,
        csrftoken: str | None = None,
        shbid: str | None = None,
        shbts: str | None = None,
        rur: str | None = None,
        www_claim: str | None = None,
        public_key: str | None = None,
        public_key_id: int | None = None,
        session_flush_nonce: str | None = None,
        waterfall_id: str | None = None,
        requests_count: int = 0,
        total_bytes: float = 0,
        total_time_ms: float = 0,
    ) -> "MobileClientLocalData":
        authorization_data = authorization_data or {}
        if authorization_data:
            user_id = authorization_data.get("ds_user_id")

        pigeon_session_id = pigeon_session_id or f"UFS-{uuid.uuid4()}-0"
        waterfall_id = waterfall_id or generate_waterfall_id()

        return cls(
            pigeon_session_id=pigeon_session_id,
            authorization_data=authorization_data,
            user_id=user_id,
            mid=mid,
            csrftoken=csrftoken,
            shbid=shbid,
            shbts=shbts,
            rur=rur,
            www_claim=www_claim,
            public_key=public_key,
            public_key_id=public_key_id,
            session_flush_nonce=session_flush_nonce,
            waterfall_id=waterfall_id,
            requests_count=requests_count,
            total_bytes=total_bytes,
            total_time_ms=total_time_ms,
        )

    def set_authorization_data(self, authorization_data: dict[str, str]):
        self.authorization_data = authorization_data
        self.user_id = self.authorization_data.get("ds_user_id")

    def clear_authorization_data(self) -> None:
        self.authorization_data = {}
        self.user_id = None

    @property
    def authorization(self) -> str | None:
        """
        Authorization Header в формате 'Bearer IGT:2:eaW9u.....aWQiOiI0NzM5='
        """

        if self.authorization_data:
            b64part = base64.b64encode(orjson.dumps(self.authorization_data)).decode()
            return f"Bearer IGT:2:{b64part}"
        return None

    def set_waterfall_id(self, waterfall_id) -> None:
        self.waterfall_id = waterfall_id

    def set_rur(self, rur: str | None):
        self.rur = rur

    def set_www_claim(self, www_claim: str | None):
        self.www_claim = www_claim

    def set_public_key(self, public_key: str):
        self.public_key = public_key

    def set_public_key_id(self, public_key_id: int):
        self.public_key_id = public_key_id

    def set_session_flush_nonce(self, session_flush_nonce: str):
        self.session_flush_nonce = session_flush_nonce

    @property
    def cookies(self) -> dict:
        cookies = {}

        if self.mid:
            cookies["mid"] = self.mid
        if self.csrftoken:
            cookies["csrftoken"] = self.csrftoken
        if self.rur:
            cookies["rur"] = self.rur
        if self.shbid:
            cookies["shbid"] = self.shbid
        if self.shbts:
            cookies["shbts"] = self.shbts
        if self.authorization_data.get("sessionid"):
            cookies["sessionid"] = self.authorization_data.get("sessionid")
        if self.authorization_data.get("ds_user_id"):
            cookies["ds_user_id"] = self.authorization_data.get("ds_user_id")

        return cookies

    @property
    def cookies_string(self) -> str:
        return ";".join([f"{k}={v}" for k, v in self.cookies.items()]) if self.cookies else ""

    @property
    def bandwidth_metrics(self) -> dict:
        # Сбрасываются при перезагрузке приложения
        total_bytes = self.total_bytes
        total_time_ms = self.total_time_ms

        if total_time_ms == 0:
            speed = 531  # константа для первого/кэшированного запроса
        else:
            base_speed = (total_bytes * 8) / total_time_ms
            coefficient = 0.18 * random.uniform(0.7, 1.3)
            speed = base_speed * coefficient

        return {
            "bandwidth_speed_kbps": speed,
            "bandwidth_totalbytes_b": self.total_bytes,
            "bandwidth_totaltime_ms": self.total_time_ms,
        }
