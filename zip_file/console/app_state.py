"""
Shared state management for the Transcriber console application.
Maintains session-wide variables like API keys, token usage, and rate limit status.
"""

import time

class AppState:
    """
    State container for the current interactive session.
    
    Attributes:
        DEFAULT_MODEL: The fallback Gemini model ID.
        api_key: The user's Google Gemini API key.
        current_model: The currently selected Gemini model.
        running: Boolean flag for the REPL loop.
        total_tokens_used: Cumulative token count for the session.
        retry_after: Unix timestamp indicating when rate limits expire.
        is_rate_limited: Boolean flag for active 429 lockout.
    """

    DEFAULT_MODEL: str = "gemini-3.5-flash"

    def __init__(self) -> None:
        """Initializes the application state with default values."""
        self.api_key: str | None = None
        self.current_model: str = self.DEFAULT_MODEL
        self.running: bool = False
        self.total_tokens_used: int = 0
        self.retry_after: float = 0.0 
        self.is_rate_limited: bool = False

    def check_rate_limit(self) -> None:
        """
        Updates the rate limit status based on the current time.
        Resets flags if the wait period has elapsed.
        """
        if self.is_rate_limited:
            remaining: float = self.retry_after - time.time()
            if remaining <= 0:
                self.is_rate_limited = False
                self.retry_after = 0.0

    def get_remaining_wait_time(self) -> int:
        """
        Calculates the remaining seconds until the rate limit expires.
        
        Returns:
            The number of seconds to wait (0 if not limited).
        """
        if not self.is_rate_limited:
            return 0
        return max(0, int(self.retry_after - time.time()))
