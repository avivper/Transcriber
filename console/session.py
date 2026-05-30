from console.app_state import AppState
from console.commands.command import Command
from console.commands.load_command import LoadCommand
from console.commands.transcribe_command import TranscribeCommand
from console.commands.exit_command import ExitCommand
from console.commands.translate_command import TranslateCommand

class Session:
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
            "translate": TranslateCommand()
        }
    
    def run(self) -> None:
        print(self.BANNER)
        self.state.running = True
        while self.state.running:
            raw: str = input(self.COMMAND_ENTRY).strip()
            if not raw:
                continue
            self._execute_commands(raw)
    
    def _execute_commands(self, raw: str) -> None:
        parts: list[str] = raw.split()
        name: str = parts[0]
        args: list[str] = parts[1:]
        command: Command | None = self.commands.get(name)
        if command is None:
            print(f"Unkown command: {name}")
        else:
            command.execute(self.state, args)