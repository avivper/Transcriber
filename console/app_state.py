import time

class AppState:

    DEFAULT_MODEL: str = "gemini-3.5-flash"

    def __init__(self) -> None:
        """Holds shared application state — the API key lives here."""
        self.api_key: str | None = None
        self.current_model: str = self.DEFAULT_MODEL
        self.running: bool = False
        self.total_tokens_used: int = 0
        self.retry_after: float = 0.0 
        self.is_rate_limited: bool = False

    def check_rate_limit(self) -> None:
        """Check if we are still within the rate limit wait period."""
        if self.is_rate_limited:
            remaining: float = self.retry_after - time.time()
            if remaining <= 0:
                self.is_rate_limited = False
                self.retry_after = 0.0

    def get_remaining_wait_time(self) -> int:
        """Return remaining wait time in seconds."""
        if not self.is_rate_limited:
            return 0
        return max(0, int(self.retry_after - time.time()))