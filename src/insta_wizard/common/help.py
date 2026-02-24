from __future__ import annotations

import importlib
import inspect
import re
import textwrap
from collections.abc import Iterable

from rich.console import Console
from rich.table import Table

_EMPTY = inspect._empty
_QUALNAME_RE = re.compile(r"\b(?:[A-Za-z_]\w*\.)+([A-Za-z_]\w*)\b")
_CLASS_REPR_RE = re.compile(r"<class '([^']+)'>")


def _iter_public_classes(pkg: str) -> list[type]:
    mod = importlib.import_module(pkg)

    names: Iterable[str]
    if hasattr(mod, "__all__"):
        names = mod.__all__
    else:
        names = [n for n in dir(mod) if not n.startswith("_")]

    out: list[type] = []
    for name in names:
        obj = getattr(mod, name, None)
        if inspect.isclass(obj):
            out.append(obj)
    out.sort(key=lambda c: c.__name__)
    return out


def _sig_raw(cls: type) -> str:
    try:
        return str(inspect.signature(cls))
    except (TypeError, ValueError):
        return "()"


def _strip_class_repr_str(s: str) -> str:
    """
    "<class 'pkg.X'>" -> "X"
    "<class 'X'>"     -> "X"
    """
    m = _CLASS_REPR_RE.fullmatch(s.strip())
    if not m:
        return s
    return m.group(1).split(".")[-1]


def _shorten_annotation(ann: object) -> str:
    if ann is _EMPTY:
        return ""

    if inspect.isclass(ann):
        return ann.__name__

    if isinstance(ann, str):
        s = ann
    else:
        try:
            if getattr(ann, "__module__", None) == "builtins" and hasattr(ann, "__name__"):
                s = ann.__name__
            else:
                s = str(ann)
        except Exception:
            s = str(ann)

    s = _strip_class_repr_str(s)

    s = s.replace("typing.", "").replace("types.", "")
    s = _QUALNAME_RE.sub(r"\1", s)

    s = _strip_class_repr_str(s)

    return s


def _shorten_default(val: object) -> str:
    if val is _EMPTY:
        return ""

    if inspect.isclass(val):
        return val.__name__

    if callable(val) and hasattr(val, "__name__"):
        name = getattr(val, "__name__", "")
        if name and name != "<lambda>":
            return name

    s = repr(val)

    m = _CLASS_REPR_RE.fullmatch(s)
    if m:
        return m.group(1).split(".")[-1]

    s = s.replace("typing.", "").replace("types.", "")
    s = _QUALNAME_RE.sub(r"\1", s)

    return s


def _format_signature(sig: inspect.Signature) -> str:
    parts: list[str] = []
    inserted_kwonly_star = False

    params = list(sig.parameters.values())

    has_var_positional = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params)

    for p in params:
        if (
            p.kind == inspect.Parameter.KEYWORD_ONLY
            and not has_var_positional
            and not inserted_kwonly_star
        ):
            parts.append("*")
            inserted_kwonly_star = True

        prefix = ""
        if p.kind == inspect.Parameter.VAR_POSITIONAL:
            prefix = "*"
        elif p.kind == inspect.Parameter.VAR_KEYWORD:
            prefix = "**"

        ann = _shorten_annotation(p.annotation)
        default = _shorten_default(p.default)

        chunk = f"{prefix}{p.name}"
        if ann:
            chunk += f": {ann}"
        if default:
            chunk += f" = {default}"

        parts.append(chunk)

    s = f"({', '.join(parts)})"

    ret = _shorten_annotation(sig.return_annotation)
    if ret:
        s += f" -> {ret}"

    return s


def _sig(cls: type) -> str:
    try:
        sig = inspect.signature(cls)
    except (TypeError, ValueError):
        return "()"
    return _format_signature(sig)


def _summary(cls: type, width: int) -> str:

    raw = (cls.__doc__ or "").strip()
    if not raw:
        return "[dim]—[/dim]"

    sig_raw = _sig_raw(cls)
    auto1 = f"{cls.__name__}{sig_raw}"
    auto2 = f"{cls.__name__}{sig_raw.split(' -> ')[0]}"

    raw_norm = " ".join(raw.split())
    if raw_norm in {" ".join(auto1.split()), " ".join(auto2.split())}:
        return "[dim]—[/dim]"

    doc = inspect.getdoc(cls) or raw
    first = doc.strip().splitlines()[0]
    return textwrap.shorten(first, width=width, placeholder="…")


def _print_help(
    base_pkg: str,
    *,
    title: str | None = None,
    groups: tuple[str, ...] = ("commands", "flows"),
    show_module: bool = False,
    max_desc: int = 140,
    console_width: int = 160,
) -> None:
    console = Console(width=console_width, force_terminal=True)

    console.print(f"[bold]{title or base_pkg}[/bold]", justify="center")
    console.print()

    table = Table(show_header=True, header_style="bold", expand=True)
    table.add_column("Group", no_wrap=True, width=12)
    table.add_column("Name", no_wrap=True, style="bold", width=40)

    table.add_column("Description", overflow="fold", ratio=4)
    table.add_column("Signature", overflow="fold", ratio=3)

    if show_module:
        table.add_column("Module", overflow="fold", ratio=2, style="dim")

    any_rows = False

    for group in groups:
        pkg = f"{base_pkg}.{group}"
        try:
            classes = _iter_public_classes(pkg)
        except ModuleNotFoundError:
            continue

        for cls in classes:
            any_rows = True
            desc = _summary(cls, max_desc)
            row = [group, cls.__name__, desc, _sig(cls)]
            if show_module:
                row.append(cls.__module__)
            table.add_row(*row)

    if not any_rows:
        console.print("[dim]No exports found.[/dim]")
        return

    console.print(table)
