from console.commands.command import Command
from console.app_state import AppState

class ExitCommand(Command):
    def execute(self, state: AppState, args: list[str]) -> None:
        print("Exiting...")
        state.running = False