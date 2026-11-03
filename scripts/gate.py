"""Deterministic mastery gate: `uv run python scripts/gate.py <lab-dir-name> [--mark]`.

Checks evidence, not honesty. Exit 0 only if every check passes. With --mark,
rewrites the lab's row in PROGRESS.md to `[*]` (the only sanctioned writer).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = re.compile(r"\[Record[^\]]*\]|\[Explain[^\]]*\]|TODO", re.IGNORECASE)
CMD_TIMEOUT_S = 300


def run(cmd: list[str]) -> bool:
    try:
        return subprocess.run(cmd, cwd=ROOT, timeout=CMD_TIMEOUT_S).returncode == 0
    except subprocess.TimeoutExpired:
        return False


def field(text: str, label: str) -> str:
    m = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.*)", text)
    return m.group(1).strip() if m else ""


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    lab = ROOT / "labs" / sys.argv[1]
    if not lab.is_dir():
        print(f"no such lab: {lab}")
        return 2

    results: dict[str, bool] = {}
    results["G1 ruff"] = run(["uv", "run", "ruff", "check", str(lab)])
    results["G1 mypy"] = run(
        ["uv", "run", "mypy", "--strict", str(lab / "src"), str(lab / "tests")]
    )
    results["G2 pytest"] = run(["uv", "run", "pytest", str(lab / "tests"), "-q"])

    state = (lab / "STATE.md").read_text(encoding="utf-8") if (lab / "STATE.md").exists() else ""
    for label in ("User Prediction", "Observed Result", "Variance Analysis"):
        value = field(state, label)
        results[f"STATE {label} filled"] = bool(value) and not PLACEHOLDER.search(value)

    defense = lab / "DEFENSE.md"
    text = defense.read_text(encoding="utf-8") if defense.exists() else ""
    results["DEFENSE Q1-Q5 answered"] = all(
        re.search(rf"^##\s*Q{i}\b.*\n+\S", text, re.MULTILINE) for i in range(1, 6)
    )

    for name, ok in results.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not all(results.values()):
        return 1

    if "--mark" in sys.argv:
        number = sys.argv[1].split("-")[0]
        progress = ROOT / "PROGRESS.md"
        lines = progress.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if line.startswith(f"| **{number}**"):
                cells = line.split("|")
                cells[3:9] = [" [*] "] * 6
                cells[-2] = " `[*]` "
                lines[i] = "|".join(cells)
        progress.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"PROGRESS.md updated for lab {number}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
