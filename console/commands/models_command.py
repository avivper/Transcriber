"""
Command for listing all available Google Gemini models and their capabilities.
Provides a real-time view of model names and supported generation methods.
"""

from console.app_state import AppState
from .command import Command, requires_key
from google import genai

class ModelsCommand(Command):
    """
    Handles the 'models' CLI command.
    Retrieves and displays a formatted table of all Gemini models accessible with the current API key.
    """
    
    @requires_key
    def execute(self, state: AppState, args: list[str] = None) -> None:
        """
        Executes the model listing workflow.
        
        Args:
            state: The shared AppState container.
            args: Optional command arguments (ignored).
        """
        client: genai.Client = genai.Client(api_key=state.api_key)
        self._print_output(client=client)
    
    def _print_output(self, client: genai.Client) -> None:
        """
        Orchestrates the retrieval and printing of model data.
        
        Args:
            client: The initialized Gemini API client.
        """
        self._list_models(client)
        print('\n')
        available_models: list[str] = [
            m.name for m in client.models.list()
        ]
        self.list_models_names(available_models)

    @staticmethod
    def list_models_names(available_models: list[str]) -> None:
        """
        Prints a simplified bulleted list of available model short-names.
        
        Args:
            available_models: A list of full model resource names.
        """
        print("\nAvailable models you can choose from:")
        for m in available_models:
                print(f" - {m.replace('models/', '')}")

    @staticmethod
    def _list_models(client: genai.Client) -> None:
        """
        Prints a formatted table showing detailed model metadata.
        
        Args:
            client: The initialized Gemini API client.
        """
        print(f"{'Model Name':<40} | {'Supported Actions'}")
        print("-" * 70)
        try:
            for model in client.models.list():
                name: str = model.name
                actions: str = ", ".join(model.supported_generation_methods)
                print(f"{name:<40} | {actions}")
        except Exception as e:
            print(f"An error occurred: {e}")
