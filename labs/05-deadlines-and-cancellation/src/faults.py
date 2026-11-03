"""Fault injection through the REAL Anthropic SDK code path. Given code.

The SDK is pointed at an in-process transport that fails on a script, so retries, backoff,
Retry-After handling and timeouts run for real, offline, for free.

NOTE: this imports `httpx2`, which the `anthropic` package (2.4.0) depends on but this repo does
not declare. If a future SDK swaps its HTTP client, this is the one file to fix, and
tests/test_faults.py will tell you.
"""

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

import anthropic
import httpx2


@dataclass(frozen=True)
class Fault:
    kind: Literal["ok", "status", "hang"]
    status: int = 200
    retry_after_ms: int | None = None


Script = Callable[[int], Fault]  # attempt number (1-based) -> what the "server" does


def ok_body(text: str = "hi") -> dict[str, Any]:
    return {
        "id": "msg_test",
        "type": "message",
        "role": "assistant",
        "model": "claude-haiku-5-5",
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 3, "output_tokens": 1},
    }


class FaultTransport:
    """Counts attempts that reach the 'endpoint' and misbehaves on a script."""

    def __init__(self, script: Script) -> None:
        self.script = script
        self.attempts = 0

    async def __call__(self, request: httpx2.Request) -> httpx2.Response:
        self.attempts += 1
        fault = self.script(self.attempts)
        if fault.kind == "hang":
            # A real transport raises a read timeout when no bytes arrive for `read` seconds.
            read = request.extensions.get("timeout", {}).get("read")
            await asyncio.sleep(float(read) if read is not None else 3600.0)
            raise httpx2.ReadTimeout("injected hang", request=request)
        if fault.kind == "status":
            headers = {}
            if fault.retry_after_ms is not None:
                headers["retry-after-ms"] = str(fault.retry_after_ms)
            body = {"type": "error", "error": {"type": "api_error", "message": "injected"}}
            return httpx2.Response(fault.status, headers=headers, json=body, request=request)
        return httpx2.Response(200, json=ok_body(), request=request)


def make_client(
    script: Script, *, timeout: float | None, max_retries: int
) -> tuple[anthropic.AsyncAnthropic, FaultTransport]:
    transport = FaultTransport(script)
    http = httpx2.AsyncClient(transport=httpx2.MockTransport(transport))
    client = anthropic.AsyncAnthropic(
        api_key="test-key-not-real", http_client=http, timeout=timeout, max_retries=max_retries
    )
    return client, transport


def _healthy(n: int) -> Fault:
    return Fault("ok")


def _flaky(n: int) -> Fault:
    return Fault("status", 500) if n <= 2 else Fault("ok")


def _rate_limited(n: int) -> Fault:
    return Fault("status", 429, retry_after_ms=2000)


def _slow_recovery(n: int) -> Fault:
    return Fault("status", 429, retry_after_ms=1500) if n == 1 else Fault("ok")


def _hang(n: int) -> Fault:
    return Fault("hang")


def _dead(n: int) -> Fault:
    return Fault("status", 500)


SCENARIOS: dict[str, Script] = {
    "healthy": _healthy,
    "flaky": _flaky,
    "rate_limited": _rate_limited,
    "slow_recovery": _slow_recovery,
    "hang": _hang,
    "dead": _dead,
}
