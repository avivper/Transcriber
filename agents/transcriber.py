"""
Agent responsible for converting audio files into verbatim text transcriptions.
Utilizes the Gemini API for high-accuracy speech-to-text processing.
"""

from google import genai
from google.genai.errors import APIError
from typing import TypeAlias
from .models import Model, ProcessorType
from .orchestrator import transcription_prompt

File: TypeAlias = genai.types.File
TranscribedData: TypeAlias = tuple[dict[str, str], int]

class Transcriber:
    """
    Handles the transcription workflow for audio segments.
    
    Attributes:
        model: The underlying Gemini model wrapper.
        language: The target output language for the transcription.
    """

    def __init__(self, model: Model, language: str = "en") -> None:
        """Initializes the Transcriber with a model and target language."""
        self.model: Model = model
        self.language: str = language

    def transcribe_files(self, audio_paths: list[str]) -> TranscribedData:
        """
        Processes a list of audio file paths and returns their transcriptions.
        
        Args:
            audio_paths: List of local paths to the audio chunks.
            
        Returns:
            A tuple containing a mapping of paths to text, and the total token usage.
        """
        try:
            result: dict[str, str] = {}
            total_tokens_used: int = 0
            for path in audio_paths:
                data: tuple[str, int] = self._transcribe(path)
                result[path] = data[0]
                total_tokens_used += data[1]
            return (result, total_tokens_used)
        except (TimeoutError, APIError):
            raise

    @transcription_prompt
    def _transcribe(self, audio_path: str, prompt: str) -> tuple[str, int]:
        """
        Internal method to upload and transcribe a single audio file.
        The 'prompt' argument is automatically injected by the @transcription_prompt decorator.
        """
        try:
            audio_file: File = self.model.upload_file_to_model(audio_path, ProcessorType.AUDIO)
            return self.model.get_data_from_file(prompt, audio_file)
        except (TimeoutError, APIError):
            raise
