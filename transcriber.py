from google import genai
from google.genai import types
import os
import time
from typing import Any


class Transcriber:
    # TODO: support a various models in the future
    MODEL: str = "gemini-3.5-flash"
    MIME_TYPE: str = "audio/mpeg"
    PROCESSING: str = "PROCESSING"
    SECONDS_TO_SLEEP: int = 2

    def __init__(self, api_key: str, prompt_path: str = None) -> None:
        self.client = genai.Client(api_key=api_key)
        self.prompt: str = self._determine_prompt(prompt_path)

    def transcribe(self, audio_path: str) -> str:
        file_name: str = os.path.basename(audio_path)
        audio_file: types.File = self._upload_audio(audio_path)
        return self._transcribe_audio_file(file_name, audio_file)
    
    # Maps filename -> Transcribtion
    def transcribe_many(self, audio_paths: list[str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for path in audio_paths:
            result[path] = self.transcribe(path)
        return result

    def _load_prompt(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def _upload_audio(self, audio_path: str) -> types.File:
        audio_file: types.File = self.client.files.upload(
            file=audio_path,
            config=types.UploadFileConfig(mime_type=self.MIME_TYPE)
            )
        while audio_file.state.name == self.PROCESSING:
            time.sleep(self.SECONDS_TO_SLEEP)
            audio_file = self.client.files.get(name=audio_file.name)
        return audio_file

    def _transcribe_audio_file(
            self, file_name: str, audio_file: types.File
            ) -> str:
        try:
            prompt: str = f"Transcribe the audio file: {file_name}"
            content: list[Any] = [audio_file, prompt]
            response: types.GenerateContentResponse = self._get_content(content)
            return response.text
        finally:
            self.client.files.delete(name=audio_file.name)

    def _determine_prompt(self, prompt_path: str) -> str:
        path: str = "prompts/transcription_agent.md"
        if (prompt_path is None):
            return os.path.join(os.path.dirname(__file__), path)
        return self._load_prompt(prompt_path)

    def _get_content(self, content: list[Any]) -> types.GenerateContentResponse:
        return self.client.models.generate_content(
            model=self.MODEL,
            config=types.GenerateContentConfig(system_instruction=self.prompt),
            contents=content
            )

