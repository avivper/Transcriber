from console.commands.command import Command
from console.app_state import AppState
from config import Config

class LoadCommand(Command):
    """Loads the Gemini API key from the environment into session state."""
    def execute(self, state: AppState, args: list[str]) -> None:
        state.api_key = self._load_key()
        print("API Key loaded successfully!")
    
    @staticmethod
    def _load_key() -> str:
        try:
            config: str = Config.load()
            return config.api_key
        except ValueError as e:
            print(f"Error: {e}")