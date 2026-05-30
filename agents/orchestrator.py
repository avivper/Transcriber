import os
from functools import wraps
from typing import Any

def language_prompt(func: callable) -> callable:
    @wraps(func)
    def wrapper(self, path: str):
        lang: Any = getattr(self, "language", "en")
        file_name: str = os.path.basename(path)
        
        transcribe_en: str = f"Transcribe the audio file: {file_name}"
        transcribe_he: str = f"תמלל את קובץ השמע: {file_name}"
        
        translate_en: str = f"Translate the data of the file: {file_name}"
        translate_he: str = f"תרגם את תוכן הקובץ: {file_name}"
        
        if func.__name__ == "_transcribe":
            prompt = transcribe_he if lang == "he" else transcribe_en
        else:
            prompt = translate_he if lang == "he" else translate_en
            
        return func(self, path, prompt)
    return wrapper
