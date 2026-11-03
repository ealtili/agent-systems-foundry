import anthropic
import httpx2
from src.classify import classify_sdk_error
from src.retry import RetryableError

REQ = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")


def status_error(status: int, **headers: str) -> anthropic.APIStatusError:
    response = httpx2.Response(status, headers=headers, request=REQ)
    return anthropic.APIStatusError("api said no", response=response, body=None)


def retry_after_of(err: BaseException) -> float | None:
    got = classify_sdk_error(err)
    assert got is not None
    return got.retry_after


def test_timeouts_and_connection_errors_are_retryable() -> None:
    for err in (
        anthropic.APITimeoutError(request=REQ),
        anthropic.APIConnectionError(message="x", request=REQ),
    ):
        got = classify_sdk_error(err)
        assert isinstance(got, RetryableError)
        assert got.retry_after is None
        assert type(err).__name__ in str(got)


def test_retryable_status_codes() -> None:
    for status in (408, 409, 429, 500, 502, 503, 529):
        got = classify_sdk_error(status_error(status))
        assert isinstance(got, RetryableError), status


def test_client_errors_are_not_retryable() -> None:
    for status in (400, 401, 403, 404, 422):
        assert classify_sdk_error(status_error(status)) is None, status


def test_other_exceptions_are_not_retryable() -> None:
    assert classify_sdk_error(ValueError("bug")) is None
    assert classify_sdk_error(KeyError("bug")) is None


def test_retry_after_ms_wins_over_retry_after() -> None:
    got = classify_sdk_error(status_error(429, **{"retry-after-ms": "1500", "retry-after": "9"}))
    assert got is not None and got.retry_after == 1.5


def test_retry_after_seconds_and_floats() -> None:
    assert retry_after_of(status_error(429, **{"retry-after": "7"})) == 7.0
    assert retry_after_of(status_error(503, **{"retry-after": "0.25"})) == 0.25


def test_dates_and_garbage_count_as_absent() -> None:
    date = "Wed, 21 Oct 2026 07:28:00 GMT"
    assert retry_after_of(status_error(429, **{"retry-after": date})) is None
    assert retry_after_of(status_error(429, **{"retry-after-ms": "soon"})) is None
