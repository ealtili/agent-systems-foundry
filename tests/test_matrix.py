import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATRIX = ROOT / "docs" / "CAPABILITY_MATRIX.md"


def lab_numbers() -> set[int]:
    return {int(p.name[:2]) for p in (ROOT / "labs").iterdir() if p.name[:2].isdigit()}


def test_matrix_references_only_existing_labs() -> None:
    referenced = {int(n) for n in re.findall(r"Lab (\d\d)", MATRIX.read_text(encoding="utf-8"))}
    assert referenced, "matrix should reference labs"
    assert referenced <= lab_numbers(), f"missing labs: {sorted(referenced - lab_numbers())}"


def test_unintroduced_capabilities_are_marked_planned() -> None:
    for row in MATRIX.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in row.split("|")]
        if len(cells) > 8 and cells[2] == "Planned":
            assert "Planned" in cells[-2], f"row not marked Planned: {cells[1]}"


def test_referenced_docs_exist() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    for rel in set(re.findall(r"`(docs/[A-Za-z0-9_./-]+\.md)`", text)):
        assert (ROOT / rel).exists(), f"missing doc: {rel}"
