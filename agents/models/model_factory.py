from agents.models.model import Model
import os

class ModelFactory:
    """Creates configured Model instances for a given API key and prompt."""
    def __init__(self, api_key: str, prompt_path: str):
        self.api_key: str = api_key
        self.prompt_path: str = prompt_path

    def init_llm_model(self) -> Model:
        """Instantiate and return a Model with the configured API key and prompt path."""
        return Model(self.api_key, self.prompt_path)