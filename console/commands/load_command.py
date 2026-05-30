"""
Command for loading the Google Gemini API key into the application session.
Interacts with the Config utility to retrieve and validate environment variables.
"""

from console.app_state import AppState
from .command import Command
from config import Config

class LoadCommand(Command):
    """
    Handles the 'load' CLI command workflow.
    Responsible for populating the global AppState with the required API credentials.
    """
    def execute(self, state: AppState, args: list[str]) -> None:
        """
        Executes the key loading process.
        
        Args:
            state: The shared AppState container.
            args: Command arguments (ignored).
        """
        state.api_key = self._load_key()
        if state.api_key:
            print("API Key loaded successfully!")
    
    @staticmethod
    def _load_key() -> str:
        """
        Loads the API key from the environment via the Config utility.
        
        Returns:
            The API key string if successful, otherwise None.
        """
        try:
            config = Config.load()
            return config.api_key
        except ValueError as e:
            print(f"Error: {e}")
            return None
