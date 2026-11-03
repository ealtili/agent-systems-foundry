"""Tool registry. You implement it; tests/test_registry.py is the contract."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    args_model: type[BaseModel]
    handler: Callable[[Any], str]


class Registry:
    def register(self, tool: Tool) -> None:
        """Add a tool.

        Raises ValueError for a duplicate name, or a name that does not match the harness
        convention ^[a-z][a-z0-9_]{0,63}$.
        """
        raise NotImplementedError

    def get(self, name: str) -> Tool | None:
        """Return the tool, or None if it is not registered."""
        raise NotImplementedError

    def names(self) -> list[str]:
        """Registered tool names, sorted."""
        raise NotImplementedError

    def schemas(self, *, strict: bool = False) -> list[dict[str, Any]]:
        """Tool definitions for the API, sorted by tool name.

        Each entry is {"name", "description", "input_schema"} where input_schema comes from the
        args model's JSON schema with every schema-level "title" keyword removed, recursively.
        A property that is itself NAMED "title" must be kept. The output must be byte-stable:
        the same tools registered in any order give identical json.dumps output (it is part of
        the cache prefix, see Lab 03). With strict=True each entry also carries "strict": True.
        """
        raise NotImplementedError
