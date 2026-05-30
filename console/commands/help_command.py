from console.commands.command import Command
from console.app_state import AppState

class HelpCommand(Command):
    """Prints all available commands with their usage and description."""

    HELP_TEXT: str = """
Available commands:

  load                    Load the Gemini API key from .env into the session
  transcribe <path>       Split a video file and transcribe it to English
  translate <path>        Translate a transcription file from English to Hebrew
  help                    Show this help message
  exit                    Exit the application
"""

    def execute(self, state: AppState, args: list[str]) -> None:
        print(self.HELP_TEXT)
