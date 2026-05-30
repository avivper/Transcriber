from console.app_state import AppState
from .command import Command

class HelpCommand(Command):
    """Prints all available commands with their usage and description."""

    HELP_TEXT: str = """
    Available commands:
    
    load                    Load the Gemini API key from .env into the session
    transcribe <path> [lang] Split a video file and transcribe it (Default: en)
    translate <path> [lang]  Translate a transcription file (Default: he)
    models                  List available Gemini models
    use <model_name>        Switch to a different Gemini model
    current                 Show the currently active Gemini model
    help                    Show this help message
    clear                   Clear the console screen
    usage                   Display the total tokens used during the current session
    exit                    Exit the application
    
    Supported languages: en (English), he (Hebrew)
  """

    def execute(self, state: AppState, args: list[str] = None) -> None:
        """
        Prints the help text containing all available commands and their usage.
        
        Args:
            state: The shared AppState container.
            args: Optional command arguments (ignored).
        """
        print(self.HELP_TEXT)
