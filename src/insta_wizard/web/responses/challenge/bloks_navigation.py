from typing import TypedDict


class BloksNavigationTakeChallengeResponse(TypedDict):
    """
    Response example:
        {
            "layout": {
                "bloks_payload": {
                    "data": [],
                    "tree": {
                        "bk.components.internal.Action": {
                            "handler": "(bk.action.core.TakeLast, (ig.action.navigation.ClearChallenge), (ig.action.navigation.CloseToScreen, (bk.action.i64.Const, 11), (bk.action.bool.Const, true)), (bk.action.i32.Const, 1))"
                        }
                    },
                    "embedded_payloads": [],
                    "error_attribution": {
                        "logging_id": "{\"callsite\":\"{\\\"oncall\\\":\\\"igwb_experiences\\\",\\\"feature\\\":\\\"HandlerForAsyncTakeChallenge\\\",\\\"product\\\":\\\"bloks_async_component\\\"}\",\"push_phase\":\"c2\"}",
                        "source_map_id": "(distillery_unknown)"
                    }
                }
            },
            "status": "ok"
        }
    """

    pass
