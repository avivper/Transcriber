from google import genai
import os
from typing import TypeAlias, Tuple
from agents.models.model import Model

File: TypeAlias = genai.types.File
TranscribedData: TypeAlias = Tuple[dict[str, str], int]
class Transcriber:
    AUDIO_PROCESSOR: str = "audio"

    def __init__(self, model: Model) -> None:
        self.model: Model = model
        # self.client = genai.Client(api_key=api_key)
    
    def transcribe_files(self, audio_paths: list[str]) -> TranscribedData:
        result: dict[str, str] = {}
        total_tokens_used: int = 0
        for path in audio_paths:
            data: Tuple[str, int] = self._transcribe(path)
            result[path] = data[0]
            total_tokens_used += data[1]
        return (result, total_tokens_used)
    
    def _transcribe(self, audio_path: str) -> Tuple[str, int]:
        file_name: str = os.path.basename(audio_path)
        audio_file: File = self.model.upload_file_to_model(audio_path, self.AUDIO_PROCESSOR)
        prompt: str = f"Transcribe the audio file: {file_name}"
        return self.model.get_data_from_file(prompt, audio_file)