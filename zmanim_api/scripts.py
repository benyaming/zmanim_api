from __future__ import annotations

import subprocess
import sys


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, check=False)
    raise SystemExit(result.returncode)


def tests() -> None:
    _run([sys.executable, "-m", "coverage", "run", "-m", "pytest", "-v", "test/"])


def xml() -> None:
    _run([sys.executable, "-m", "coverage", "xml"])
