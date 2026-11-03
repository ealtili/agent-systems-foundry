"""Test support. Given code."""


class FakeClock:
    """A clock you advance by hand; also usable as an async `sleep` that advances itself."""

    def __init__(self, now: float = 0.0) -> None:
        self.now = now
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.now

    async def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds
