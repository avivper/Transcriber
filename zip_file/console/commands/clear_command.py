import os
from console.app_state import AppState
from .command import Command
from ..constants import BANNER

class ClearCommand(Command):
    """Clears the console screen and redisplays the application banner."""

    def execute(self, state: AppState, args: list[str] = None) -> None:
        # Clear terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Redisplay banner and welcome message
        print(BANNER)
        print('Type "help" to see available commands.\n')
