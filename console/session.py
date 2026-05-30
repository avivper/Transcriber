"""
Initializes and manages the interactive Transcriber REPL session.
"""

from .app_state import AppState
from .exceptions import CommandError
from .commands import Command
from .commands.command_factory import CommandFactory
from .constants import BANNER


class Session:
    """
    Interactive REPL that reads commands from stdin and dispatches them to registered handlers.
    
    Attributes:
        COMMAND_ENTRY: The prompt string displayed to the user.
        state: The shared application state container.
        running: Internal loop control flag.
        commands: Mapping of command strings to Command objects.
    """
    COMMAND_ENTRY: str = ">>> "

    def __init__(self) -> None:
        """Initializes the session, state, and command registry."""
        self.state = AppState()
        self.running: bool = False
        self.commands: dict[str, Command] = CommandFactory.get_commands()
    
    def run(self) -> None:
        """
        Starts the main interactive loop.
        Handles global interrupts (Ctrl+C) and EOF (Ctrl+D) gracefully.
        """
        self._init_launch()
        while self.state.running:
            try:
                raw: str = input(self.COMMAND_ENTRY).strip()
                if not raw:
                    continue
                self._execute_commands(raw)
            except KeyboardInterrupt:
                print("\n[Interrupt] Operation cancelled. Type 'exit' to quit.")
                continue
            except EOFError:
                print("\nExiting...")
                self.state.running = False

    def _init_launch(self) -> None:
        """Sets launch flags and displays the application branding."""
        self.state.running = True
        print(BANNER)
        print('Type "help" to see available commands.\n')

    def _execute_commands(self, raw: str) -> None:
        """Parses user input into command names and arguments."""
        parts: list[str] = raw.split()
        name: str = parts[0]
        args: list[str] = parts[1:]
        command: Command | None = self.commands.get(name)

        if command is None:
            print(f"Unknown command: {name}")
            return
        
        self._execute(command, args)
    
    def _execute(self, command: Command, args: list[str]) -> None:
        """
        Orchestrates the safe execution of a single command.
        Catches and reports CommandErrors and unexpected system failures.
        """
        try: 
            command.execute(self.state, args)
        except CommandError as e:
            # Catch known user/validation errors gracefully
            print(f"Command Error: {e}")
        except Exception as e:
            # Catch unexpected fatal crashes (like network failures or deep bugs)
            print(f"An unexpected system error occurred: {e}")
