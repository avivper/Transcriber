from console.commands.command import Command, requires_key
from console.app_state import AppState
from console.commands.models_command import ModelsCommand
from google import genai

class UseCommand(Command):
    """Command to switch the currently active Gemini model with validation."""

    DEFAULT: str = "default"

    @requires_key
    def execute(self, state: AppState, args: list[str]) -> None:
        if not args:
            print(f"Current model: {state.current_model}")
            print("Usage: use <model_name>")
            return

        requested_model: str = args[0]

        if not self._handle_default(state , requested_model):
            self._fetch_valid_models(requested_model, state)

    def _handle_default(self, state: AppState, requested_model: str) -> bool:
        if requested_model.lower() == self.DEFAULT:
            state.current_model = state.DEFAULT_MODEL
            print(f"Switched to default model: {state.DEFAULT_MODEL}")
            return True 
        return False
    
    def _fetch_valid_models(self, requested_model: str, state: AppState) -> None:
        client: genai.Client = genai.Client(api_key=state.api_key)
        try:
            available_models: list[str] = [
                m.name for m in client.models.list()
                ]
            switch_succeeded: bool = self._implement_input(
                 requested_model, available_models, state
                 )
            if not switch_succeeded:
                self._display_error_message(available_models, requested_model)
        except Exception as e:
            print(f"Could not validate model name: {e}")

    @staticmethod
    def _implement_input(requested_model: str, available_models: list[str], state: AppState) -> bool:
        if requested_model in available_models:
                state.current_model = requested_model
                print(f"Switched to model: {requested_model}")
                return True
        prefixed_name: str = f"models/{requested_model}"
        if prefixed_name in available_models:
                state.current_model = prefixed_name
                print(f"Switched to model: {prefixed_name}")
                return True
        return False
    
    @staticmethod
    def _display_error_message(available_models: list[str], requested_model: str) -> None:
        print(f"Error: '{requested_model}' is not a valid Gemini model.")
        ModelsCommand.list_models_names(available_models)
        print("\nYou can use either the full name or the short name shown above.")