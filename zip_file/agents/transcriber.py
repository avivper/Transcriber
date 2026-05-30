"""
Agent responsible for converting audio files into verbatim text transcriptions.
Utilizes the Gemini API for high-accuracy speech-to-text processing.
"""

from google import genai
import os
from typing import TypeAlias, Tuple
from .models import Model
from .orchestrator import language_prompt

File: TypeAlias = genai.types.File
TranscribedData: TypeAlias = Tuple[dict[str, str], int]

class Transcriber:
    """
    Handles the transcription workflow for audio segments.
    
    Attributes:
        AUDIO_PROCESSOR: The processor type identifier for audio files.
        model: The underlying Gemini model wrapper.
        language: The target output language for the transcription.
    """
    AUDIO_PROCESSOR: str = "audio"

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
        result: dict[str, str] = {}
        total_tokens_used: int = 0
        for path in audio_paths:
            data: Tuple[str, int] = self._transcribe(path)
            result[path] = data[0]
            total_tokens_used += data[1]
        return (result, total_tokens_used)

    @language_prompt
    def _transcribe(self, audio_path: str, prompt: str) -> Tuple[str, int]:
        """
        Internal method to upload and transcribe a single audio file.
        The 'prompt' argument is automatically injected by the @language_prompt decorator.
        """
        audio_file: File = self.model.upload_file_to_model(audio_path, self.AUDIO_PROCESSOR)
        return self.model.get_data_from_file(prompt, audio_file)
