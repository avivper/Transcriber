from google import genai
import os
from typing import TypeAlias
from agents.models.model import Model

File: TypeAlias = genai.types.File

class Transcriber:
    AUDIO_PROCESSOR: str = "audio"

    def __init__(self, model: Model) -> None:
        self.model: Model = model
        # self.client = genai.Client(api_key=api_key)

    def transcribe(self, audio_path: str) -> str:
        file_name: str = os.path.basename(audio_path)
        audio_file: File = self.model.upload_file_to_model(audio_path, self.AUDIO_PROCESSOR)
        prompt: str = f"Transcribe the audio file: {file_name}"
        return self.model.get_data_from_file(prompt, audio_file)
    
    def transcribe_files(self, audio_paths: list[str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for path in audio_paths:
            result[path] = self.transcribe(path)
        return result
