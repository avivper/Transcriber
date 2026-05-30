from console.commands.command import Command
from console.app_state import AppState

class UsageCommand(Command):
    def execute(self, state: AppState, args: list[str]) -> None:
        print(f"Total session usage so far: {state.total_tokens_used} tokens.")
        