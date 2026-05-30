import os
from google import genai
from agents.models import Model
from typing import TypeAlias, Tuple
from .orchestrator import language_prompt

File: TypeAlias = genai.types.File
TranslatedData: TypeAlias = Tuple[str, int]
class Translator:
    TEXT_PROCESSOR: str = "text"

    def __init__(self, model: Model, language: str = "he") -> None:
        self.model: Model = model
        self.language: str = language

    @language_prompt
    def translate_from_file(self, text_path: str, prompt: str) -> TranslatedData:
        text_file: File = self.model.upload_file_to_model(text_path, self.TEXT_PROCESSOR)
        return self.model.get_data_from_file(prompt, text_file)
    
