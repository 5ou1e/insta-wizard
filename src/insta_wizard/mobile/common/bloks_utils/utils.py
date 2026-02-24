import json

from insta_wizard.mobile.common.bloks_utils.bloks_parser import deserialize
from insta_wizard.mobile.exceptions import (
    ResponseParsingError,
)


def deserialize_bloks_action(action: str) -> list:
    try:
        return deserialize(action)
    except Exception:
        raise ResponseParsingError(msg=f"Не удалось десериализовать bloks action: {action}")


def find_action(action, action_name: str | None = None, arg_value: str | None = None):
    if not isinstance(action, list) or len(action) == 0:
        return None

    valid = True

    if action_name:
        valid = action[0] == action_name

    if arg_value and valid:
        valid = arg_value in action

    if valid:
        return action

    for item in action:
        if isinstance(item, list):
            result = find_action(item, action_name, arg_value)
            if result:
                return result

    return None


def find_action_by_arg(action, arg_value: str):
    if not isinstance(action, list) or not action:
        return None

    if arg_value in action:
        return action

    for item in action:
        if isinstance(item, list):
            result = find_action_by_arg(item, arg_value)
            if result:
                return result

    return None


def parse_nested_json(data):
    """Рекурсивно парсит вложенные JSON-строки"""
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
            return parse_nested_json(parsed)
        except json.JSONDecodeError:
            return data
    elif isinstance(data, dict):
        return {k: parse_nested_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [parse_nested_json(item) for item in data]
    else:
        return data
