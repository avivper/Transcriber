"""
Middleware and orchestration logic for agent communication.
Contains decorators for dynamic prompt injection and language handling.
"""

import os
from functools import wraps
from typing import Any, Callable


def inject_prompt(template_en: str, template_he: str) -> Callable:
    """
    Decorator factory that generates a language-aware prompt injector.
    """
    def decorator(func: Callable) -> Callable:
        """Wraps the target method to inject a language-specific prompt."""
        @wraps(func)
        def wrapper(self, path: str, *args, **kwargs) -> Callable:
            """Resolves the prompt from the file name and instance language, then delegates to the wrapped method."""
            lang: Any = getattr(self, "language", "en")
            file_name: str = os.path.basename(path)

            template: str = template_he if lang == "he" else template_en
            prompt: str = template.format(file_name=file_name)

            return func(self, path, prompt, *args, **kwargs)
        return wrapper
    return decorator


transcription_prompt: Callable = inject_prompt(
    template_en="Transcribe the audio file: {file_name}",
    template_he="תמלל את קובץ השמע: {file_name}"
)

translation_prompt: Callable = inject_prompt(
    template_en="Translate the data of the file: {file_name}",
    template_he="תרגם את תוכן הקובץ: {file_name}"
)