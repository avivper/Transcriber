from console.commands.command import Command
from console.commands.load_command import LoadCommand
from console.commands.transcribe_command import TranscribeCommand
from console.commands.exit_command import ExitCommand
from console.commands.translate_command import TranslateCommand
from console.commands.help_command import HelpCommand
from console.commands.usage_command import UsageCommand
from console.commands.models_command import ModelsCommand
from console.commands.use_command import UseCommand

class CommandFactory:
    """Central factory to manage and initialize all available commands."""
    
    @staticmethod
    def get_commands() -> dict[str, Command]:
        """Returns a dictionary mapping command names to their handler instances."""
        return {
            "exit": ExitCommand(),
            "load": LoadCommand(),
            "transcribe": TranscribeCommand(),
            "translate": TranslateCommand(),
            "help": HelpCommand(),
            "usage": UsageCommand(),
            "models": ModelsCommand(),
            "use": UseCommand()
        }
