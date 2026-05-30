from console.commands.command import Command
from console.app_state import AppState

class ExitCommand(Command):
    """Stops the session loop and exits the application."""
    def execute(self, state: AppState, args: list[str] = None) -> None:
        print("Exiting...")
        state.running = False