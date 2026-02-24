from dataclasses import dataclass
from enum import StrEnum


class InstagramAppVersion(StrEnum):
    V269 = "269.0.0.18.75"
    V374 = "374.0.0.43.67"
    V410 = "410.1.0.63.71"

    @classmethod
    def from_string(cls, version_string: str):
        try:
            return cls[version_string]
        except KeyError:
            raise ValueError("Неизвестная версия Instagram App")


@dataclass(kw_only=True, frozen=True)
class InstagramAppVersionInfo:
    version: InstagramAppVersion
    app_id: str
    version_code: str
    min_sdk: int | None = None  # minSDK - Минимальная версия Android
    taget_sdk: int | None = None  # targetSDK - Совместимая версия Android
    apk_version_code: int | None = None
    access_token: str
    bloks_version_id: str
    capabilities: str
    module_hash: str | None = None
    qpl_marker_id: int
    offline_experiment_group: str

    @property
    def app_version(self) -> str:
        return self.version.value


class InstagramAppVersionInfoRegistry:
    _version_configs: dict[InstagramAppVersion, InstagramAppVersionInfo] = {
        InstagramAppVersion.V374: InstagramAppVersionInfo(
            version=InstagramAppVersion.V374,
            app_id="567067343352427",
            version_code="715888958",
            min_sdk=28,
            taget_sdk=35,
            apk_version_code=377811765,
            access_token="567067343352427|f249176f09e26ce54212b472dbab8fa8",
            bloks_version_id="382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            capabilities="3brTv10=",
            module_hash="7607b7fe70423451370dd0c5de28a5be46472931dafbe414e638d872996d4304",
            qpl_marker_id=36707139,  # эта штука не факт что константа для версии
            offline_experiment_group="caa_iteration_v3_perf_ig_4",
        ),
        InstagramAppVersion.V269: InstagramAppVersionInfo(
            version=InstagramAppVersion.V269,
            app_id="567067343352427",
            version_code="314665256",
            min_sdk=28,
            taget_sdk=33,
            apk_version_code=366906366,
            bloks_version_id="ce555e5500576acd8e84a66018f54a05720f2dce29f0bb5a1f97f0c10d6fac48",  # из aiograpi
            # Параметры ниже взяты из v374
            access_token="567067343352427|f249176f09e26ce54212b472dbab8fa8",
            capabilities="3brTv10=",
            qpl_marker_id=36707139,
            offline_experiment_group="caa_iteration_v3_perf_ig_4",
        ),
        InstagramAppVersion.V410: InstagramAppVersionInfo(
            version=InstagramAppVersion.V410,
            app_id="567067343352427",
            version_code="846519343",
            min_sdk=28,
            taget_sdk=36,
            apk_version_code=381607172,
            access_token="567067343352427|f249176f09e26ce54212b472dbab8fa8",
            offline_experiment_group="caa_iteration_v3_perf_ig_4",
            bloks_version_id="b7737193b91c3a2f4050bdfc9d9ae0f578a93b4181fd43efe549daacba5c7db9",
            capabilities="3brTv10=",
            qpl_marker_id=36707139,
        ),
    }

    @classmethod
    def get(cls, version: InstagramAppVersion) -> InstagramAppVersionInfo:
        try:
            return cls._version_configs[version]
        except KeyError:
            raise ValueError(f"Неизвестная версия Instagram: {version}")
