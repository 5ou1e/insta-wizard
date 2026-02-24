from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(*cmd: str) -> None:
    print("Running:", " ".join(cmd))
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise SystemExit(r.returncode)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["fix", "format", "lint", "type", "test", "check"])
    args = p.parse_args()

    root = Path.cwd()
    src = str(root / "src")
    tests = str(root / "tests")

    if args.cmd == "fix":
        run(sys.executable, "-m", "ruff", "check", "--fix", src, tests)
        run(sys.executable, "-m", "ruff", "format", src, tests)
        return

    if args.cmd == "format":
        run(sys.executable, "-m", "ruff", "format", src, tests)
        return

    if args.cmd == "lint":
        run(sys.executable, "-m", "ruff", "check", src, tests)
        return

    if args.cmd == "type":
        run(sys.executable, "-m", "mypy", src)
        return

    if args.cmd == "test":
        run(sys.executable, "-m", "pytest", "-v")
        return

    if args.cmd == "check":
        run(sys.executable, "-m", "ruff", "check", src, tests)
        run(sys.executable, "-m", "mypy", src)
        run(sys.executable, "-m", "pytest", "-q")
        return


if __name__ == "__main__":
    main()
