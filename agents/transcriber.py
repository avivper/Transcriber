from google import genai
import os
from typing import TypeAlias, Tuple
from agents.models.model import Model
from agents.orchestrator import language_prompt

File: TypeAlias = genai.types.File
TranscribedData: TypeAlias = Tuple[dict[str, str], int]
class Transcriber:
    AUDIO_PROCESSOR: str = "audio"

    def __init__(self, model: Model, language: str = "en") -> None:
        self.model: Model = model
        self.language: str = language

    def transcribe_files(self, audio_paths: list[str]) -> TranscribedData:
        result: dict[str, str] = {}
        total_tokens_used: int = 0
        for path in audio_paths:
            data: Tuple[str, int] = self._transcribe(path)
            result[path] = data[0]
            total_tokens_used += data[1]
        return (result, total_tokens_used)

    @language_prompt
    def _transcribe(self, audio_path: str, prompt: str) -> Tuple[str, int]:
        audio_file: File = self.model.upload_file_to_model(audio_path, self.AUDIO_PROCESSOR)
        return self.model.get_data_from_file(prompt, audio_file)