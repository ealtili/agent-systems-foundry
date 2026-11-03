"""SDK error classification. You implement it; tests/test_classify.py is the contract."""

from src.retry import RetryableError


def classify_sdk_error(err: BaseException) -> RetryableError | None:
    """Decide whether an Anthropic SDK exception deserves another attempt.

    - APITimeoutError and APIConnectionError: retryable, retry_after None.
    - APIStatusError with status 408, 409, 429 or >= 500: retryable. retry_after comes from the
      `retry-after-ms` header (milliseconds / 1000) if present and numeric, else from `retry-after`
      parsed as a number of seconds. An HTTP-date or garbage value counts as absent.
    - Any other APIStatusError (400, 401, 403, 404, 422, ...) and any other exception: None.
    The returned RetryableError's message mentions the exception type name.
    """
    raise NotImplementedError
