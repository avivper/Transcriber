import os 
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Config:
    """Immutable application configuration loaded from environment variables."""

    api_key: str

    @classmethod
    def load(cls) -> "Config":
        """Load config from .env or environment. Raises ValueError if GEMINI_API_KEY is missing."""
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment or .env file"
                )
        
        return cls(api_key=api_key)
    
