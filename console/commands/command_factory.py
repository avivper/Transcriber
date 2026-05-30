"""
Central registry and initializer for all console commands.
"""

from .command import Command
from .load_command import LoadCommand
from .transcribe_command import TranscribeCommand
from .exit_command import ExitCommand
from .translate_command import TranslateCommand
from .help_command import HelpCommand
from .usage_command import UsageCommand
from .models_command import ModelsCommand
from .use_command import UseCommand
from .clear_command import ClearCommand
from .current_command import CurrentCommand

class CommandFactory:
    """
    Central factory to manage and initialize all available commands.
    Keeps the main Session decoupled from specific command implementations.
    """
    
    @staticmethod
    def get_commands() -> dict[str, Command]:
        """
        Returns a dictionary mapping command names to their handler instances.
        
        Returns:
            A dict of command_name -> Command instance.
        """
        return {
            "exit": ExitCommand(),
            "load": LoadCommand(),
            "transcribe": TranscribeCommand(),
            "translate": TranslateCommand(),
            "help": HelpCommand(),
            "usage": UsageCommand(),
            "models": ModelsCommand(),
            "use": UseCommand(),
            "clear": ClearCommand(),
            "current": CurrentCommand()
        }
