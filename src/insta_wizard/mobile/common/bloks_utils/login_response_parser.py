import json
import re
from dataclasses import dataclass

from insta_wizard.common.utils import MASKED_EMAIL_RE
from insta_wizard.mobile.common.bloks_utils.utils import (
    deserialize_bloks_action,
    find_action,
    parse_nested_json,
)
from insta_wizard.mobile.exceptions import (
    ResponseParsingError,
)
from insta_wizard.mobile.models.challenge import (
    ChallengeRequiredData,
)

UNICODE_ESCAPE_RE = re.compile(r"\\u[0-9a-fA-F]{4}")


@dataclass
class SuccessLoginResult:
    login_response_data: dict


@dataclass
class ChallengeRequiredLoginResult:
    challenge_data: ChallengeRequiredData


@dataclass
class TwoStepVerificationRequiredLoginResult:
    data: dict


@dataclass
class UnknownLoginResult:
    response: dict


@dataclass
class AccountNotFoundLoginResult:
    response: dict


@dataclass
class BadPasswordLoginResult:
    response: dict


@dataclass
class AssistiveLoginConfirmationNeededLoginResult:
    response: dict


@dataclass
class AuthenticationConfiramtionRequiredLoginResult:
    response: dict
    masked_email: str | None


@dataclass
class BloksCAAAccountRecoveryAuthMethodControllerLoginResult:
    response: dict


def get_action_from_bloks_response(response: dict):
    return response.get("layout", {}).get("bloks_payload", {}).get("action", "")


def parse_bloks_login_response(
    response: dict,
) -> (
    SuccessLoginResult
    | ChallengeRequiredLoginResult
    | UnknownLoginResult
    | TwoStepVerificationRequiredLoginResult
    | AccountNotFoundLoginResult
    | BadPasswordLoginResult
    | AssistiveLoginConfirmationNeededLoginResult
    | AuthenticationConfiramtionRequiredLoginResult
    | BloksCAAAccountRecoveryAuthMethodControllerLoginResult
):
    action_string = get_action_from_bloks_response(response)
    response_string = str(response)

    if not action_string:
        raise ResponseParsingError(msg="Отсутствует поле action в BloksLogin response")

    if "bk.action.caa.HandleLoginResponse" in action_string:
        action = deserialize_bloks_action(action_string)

        handle_login_response_action = find_action(action, "bk.action.caa.HandleLoginResponse")
        if handle_login_response_action:
            return SuccessLoginResult(
                login_response_data=extract_login_response_data_from_action(
                    handle_login_response_action
                )
            )

    if "lookup_query_not_associated_with_account" in action_string:
        return AccountNotFoundLoginResult(response=response)

    if "com.bloks.www.ap.two_step_verification.entrypoint_async" in action_string:
        action = deserialize_bloks_action(action_string)

        two_step_verification_action = find_action(
            action, arg_value="com.bloks.www.ap.two_step_verification.entrypoint_async"
        )

        if two_step_verification_action:
            data = extract_two_step_verification_action_data(two_step_verification_action)
            return TwoStepVerificationRequiredLoginResult(data=data)

    # if "com.bloks.www.ap.two_step_verification.challenge_picker" in response_string:
    #     return TwoStepVerificationRequiredLoginResult(data={})

    if "com.bloks.www.two_step_verification.entrypoint" in action_string:
        action = deserialize_bloks_action(action_string)
        two_step_verification_action = find_action(
            action, arg_value="com.bloks.www.two_step_verification.entrypoint"
        )
        if two_step_verification_action:
            return TwoStepVerificationRequiredLoginResult(data={})

    if "bk.action.caa.PresentCheckpointsFlow" in action_string:
        action = deserialize_bloks_action(action_string)
        checkpoint_action = find_action(action, "bk.action.caa.PresentCheckpointsFlow")
        if checkpoint_action:
            challenge_data = extract_challenge_data_from_action(checkpoint_action)
            return ChallengeRequiredLoginResult(challenge_data=challenge_data)

    if "login_wrong_password_error_dialog_shown" in response_string:
        return BadPasswordLoginResult(response=response)

    if "login_wrong_username_error_dialog_shown" in response_string:
        return AccountNotFoundLoginResult(response=response)

    if "com.bloks.www.caa.assistive_login_confirmation" in action_string:
        return AssistiveLoginConfirmationNeededLoginResult(response=response)

    if (
        "password_form_incorrect_password_ok_clicked_client" in str(response)
        and "ig.action.cdsdialog.OpenDialog" in action_string
    ):
        return BadPasswordLoginResult(response=response)

    if "com.bloks.www.caa.ar.authentication_confirmation" in action_string:
        response_string = UNICODE_ESCAPE_RE.sub("", response_string)
        m = MASKED_EMAIL_RE.search(response_string)

        masked_email = m.group(0) if m else None
        return AuthenticationConfiramtionRequiredLoginResult(
            response=response,
            masked_email=masked_email,
        )

    if "push_screen_BloksCAAAccountRecoveryAuthMethodController" in action_string:
        return BloksCAAAccountRecoveryAuthMethodControllerLoginResult(response=response)

    return UnknownLoginResult(response=response)


def extract_two_step_verification_action_data(
    two_step_verification_action: list,
) -> dict:
    try:
        map_make = find_action(two_step_verification_action, action_name="bk.action.map.Make")
        names = [val for val in map_make[1][1:]]
        values = [val for val in map_make[2][1:]]
        return dict(zip(names, values, strict=True))
    except Exception:
        raise ResponseParsingError(msg="Не удалось извлечь данные для two_step_verification_action")


def extract_login_response_data_from_action(handle_login_response_action: list) -> dict:
    try:
        tree_make = find_action(handle_login_response_action, "bk.action.tree.Make")
        if tree_make:
            login_response_string = tree_make[3]
            return parse_nested_json(login_response_string)
    except Exception:
        raise ResponseParsingError(
            msg="Не удалось извлечь login_response_data из HandleLoginResponse action"
        )

    raise ResponseParsingError(
        msg="Не удалось извлечь login_response_data из HandleLoginResponse action"
    )


def extract_challenge_data_from_action(checkpoint_action: list) -> ChallengeRequiredData:
    challenge_data = json.loads(checkpoint_action[1])["error"]["error_data"]
    return ChallengeRequiredData(**challenge_data)
