import os
from google import genai
from agents.models.model import Model
from typing import TypeAlias

File: TypeAlias = genai.types.File

class Translator:
    TEXT_PROCESSOR: str = "text"

    def __init__(self, model: Model) -> None:
        self.model: Model = model

    def translate_from_file(self, text_path: str) -> str:
        file_name: str = os.path.basename(text_path)
        text_file: File = self.model.upload_file_to_model(text_path, self.TEXT_PROCESSOR)
        prompt: str = f"Translate the data of the file: {file_name}"
        return self.model.get_data_from_file(prompt, text_file)
    
