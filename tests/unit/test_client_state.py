"""
Тесты для MobileInstagramClient.dump_state() / load_state().
Внешних сервисов не требует.
"""

import pytest

from insta_wizard.common.exceptions import InstaWizardError
from insta_wizard.mobile.client import MobileInstagramClient
from insta_wizard.mobile.models.android_device_info import AndroidDeviceInfo, AndroidPreset


@pytest.fixture()
async def client():
    c = MobileInstagramClient(
        device=AndroidDeviceInfo.from_preset(AndroidPreset.SAMSUNG_A16, locale="ru_RU")
    )
    yield c
    await c.close()


class TestDumpLoadStateValid:
    async def test_dump_contains_expected_keys(self, client):
        state = client.dump_state()
        assert set(state.keys()) == {"version", "device", "local_data"}

    async def test_load_restores_device(self, client):
        state = client.dump_state()

        other = MobileInstagramClient(
            device=AndroidDeviceInfo.from_preset(AndroidPreset.PIXEL_8, locale="de_DE")
        )
        assert other.state.device.model != client.state.device.model

        other.load_state(state)
        assert other.state.device.model == client.state.device.model
        assert other.state.device.locale == client.state.device.locale
        await other.close()

    async def test_load_restores_local_data(self, client):
        client.state.local_data.user_id = "999888777"
        client.state.local_data.mid = "test_mid_xyz"

        state = client.dump_state()

        other = MobileInstagramClient()
        other.load_state(state)
        assert other.state.local_data.user_id == "999888777"
        assert other.state.local_data.mid == "test_mid_xyz"
        await other.close()

    async def test_load_restores_version(self, client):
        state = client.dump_state()
        other = MobileInstagramClient()
        other.load_state(state)
        assert other.state.version_info.version == client.state.version_info.version
        await other.close()

    async def test_headers_reflect_loaded_device(self, client):
        """После load_state заголовки должны содержать UA нового устройства."""
        state = client.dump_state()

        other = MobileInstagramClient(device=AndroidDeviceInfo.from_preset(AndroidPreset.PIXEL_8))
        other.load_state(state)

        ua = other._headers.api_headers()["User-Agent"]
        assert client.state.device.model in ua
        await other.close()

    async def test_dump_load_roundtrip_via_json(self, client):
        """dump → orjson → load должен давать идентичный стейт."""
        import orjson

        client.state.local_data.user_id = "123"
        state = orjson.loads(orjson.dumps(client.dump_state()))

        other = MobileInstagramClient()
        other.load_state(state)
        assert other.state.local_data.user_id == "123"
        assert other.state.device.model == client.state.device.model
        await other.close()


class TestLoadStateInvalid:
    async def test_missing_version_raises(self, client):
        state = client.dump_state()
        del state["version"]
        with pytest.raises(InstaWizardError):
            client.load_state(state)

    async def test_unknown_version_raises(self, client):
        state = client.dump_state()
        state["version"] = "0.0.0.0.0"
        with pytest.raises(InstaWizardError):
            client.load_state(state)

    async def test_malformed_device_raises(self, client):
        state = client.dump_state()
        state["device"] = {"bad": "data"}
        with pytest.raises(InstaWizardError):
            client.load_state(state)

    async def test_missing_local_data_raises(self, client):
        state = client.dump_state()
        del state["local_data"]
        with pytest.raises(InstaWizardError):
            client.load_state(state)

    async def test_state_unchanged_after_failed_load(self, client):
        """При неудачной загрузке оригинальный стейт не должен быть испорчен."""
        original_model = client.state.device.model
        original_user_id = client.state.local_data.user_id

        with pytest.raises(InstaWizardError):
            client.load_state({"version": "bad", "device": {}, "local_data": {}})

        assert client.state.device.model == original_model
        assert client.state.local_data.user_id == original_user_id
