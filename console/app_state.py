class AppState:
    def __init__(self) -> None:
        """Holds shared application state — the API key lives here."""
        self.api_key: str | None = None
        self.running: bool = False