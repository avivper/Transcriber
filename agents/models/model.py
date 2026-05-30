"""
Core wrapper for the Google Gemini Generative AI API.
Provides high-level methods for file uploading, content generation, and error handling.
"""

from google import genai
from google.genai.errors import APIError
from typing import Any, TypeAlias, Tuple
import os 
import time 

# Type aliases for Gemini SDK components
File: TypeAlias = genai.types.File
GenerateContentResponse: TypeAlias = genai.types.GenerateContentResponse
UploadFileConfig : TypeAlias = genai.types.UploadFileConfig
GenerateContentConfig: TypeAlias = genai.types.GenerateContentConfig

class Model:
    """
    Main interface for interacting with Gemini models.
    Handles automated retries for rate limits and abstracts file polling logic.
    """
    MODEL: str = "gemini-3.5-flash" # default model name
    MIME_TYPE: str = "audio/mpeg"
    PROCESSING: str = "PROCESSING"
    SECONDS_TO_SLEEP: int = 2
    AUDIO_PROCESSOR: str = "audio"
    TEXT_PROCESSOR: str = "text"
    RESOURCE_EXHAUSTED: int = 429
    MAX_RETRIES: int = 3

    def __init__(self, api_key: str, prompt_path: str, model_type: str = MODEL) -> None:
        """
        Initializes the Gemini model wrapper.
        
        Args:
            api_key: The Google AI Studio API key.
            prompt_path: Relative path to the system prompt Markdown file.
            model_type: The specific model ID (e.g., 'gemini-1.5-flash').
        """
        self.client: genai.Client = genai.Client(api_key=api_key)
        self.prompt: str = self._load_prompt_path(prompt_path)
        self.model_type = model_type

    @staticmethod
    def load_prompt(path: str) -> str:
        """Loads prompt text from a file."""
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def get_data_from_file(self, prompt: str, file: File) -> Tuple[str, int]: 
        """
        Generates content from an uploaded file and then deletes the file from the API.
        
        Args:
            prompt: The user-level instruction.
            file: The Gemini File object already uploaded.
            
        Returns:
            A tuple of (result_text, tokens_used).
        """
        try:
            content: list[Any] = [file, prompt]
            return self.get_tokens_and_data(content)
        finally:
            self.client.files.delete(name=file.name)
    
    def get_tokens_and_data(self, content: list[Any]) -> Tuple[str, int]:
        """
        Executes a content generation request with automated retry logic for 429 errors.
        
        Args:
            content: List of content items (text, files, etc.).
            
        Returns:
            A tuple of (result_text, tokens_used).
        """
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                response: GenerateContentResponse = self._get_content(content)
                text_result: str = response.text
                tokens_used: int = 0

                if response.usage_metadata:
                    tokens_used = response.usage_metadata.total_token_count
                
                return (text_result, tokens_used)
            except APIError as e:
                if e.code == self.RESOURCE_EXHAUSTED:
                    retries += 1
                    if retries < self.MAX_RETRIES:
                        wait_time = self._get_retry_delay(e)
                        print(f"Rate limit reached (429). Retrying in {wait_time}s... (Attempt {retries}/{self.MAX_RETRIES})")
                        time.sleep(wait_time)
                        continue
                raise e
        return ("", 0)

    def _get_retry_delay(self, e: APIError) -> int:
        """Extracts retry delay from APIError details or defaults to 60s."""
        try:
            import re
            match = re.search(r"retry in ([\d.]+)s", str(e))
            if match:
                return int(float(match.group(1))) + 1
        except Exception:
            pass
        return 60

    def upload_file_to_model(self, path: str, processor_type: str) -> File:
        """
        Uploads a file and waits until its processing state is complete.
        
        Args:
            path: Local path to the file.
            processor_type: Either 'audio' or 'text'.
            
        Returns:
            The processed Gemini File object.
        """
        file: File = self._set_file_type_to_process(path, processor_type)
        while file.state.name == self.PROCESSING:
            time.sleep(self.SECONDS_TO_SLEEP)
            file = self.client.files.get(name=file.name)
        return file
    
    def _set_file_type_to_process(self, path:str, processor_type: str) -> File:
        """Configures and executes the file upload based on processor type."""
        if (processor_type == self.AUDIO_PROCESSOR):
            audio_file: File = self.client.files.upload(
                file=path,
                config=UploadFileConfig(mime_type=self.MIME_TYPE)
            )
            return audio_file
        elif (processor_type == self.TEXT_PROCESSOR):
            text_file: File = self.client.files.upload(
                file=path
            )
            return text_file 
        return None
    
    def _get_content(self, content: list[Any]) -> GenerateContentResponse:
        """Calls the Gemini generate_content API."""
        return self.client.models.generate_content(
            model=self.model_type,
            config=GenerateContentConfig(system_instruction=self.prompt),
            contents=content
            )
    
    def _load_prompt_path(self, prompt_path: str) -> str:
        """Resolves the absolute path for a prompt file and loads its content."""
        path: str = os.path.join(os.path.dirname(__file__), prompt_path)
        return self.load_prompt(path)
