"""Silent-invalidator detector. You implement it; tests/test_prefix.py is the contract."""

from collections.abc import Mapping, Sequence
from typing import NamedTuple


class Divergence(NamedTuple):
    section: str
    position: int


def render_blocks(request: Mapping[str, Sequence[object]]) -> list[tuple[str, int, str]]:
    """Flatten a request into (section, index, serialized_bytes) in cache render order.

    Order is tools, then system, then messages. A missing section is empty. Each block is
    serialized with json.dumps(block, separators=(",", ":"), ensure_ascii=False) and WITHOUT
    sorting keys, because the cache matches exact bytes.
    """
    raise NotImplementedError


def first_divergence(
    prev: Mapping[str, Sequence[object]], cur: Mapping[str, Sequence[object]]
) -> Divergence | None:
    """First position where the rendered prefix of `cur` differs from `prev`.

    Compare the flattened blocks pairwise up to the shorter length. Return the section and the
    position within that section of the block in `cur` at the first differing place. If one
    request is a prefix of the other (a pure append or a truncation), the cache prefix is
    intact: return None.
    """
    raise NotImplementedError
