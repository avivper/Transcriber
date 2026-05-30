import os
from google import genai
from agents.model import Model
from typing import TypeAlias

File: TypeAlias = genai.types.File

class Translator:
    TEXT_PROCESSOR: str = "text"
    PROMPT_PATH: str = "prompts/translation_agent.md"

    def __init__(self, api_key: str, prompt_path: str = None) -> None:
        prompt: str = self._determine_prompt(prompt_path)
        self.model: Model = Model(api_key=api_key, prompt_path=prompt)

    def translate_from_file(self, text_path: str) -> str:
        file_name: str = os.path.basename(text_path)
        text_file: File = self.model.upload_file_to_model(text_path, self.TEXT_PROCESSOR)
        prompt: str = f"Translate the data of the file: {file_name}"
        return self.model.get_data_from_file(prompt, text_file)
    
    def translate_files(self, text_paths: list[str]) -> list[str]:
        result: list[str] = []
        for file in text_paths:
            result.append(self.translate_from_file(file))
        return result
    
    def translate_from_dict(self, transcribed_data: dict[str, str]) -> list[str]:
        result: list[str] = []
        for file_name, data_to_translate in transcribed_data.items():
            prompt: str = f"Translate the data of the file: {file_name}"
            content_to_llm: list[str] = [prompt, data_to_translate]
            result.append(self.model.get_data(content_to_llm))
        return result
    
    def _determine_prompt(self, prompt_path: str) -> str:
        if prompt_path is None:
            return os.path.join(os.path.dirname(__file__), self.PROMPT_PATH)
        return prompt_path
    
    @staticmethod 
    def _get_data_to_translate(data: dict[str, str]) -> list[str]: 
        data_to_translate: list[str] = []
        for text_file in data:
            data_to_translate.append(data[text_file])
        return data_to_translate