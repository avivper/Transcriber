from agents.models.model import Model
import os

class ModelFactory:
    def __init__(self, api_key: str, prompt_path: str):
        self.api_key: str = api_key
        self.prompt_path: str = prompt_path

    def init_llm_model(self) -> Model:
        return Model(self.api_key, self.prompt_path)