from console.app_state import AppState
from console.commands.command import Command
from console.commands.load_command import LoadCommand
from console.commands.transcribe_command import TranscribeCommand
from console.commands.exit_command import ExitCommand
from console.commands.translate_command import TranslateCommand
from console.commands.help_command import HelpCommand
from console.commands.usage_command import UsageCommand
from console.exceptions import CommandError

class Session:
    """Interactive REPL that reads commands from stdin and dispatches them to registered Command handlers."""
    COMMAND_ENTRY: str = ">>> "
    BANNER: str = r"""
+--------------------------------------------------------------+
|                                                              |
|  _____                              _ _                      |
| |_   _| __ __ _ _ __  ___  ___ _ __(_) |__   ___ _ __        |
|   | || '__/ _` | '_ \/ __|/ __| '__| | '_ \ / _ \ '__|       |
|   | || | | (_| | | | \__ \ (__| |  | | |_) |  __/ |          |
|   |_||_|  \__,_|_| |_|___/\___|_|  |_|_.__/ \___|_|          |
|                                                              |
+--------------------------------------------------------------+"""

    def __init__(self) -> None:
        self.state = AppState()
        self.running: bool = False
        self.commands: dict[str, Command] = {
            "exit": ExitCommand(),
            "load" : LoadCommand(),
            "transcribe": TranscribeCommand(),
            "translate": TranslateCommand(),
            "help": HelpCommand(),
            "usage": UsageCommand()
        }
    
    def run(self) -> None:
        """Print the banner and start the command loop until exit is called."""
        self._init_launch()
        while self.state.running:
            raw: str = input(self.COMMAND_ENTRY).strip()
            if not raw:
                continue
            self._execute_commands(raw)

    def _init_launch(self) -> None:
        self.state.running = True
        print(self.BANNER)
        print('Type "help" to see available commands.\n')

    def _execute_commands(self, raw: str) -> None:
        parts: list[str] = raw.split()
        name: str = parts[0]
        args: list[str] = parts[1:]
        command: Command | None = self.commands.get(name)

        if command is None:
            print(f"Unkown command: {name}")
            return
        
        self._execute(command, args)
    
    def _execute(self, command: Command, args: list[str]) -> None:
        try: 
            command.execute(self.state, args)
        except CommandError as e:
            # Catch known user/validation errors gracefully
            print(f"Command Error: {e}")
        except Exception as e:
            # Catch unexpected fatal crashes (like network failures or deep bugs)
            print(f"An unexpected system error occurred: {e}")