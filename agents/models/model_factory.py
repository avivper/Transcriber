"""
Factory class for initializing configured Model instances.
"""

from .model import Model

class ModelFactory:
    """
    Centralizes the creation of Gemini Model wrappers with specific configurations.
    """
    def __init__(self, api_key: str, prompt_path: str, model_type: str):
        """
        Initializes the factory with shared parameters.
        
        Args:
            api_key: The API key for Gemini.
            prompt_path: The relative path to the MD prompt file.
            model_type: The Gemini model ID to use.
        """
        self.api_key: str = api_key
        self.prompt_path: str = prompt_path
        self.model_type: str = model_type

    def init_llm_model(self) -> Model:
        """
        Instantiates and returns a configured Model.

        Returns:
            A fully initialized Model instance.

        Raises:
            FileNotFoundError: If the prompt file at prompt_path cannot be found.
        """
        return Model(self.api_key, self.prompt_path, self.model_type)
