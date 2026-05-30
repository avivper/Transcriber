from console.commands.command import Command
from console.app_state import AppState

class HelpCommand(Command):
    """Prints all available commands with their usage and description."""

    HELP_TEXT: str = """
    Available commands:
    
    load                    Load the Gemini API key from .env into the session
    transcribe <path>       Split a video file and transcribe it to English
    translate <path>        Translate a transcription file from English to Hebrew
    models                  List available Gemini models
    use <model_name>        Switch to a different Gemini model
    help                    Show this help message
    usage                   display the total tokens that used during this current session
    exit                    Exit the application
  """

    def execute(self, state: AppState, args: list[str] = None) -> None:
        print(self.HELP_TEXT)
