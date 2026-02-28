from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from insta_wizard.common.password_encrypter import (
    PasswordEncrypter,
)
from insta_wizard.common.utils import (
    auth_data_from_authorization_header,
)
from insta_wizard.common.generators import generate_waterfall_id
from insta_wizard.mobile.commands.attestation.create_android_keystore_b_api import (
    AttestationCreateAndroidKeystore,
)
from insta_wizard.mobile.commands.bloks.phone_number_prefill_async import (
    BloksPhoneNumberPrefillAsync,
)
from insta_wizard.mobile.commands.bloks.process_client_data_and_redirect import (
    BloksProcessClientDataAndRedirectBApi,
)
from insta_wizard.mobile.commands.bloks.send_login_request import (
    BloksSendLoginRequest,
)
from insta_wizard.mobile.commands.bloks.youth_regulation_delete_pregent import (
    BloksYouthRegulationDeletePregent,
)
from insta_wizard.mobile.commands.zr.dual_tokens import (
    ZrDualTokens,
)
from insta_wizard.mobile.common.bloks_utils.login_response_parser import (
    AccountNotFoundLoginResult,
    AssistiveLoginConfirmationNeededLoginResult,
    AuthenticationConfiramtionRequiredLoginResult,
    BadPasswordLoginResult,
    BloksCAAAccountRecoveryAuthMethodControllerLoginResult,
    ChallengeRequiredLoginResult,
    SuccessLoginResult,
    TwoStepVerificationRequiredLoginResult,
    UnknownLoginResult,
    parse_bloks_login_response,
)
from insta_wizard.mobile.common.command import (
    Command,
    CommandBus,
    CommandHandler,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.exceptions import (
    BloksLoginAccountNotFoundError,
    BloksLoginAssistiveLoginConfirmationNeededError,
    BloksLoginAuthenticationConfiramtionRequiredError,
    BloksLoginBadPasswordError,
    BloksLoginBloksCAAAccountRecoveryAuthMethodControllerError,
    LoginTwoStepVerificationRequiredError,
    BloksLoginUnknownError,
    ChallengeRequiredError,
    LoginUnknownChallengeRequiredError,
)
from insta_wizard.mobile.models.state import (
    MobileClientState,
)

BloksLoginResult: TypeAlias = None


@dataclass(slots=True)
class BloksLogin(Command[BloksLoginResult]):
    """Авторизоваться в аккаунт с помощью логина и пароля (Bloks версия)"""

    username: str
    password: str


class BloksLoginHandler(CommandHandler[BloksLogin, BloksLoginResult]):
    def __init__(
        self,
        state: MobileClientState,
        api: ApiRequestExecutor,
        bus: CommandBus,
    ) -> None:
        self.state = state
        self.api = api
        self.bus = bus

    async def __call__(self, command: BloksLogin) -> BloksLoginResult:
        self.state.local_data.clear_authorization_data()
        self.state.local_data.set_rur(None)
        self.state.local_data.set_www_claim(None)
        self.state.local_data.set_waterfall_id(generate_waterfall_id())

        await self.send_requests_before_login(waterfall_id=self.state.local_data.waterfall_id)
        return await self._login(
            username=command.username,
            password=command.password,
        )

    async def _login(self, username: str, password: str) -> None:
        if self.state.local_data.public_key and self.state.local_data.public_key_id:
            enc_password = PasswordEncrypter.encrypt_v4(
                password,
                self.state.local_data.public_key_id,
                self.state.local_data.public_key,
            )
        else:
            enc_password = PasswordEncrypter.encrypt_v0(password)

        response = await self.bus.execute(
            BloksSendLoginRequest(username=username, enc_password=enc_password)
        )

        login_result = parse_bloks_login_response(response)

        match login_result:
            case SuccessLoginResult() as r:
                self._update_local_data_from_login_response_data(r.login_response_data)
                return

            case AccountNotFoundLoginResult():
                raise BloksLoginAccountNotFoundError(response_json=response)

            case ChallengeRequiredLoginResult() as r:
                raise LoginUnknownChallengeRequiredError(
                    challenge_data=r.challenge_data,
                    response_json=response,
                )

            case TwoStepVerificationRequiredLoginResult():
                raise LoginTwoStepVerificationRequiredError(response_json=response)

            case BadPasswordLoginResult():
                raise BloksLoginBadPasswordError(response_json=response)

            case AssistiveLoginConfirmationNeededLoginResult():
                raise BloksLoginAssistiveLoginConfirmationNeededError(response_json=response)

            case AuthenticationConfiramtionRequiredLoginResult() as r:
                raise BloksLoginAuthenticationConfiramtionRequiredError(
                    response_json=response,
                    masked_email=r.masked_email,
                )

            case BloksCAAAccountRecoveryAuthMethodControllerLoginResult():
                raise BloksLoginBloksCAAAccountRecoveryAuthMethodControllerError(
                    response_json=response
                )

            case UnknownLoginResult():
                raise BloksLoginUnknownError(response_json=response)

            case _:
                raise BloksLoginUnknownError(response_json=response)

    async def send_requests_before_login(self, waterfall_id: str) -> None:
        await self.bus.execute(ZrDualTokens())
        await self.bus.execute(AttestationCreateAndroidKeystore())
        await self.bus.execute(
            BloksProcessClientDataAndRedirectBApi(
                waterfall_id=waterfall_id,
            )
        )
        await self.bus.execute(BloksYouthRegulationDeletePregent())
        await self.bus.execute(BloksPhoneNumberPrefillAsync())

    def _update_local_data_from_login_response_data(self, login_response_data: dict):
        headers_raw = login_response_data.get("headers", {})
        headers = {k.lower(): v for k, v in headers_raw.items()}

        authorization = headers.get("ig-set-authorization", "")
        self.state.local_data.set_authorization_data(
            auth_data_from_authorization_header(authorization)
        )

        www_claim = headers.get("x-ig-set-www-claim")
        if www_claim:
            self.state.local_data.set_www_claim(www_claim)

        rur = headers.get("ig-set-ig-u-rur")
        if rur:
            self.state.local_data.set_rur(rur)

        password_key_id = headers.get("ig-set-password-encryption-key-id")
        if password_key_id:
            self.state.local_data.set_public_key_id(int(password_key_id))

        password_pub_key = headers.get("ig-set-password-encryption-pub-key")
        if password_pub_key:
            self.state.local_data.set_public_key(password_pub_key)

        logged_in_user = login_response_data.get("login_response", {}).get("logged_in_user", {})
        session_flush_nonce = logged_in_user.get("session_flush_nonce")
        if session_flush_nonce:
            self.state.local_data.set_session_flush_nonce(session_flush_nonce)
