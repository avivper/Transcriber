from console.commands import (
    Command, LoadCommand, TranscribeCommand, ExitCommand, 
    TranslateCommand, HelpCommand, UsageCommand, ModelsCommand, UseCommand
)

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
