from google import genai
from typing import Any, TypeAlias, Tuple
import os 
import time 

File: TypeAlias = genai.types.File
GenerateContentResponse: TypeAlias = genai.types.GenerateContentResponse
UploadFileConfig : TypeAlias = genai.types.UploadFileConfig
GenerateContentConfig: TypeAlias = genai.types.GenerateContentConfig

class Model:
    # TODO: support a various models in the future
    MODEL: str = "gemini-2.5-pro" # "gemini-3.5-flash"
    MIME_TYPE: str = "audio/mpeg"
    PROCESSING: str = "PROCESSING"
    SECONDS_TO_SLEEP: int = 2
    AUDIO_PROCESSOR: str = "audio"
    TEXT_PROCESSOR: str = "text"

    def __init__(self, api_key: str, prompt_path: str) -> None:
        self.client: Model = genai.Client(api_key=api_key)
        self.prompt: str = self._load_prompt_path(prompt_path)

    @staticmethod
    def load_prompt(path: str) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def get_data_from_file(self, prompt: str, file: File) -> Tuple[str, int]: 
        try:
            content: list[Any] = [file, prompt]
            return self.get_tokens_and_data(content)
        finally:
            self.client.files.delete(name=file.name)
    
    def get_tokens_and_data(self, content: list[Any]) -> Tuple[str, int]:
        response: GenerateContentResponse = self._get_content(content)
        text_result: str = response.text
        tokens_used: int = 0

        if response.usage_metadata:
            tokens_used = response.usage_metadata.total_token_count
        
        return (text_result, tokens_used)

    def upload_file_to_model(self, path: str, processor_type: str) -> File:
        file: File = self._set_file_type_to_process(path, processor_type)
        while file.state.name == self.PROCESSING:
            time.sleep(self.SECONDS_TO_SLEEP)
            file = self.client.files.get(name=file.name)
        return file
    
    def _set_file_type_to_process(self, path:str, processor_type: str) -> File:
        if (processor_type == self.AUDIO_PROCESSOR):
            audio_file: File = self.client.files.upload(
                file=path,
                config=UploadFileConfig(mime_type=self.MIME_TYPE)
            )
            return audio_file
        elif (processor_type == self.TEXT_PROCESSOR):
            text_file: File = self.client.files.upload(
                file=path
            )
            return text_file 
        return None
    
    def _get_content(self, content: list[Any]) -> GenerateContentResponse:
        return self.client.models.generate_content(
            model=self.MODEL,
            config=GenerateContentConfig(system_instruction=self.prompt),
            contents=content
            )
    
    def _load_prompt_path(self, prompt_path: str) -> str:
        path: str = os.path.join(os.path.dirname(__file__), prompt_path)
        return self.load_prompt(path)