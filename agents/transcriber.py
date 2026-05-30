from google import genai
import os
from typing import  TypeAlias
from agents.model import Model

File: TypeAlias = genai.types.File

class Transcriber:
    AUDIO_PROCESSOR: str = "audio"
    PROMPT_PATH: str = "prompts/transcription_agent.md"

    def __init__(self, api_key: str, prompt_path: str = None) -> None:
        prompt: str = self._determine_prompt(prompt_path)
        self.model: Model = Model(api_key=api_key, prompt_path=prompt)
        # self.client = genai.Client(api_key=api_key)

    def transcribe(self, audio_path: str) -> str:
        file_name: str = os.path.basename(audio_path)
        audio_file: File = self.model.upload_file_to_model(audio_path, self.AUDIO_PROCESSOR)
        prompt: str = f"Transcribe the audio file: {file_name}"
        return self.model.get_data_from_file(prompt, audio_file)
    
    # Maps filename -> Transcribtion
    def transcribe_files(self, audio_paths: list[str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for path in audio_paths:
            result[path] = self.transcribe(path)
        return result

    def _determine_prompt(self, prompt_path: str) -> str:
        if prompt_path is None:
            return os.path.join(os.path.dirname(__file__), self.PROMPT_PATH)
        return prompt_path

