"""Characterization tests for the SDK itself (given, expected to pass).

They pin what the installed SDK does under faults. If an SDK upgrade changes any of this, these
fail first: that is the point. Timing assertions use lower bounds with generous slack.
"""

import asyncio
import time
from typing import Any

import anthropic
import pytest
from src.faults import Fault, make_client


async def ask(client: anthropic.AsyncAnthropic, **kw: Any) -> str:
    msg = await client.messages.create(
        model="claude-haiku-5-5", max_tokens=16, messages=[{"role": "user", "content": "x"}], **kw
    )
    return "".join(b.text for b in msg.content if b.type == "text")


async def test_healthy_call() -> None:
    client, transport = make_client(lambda n: Fault("ok"), timeout=5, max_retries=2)
    assert await ask(client) == "hi"
    assert transport.attempts == 1


async def test_sdk_retries_server_errors_then_succeeds() -> None:
    script = lambda n: Fault("status", 500) if n < 3 else Fault("ok")  # noqa: E731
    client, transport = make_client(script, timeout=5, max_retries=2)
    assert await ask(client) == "hi"
    assert transport.attempts == 3


async def test_sdk_obeys_retry_after_between_retries() -> None:
    script = lambda n: Fault("status", 429, retry_after_ms=200)  # noqa: E731
    client, transport = make_client(script, timeout=5, max_retries=2)
    start = time.monotonic()
    with pytest.raises(anthropic.RateLimitError):
        await ask(client)
    assert transport.attempts == 3
    assert time.monotonic() - start >= 0.4  # two waits of 0.2 s


async def test_retries_multiply_the_timeout() -> None:
    client, transport = make_client(lambda n: Fault("hang"), timeout=0.2, max_retries=1)
    start = time.monotonic()
    with pytest.raises(anthropic.APITimeoutError):
        await ask(client)
    assert transport.attempts == 2
    assert time.monotonic() - start >= 0.4  # 2 attempts x 0.2 s, plus backoff on top


async def test_an_outer_deadline_cancels_everything_beneath_it() -> None:
    client, transport = make_client(lambda n: Fault("hang"), timeout=30, max_retries=2)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        async with asyncio.timeout(0.3):
            await ask(client)
    assert time.monotonic() - start < 2.0
    assert transport.attempts == 1
