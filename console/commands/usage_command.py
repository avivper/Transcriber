from console.app_state import AppState
from .command import Command

class UsageCommand(Command):
    def execute(self, state: AppState, args: list[str] = None) -> None:
        print(f"Total session usage so far: {state.total_tokens_used} tokens.")
        
        state.check_rate_limit()
        if state.is_rate_limited:
            wait_time = state.get_remaining_wait_time()
            print(f"API Quota/Rate Limit reached. Please wait {wait_time} seconds before next request.")
        else:
            print("API Status: Ready")
        