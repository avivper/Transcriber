"""
Agent responsible for translating transcription text between supported languages.
Leverages the Gemini API to maintain natural phrasing and preserve formatting.
"""

import os
from google import genai
from .models import Model
from typing import TypeAlias, Tuple
from .orchestrator import language_prompt

File: TypeAlias = genai.types.File
TranslatedData: TypeAlias = Tuple[str, int]

class Translator:
    """
    Handles the translation of text documents using LLM agents.
    
    Attributes:
        TEXT_PROCESSOR: The processor type identifier for text files.
        model: The underlying Gemini model wrapper.
        language: The target output language for the translation.
    """
    TEXT_PROCESSOR: str = "text"

    def __init__(self, model: Model, language: str = "he") -> None:
        """Initializes the Translator with a model and target language."""
        self.model: Model = model
        self.language: str = language

    @language_prompt
    def translate_from_file(self, text_path: str, prompt: str) -> TranslatedData:
        """
        Translates the content of a local text file.
        The 'prompt' argument is automatically injected by the @language_prompt decorator.
        
        Args:
            text_path: Path to the source text file.
            
        Returns:
            A tuple containing the translated text and token usage.
        """
        text_file: File = self.model.upload_file_to_model(text_path, self.TEXT_PROCESSOR)
        return self.model.get_data_from_file(prompt, text_file)
