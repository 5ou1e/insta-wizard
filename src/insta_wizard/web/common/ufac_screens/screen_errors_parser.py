from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GenericScreenError:
    message: str
    light_color: str | None
    dark_color: str | None
    path: tuple[Any, ...]
    source: str


def _parse_hex_color(c: str | None) -> tuple[int, int, int, int] | None:
    if not c or not isinstance(c, str) or not c.startswith("#"):
        return None
    h = c[1:]
    try:
        if len(h) == 8:  # AARRGGBB
            a = int(h[0:2], 16)
            r = int(h[2:4], 16)
            g = int(h[4:6], 16)
            b = int(h[6:8], 16)
            return a, r, g, b
        if len(h) == 6:  # RRGGBB
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            return 255, r, g, b
    except Exception:
        return None
    return None


def _is_error_red(c: str | None) -> bool:
    """
    Более стабильная эвристика "красного алерта", чем (g<=0x45,b<=0x55),
    потому что у IG встречаются более "светлые" красные типа #FFED4956. :contentReference[oaicite:1]{index=1}
    """
    parsed = _parse_hex_color(c)
    if not parsed:
        return False
    _a, r, g, b = parsed
    return r >= 120 and (r - g) >= 40 and (r - b) >= 40


def _iter_nodes(obj: Any, path: tuple[Any, ...] = ()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = path + (k,)
            yield p, k, v, obj
            yield from _iter_nodes(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = path + (i,)
            yield p, i, v, obj
            yield from _iter_nodes(v, p)


def _get_by_path(doc: Any, path: tuple[Any, ...]) -> Any:
    cur = doc
    for k in path:
        cur = cur[k]
    return cur


def _is_inside_clickable(doc: dict[str, Any], path: tuple[Any, ...], max_up: int = 18) -> bool:
    """
    Фильтр от ложных срабатываний: "красные" destructive-action тексты
    обычно лежат внутри дерева с `on_click` / accessibility role Button.
    """
    start = len(path)
    stop = max(start - max_up, 0)
    for i in range(start, stop, -1):
        sub = path[:i]
        try:
            obj = _get_by_path(doc, sub)
        except Exception:
            continue

        if isinstance(obj, dict):
            if "on_click" in obj:
                return True
            exts = obj.get("extensions")
            if isinstance(exts, list):
                for ext in exts:
                    if isinstance(ext, dict) and "bk.components.AccessibilityExtension" in ext:
                        ae = ext["bk.components.AccessibilityExtension"]
                        if isinstance(ae, dict) and ae.get("role") == "Button":
                            return True
    return False


def _get_bloks_payload(doc: dict[str, Any]) -> dict[str, Any]:
    return ((doc.get("payload") or {}).get("layout") or {}).get("bloks_payload") or {}


def _extract_local_state_strings(doc: dict[str, Any]) -> dict[str, str]:
    bp = _get_bloks_payload(doc)
    data = bp.get("data") or []
    ls: dict[str, str] = {}
    if not isinstance(data, list):
        return ls

    for item in data:
        if not isinstance(item, dict) or item.get("type") != "ls":
            continue
        ls_id = item.get("id")
        init = (item.get("data") or {}).get("initial")
        if isinstance(ls_id, str) and isinstance(init, str):
            ls[ls_id] = init
    return ls


_VAR_RE = re.compile(
    r'GetVariableWithScope,\s*"([^"]+)"|GetVariable2,\s*"([^"]+)"|GetVariable,\s*"([^"]+)"'
)


def _extract_ls_ids_used_in_status_alert(doc: dict[str, Any]) -> set[str]:
    """
    Берём только те local_state id, которые реально участвуют в on_bind,
    где присутствует STATUS_ALERT (т.е. речь про error/alert state, а не просто текст). :contentReference[oaicite:2]{index=2}
    """
    ids: set[str] = set()
    for _path, k, v, _parent in _iter_nodes(doc):
        if (
            k == "on_bind"
            and isinstance(v, str)
            and "STATUS_ALERT" in v
            and ('"text"' in v or '"visibility"' in v)
        ):
            for m in _VAR_RE.finditer(v):
                for g in m.groups():
                    if g:
                        ids.add(g)
    return ids


def _extract_local_state_status_errors(doc: dict[str, Any]) -> list[GenericScreenError]:
    ls = _extract_local_state_strings(doc)
    alert_ids = _extract_ls_ids_used_in_status_alert(doc)

    out: list[GenericScreenError] = []
    seen: set[str] = set()

    for ls_id in alert_ids:
        msg = ls.get(ls_id, "")
        msg = msg.strip()
        if not msg:
            continue
        if msg in {"gone", "visible", "enabled", "disabled"}:
            continue

        if msg not in seen:
            seen.add(msg)
            out.append(
                GenericScreenError(
                    message=msg,
                    light_color=None,
                    dark_color=None,
                    path=("ls", ls_id),
                    source="local_state",
                )
            )
    return out


def _extract_themed_colors(node: dict[str, Any]) -> tuple[str | None, str | None]:
    tc = node.get("text_themed_color")
    if isinstance(tc, dict):
        inner = tc.get("bk.types.ThemedColor")
        if isinstance(inner, dict):
            return inner.get("light_color"), inner.get("dark_color")
    return None, None


def _extract_static_red_text_errors(doc: dict[str, Any]) -> list[GenericScreenError]:
    ls_vals = {v.strip() for v in _extract_local_state_strings(doc).values() if isinstance(v, str)}

    out: list[GenericScreenError] = []
    seen: set[str] = set()

    for path, k, v, _parent in _iter_nodes(doc):
        if k not in ("bk.components.Text", "bk.components.RichText", "bk.components.MarkdownText"):
            continue
        if not isinstance(v, dict):
            continue

        text = v.get("text")
        if not isinstance(text, str):
            continue

        msg = text.strip()
        if not msg:
            continue

        if msg in ls_vals:
            continue

        lc, dc = _extract_themed_colors(v)
        if not (_is_error_red(lc) or _is_error_red(dc)):
            continue

        if _is_inside_clickable(doc, path):
            continue

        if msg not in seen:
            seen.add(msg)
            out.append(GenericScreenError(msg, lc, dc, path, source="static_text"))

    return out


def extract_all_generic_errors(doc: dict[str, Any]) -> list[GenericScreenError]:
    errs: list[GenericScreenError] = []
    errs.extend(_extract_local_state_status_errors(doc))
    errs.extend(_extract_static_red_text_errors(doc))

    uniq: list[GenericScreenError] = []
    seen: set[str] = set()
    for e in errs:
        if e.message in seen:
            continue
        seen.add(e.message)
        uniq.append(e)
    return uniq


def has_generic_error(doc: dict[str, Any]) -> bool:
    return len(extract_all_generic_errors(doc)) > 0
