from console import AppState
from console.commands import Command

class HelpCommand(Command):
    """Prints all available commands with their usage and description."""

    HELP_TEXT: str = """
    Available commands:
    
    load                    Load the Gemini API key from .env into the session
    transcribe <path> [lang] Split a video file and transcribe it (Default: en)
    translate <path> [lang]  Translate a transcription file (Default: he)
    models                  List available Gemini models
    use <model_name>        Switch to a different Gemini model
    help                    Show this help message
    usage                   display the total tokens that used during this current session
    exit                    Exit the application
    
    Supported languages: en (English), he (Hebrew)
  """

    def execute(self, state: AppState, args: list[str] = None) -> None:
        print(self.HELP_TEXT)
