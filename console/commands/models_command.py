from console.app_state import AppState
from .command import Command, requires_key
from google import genai

class ModelsCommand(Command):
    """Lists all available Gemini models and their supported generation methods."""
    
    @requires_key
    def execute(self, state: AppState, args: list[str] = None) -> None:
        client: genai.Client = genai.Client(api_key=state.api_key)
        self._print_output(client=client)
    
    def _print_output(self, client: genai.Client) -> None:
        self._list_models(client)
        print('\n')
        available_models: list[str] = [
            m.name for m in client.models.list()
        ]
        self.list_models_names(available_models)

    @staticmethod
    def list_models_names(available_models: list[str]) -> None:
        print("\nAvailable models you can choose from:")
        for m in available_models:
                print(f" - {m.replace('models/', '')}")


    @staticmethod
    def _list_models(client: genai.Client) -> None:
        print(f"{'Model Name':<40} | {'Supported Actions'}")
        print("-" * 70)
        try:
            for model in client.models.list():
                name: str = model.display_name
                actions: str = ", ".join(model.supported_actions)
                print(f"{name:<40} | {actions}")
        except Exception as e:
            print(f"An error occurred: {e}")