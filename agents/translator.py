"""
Agent responsible for translating transcription text between supported languages.
Leverages the Gemini API to maintain natural phrasing and preserve formatting.
"""

from google import genai
from google.genai.errors import APIError
from .models import Model, ProcessorType
from typing import TypeAlias
from .orchestrator import translation_prompt

File: TypeAlias = genai.types.File
TranslatedData: TypeAlias = tuple[str, int]

class Translator:
    """
    Handles the translation of text documents using LLM agents.
    
    Attributes:
        model: The underlying Gemini model wrapper.
        language: The target output language for the translation.
    """

    def __init__(self, model: Model, language: str = "he") -> None:
        """Initializes the Translator with a model and target language."""
        self.model: Model = model
        self.language: str = language

    @translation_prompt
    def translate_from_file(self, text_path: str, prompt: str) -> TranslatedData:
        """
        Translates the content of a local text file.
        The 'prompt' argument is automatically injected by the @translation_prompt decorator.
        
        Args:
            text_path: Path to the source text file.
            
        Returns:
            A tuple containing the translated text and token usage.
        """
        try:
            text_file: File = self.model.upload_file_to_model(text_path, ProcessorType.TEXT)
            return self.model.get_data_from_file(prompt, text_file)
        except (TimeoutError, APIError):
            raise
