"""
Configuration management for the Transcriber application.
Handles environment variable loading and validation.
"""

import os 
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Config:
    """
    Immutable application configuration loaded from environment variables.
    
    Attributes:
        api_key: The Google Gemini API key required for all LLM operations.
    """

    api_key: str

    @classmethod
    def load(cls) -> "Config":
        """
        Loads configuration from the .env file or system environment.
        
        Returns:
            An initialized Config instance.
            
        Raises:
            ValueError: If GEMINI_API_KEY is not found.
        """
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment or .env file"
                )
        
        return cls(api_key=api_key)
