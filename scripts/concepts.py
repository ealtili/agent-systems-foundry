"""Spaced-repetition concept store (Leitner boxes).

Content lives in `labs/<lab>/concepts.json`; learner state lives in
`.foundry/concepts_state.json`. CLI:

    uv run python scripts/concepts.py add <lab-dir-name>
    uv run python scripts/concepts.py due [--n 3] [--exclude-lab <lab-dir-name>]
    uv run python scripts/concepts.py grade <card-id> pass|fail
    uv run python scripts/concepts.py stats
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

from pydantic import BaseModel, Field, TypeAdapter, ValidationError

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / ".foundry" / "concepts_state.json"
INTERVALS_DAYS: tuple[int, ...] = (1, 3, 7, 14, 30)


class Concept(BaseModel):
    """One authored question (trust boundary: file written by a human/Claude)."""

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$")
    question: str = Field(min_length=10)
    hint: str = ""


class Card(BaseModel):
    id: str
    lab: str
    question: str
    hint: str = ""
    box: int = Field(default=0, ge=0, le=len(INTERVALS_DAYS))
    due: date
    history: list[tuple[date, bool]] = Field(default_factory=list)


class Store(BaseModel):
    cards: dict[str, Card] = Field(default_factory=dict)


def load(path: Path = STATE_PATH) -> Store:
    if not path.exists():
        return Store()
    return Store.model_validate_json(path.read_text(encoding="utf-8"))


def save(store: Store, path: Path = STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(store.model_dump_json(indent=2), encoding="utf-8")
    os.replace(tmp, path)


def register(store: Store, lab_dir: Path, today: date) -> int:
    """Add unseen concepts from a lab. Returns the number of new cards."""
    source = lab_dir / "concepts.json"
    concepts = TypeAdapter(list[Concept]).validate_json(source.read_text(encoding="utf-8"))
    added = 0
    for c in concepts:
        key = f"{lab_dir.name}:{c.id}"
        if key not in store.cards:
            store.cards[key] = Card(
                id=key, lab=lab_dir.name, question=c.question, hint=c.hint, due=today
            )
            added += 1
    return added


def due(store: Store, today: date, n: int, exclude_lab: str | None = None) -> list[Card]:
    pool = [c for c in store.cards.values() if c.due <= today and c.lab != exclude_lab]
    pool.sort(key=lambda c: (c.due, c.box, c.id))
    return pool[:n]


def grade(store: Store, card_id: str, passed: bool, today: date) -> Card:
    card = store.cards[card_id]
    card.history.append((today, passed))
    if passed:
        card.box = min(card.box + 1, len(INTERVALS_DAYS))
        card.due = today + timedelta(days=INTERVALS_DAYS[card.box - 1])
    else:
        card.box = 0
        card.due = today + timedelta(days=1)
    return card


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add")
    p_add.add_argument("lab")
    p_due = sub.add_parser("due")
    p_due.add_argument("--n", type=int, default=3)
    p_due.add_argument("--exclude-lab", default=None)
    p_grade = sub.add_parser("grade")
    p_grade.add_argument("card_id")
    p_grade.add_argument("result", choices=["pass", "fail"])
    sub.add_parser("stats")
    args = parser.parse_args(argv)

    today = date.today()
    try:
        store = load()
        if args.cmd == "add":
            lab_dir = ROOT / "labs" / args.lab
            print(f"added {register(store, lab_dir, today)} card(s) from {args.lab}")
            save(store)
        elif args.cmd == "due":
            for card in due(store, today, args.n, args.exclude_lab):
                print(json.dumps({"id": card.id, "box": card.box, "question": card.question}))
        elif args.cmd == "grade":
            card = grade(store, args.card_id, args.result == "pass", today)
            print(f"{card.id}: box={card.box} next due {card.due}")
            save(store)
        else:
            boxes = [sum(1 for c in store.cards.values() if c.box == b) for b in range(6)]
            print(f"cards={len(store.cards)} per-box={boxes}")
    except (ValidationError, FileNotFoundError, KeyError) as err:
        print(f"error: {err!r}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
