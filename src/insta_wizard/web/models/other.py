from dataclasses import dataclass

from mashumaro import DataClassDictMixin


@dataclass(slots=True)
class GraphqlQueriesInitialParams:
    lsd_token: str
    dtsg_token: str
    haste_session: str
    hsi: str
    spin_r: str
    spin_b: str
    spin_t: str
    comet_env: str
    versioning_id: str
    jazoest: str

    def as_dict(self) -> dict[str, str]:
        return {
            "lsd_token": self.lsd_token,
            "dtsg_token": self.dtsg_token,
            "haste_session": self.haste_session,
            "hsi": self.hsi,
            "__spin_r": self.spin_r,
            "__spin_b": self.spin_b,
            "__spin_t": self.spin_t,
            "comet_env": self.comet_env,
            "versioningID": self.versioning_id,
            "jazoest": self.jazoest,
        }


@dataclass(kw_only=True, slots=True)
class CheckpointRequiredErrorData(DataClassDictMixin):
    message: str
    checkpoint_url: str
    lock: bool
    flow_render_type: int
    status: str
