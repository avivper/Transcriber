"""
Command for translating existing transcription files using Gemini.
Supports target language validation and automated output organization.
"""

from console.app_state import AppState
from utils import TextWriter, TextProcessor, CommandError, FactoryError
from .command import Command, requires_key
from agents import Translator, TranslatedData, AgentFactory, AgentType
from agents.models import Model, ModelFactory
from google.genai.errors import APIError
import os
import time
import re

class TranslateCommand(Command):
    """
    Handles the 'translate' CLI command workflow.
    """
    OUTPUT_DIR: str = "output"
    RESOURCE_EXHAUSTED: int = 429
    WAIT_TIME: int = 60

    @requires_key
    def execute(self, state: AppState, args: list[str] = None) -> None:
        """
        Executes the translation process.
        
        Args:
            state: Global application state.
            args: Command arguments [input_path, optional_lang].
        """
        try:
            self._rate_limit_checks(state)
            user_input: tuple[str, str] = self._get_args(args)
            input_path: str = user_input[0]
            lang_code: str = user_input[1]

            self._validate_language_switch(input_path, lang_code)

            self._check_path(input_path)
            prompt_path: str = f"prompts/translation_{lang_code}.md"
            self._create_translated_output(input_path, state, lang_code, prompt_path)
            print(
                f"Processed chunk. Total session usage so far: {state.total_tokens_used} tokens."
                )

        except APIError as e:
            if e.code == self.RESOURCE_EXHAUSTED:
                self._handle_rate_limit(state, e)
                raise CommandError(f"API Quota exceeded. {e.message}")
            raise
        except (
            CommandError, FactoryError, TimeoutError, FileNotFoundError
            ):
            raise

    def _handle_rate_limit(self, state: AppState, e: APIError) -> None:
        """Updates state with rate limit info and calculates wait time."""
        state.is_rate_limited = True
        match = re.search(r"retry in ([\d.]+)s", str(e))
        wait_time: int = self.WAIT_TIME
        if match:
            wait_time = int(float(match.group(1))) + 1
        state.retry_after = time.time() + wait_time
        print(f"Rate limit hit. Application will wait for {wait_time}s.")

    def _create_translated_output(
            self, input_path: str, state: AppState, 
            lang_code: str, prompt_path: str
            ) -> None:
        """Orchestrates the translation and file writing workflow."""
        try:
            translated_data: list[str] = self._translate_data(
                input_path, state, lang_code, prompt_path
                )
            self._write_output_data(translated_data, input_path, lang_code)
        except TimeoutError:
            raise
        except FactoryError:
            raise

    def _translate_data(
            self, input_path: str, state: AppState, 
            lang_code: str, prompt_path: str
            ) -> list[str]:
        """Initializes the agent and translates the source file."""
        try:
            translator: Translator = self._init_translator_agent(state, lang_code, prompt_path)
            target_lang: str = "English" if lang_code == "en" else "Hebrew"
            print(f"\n[Process] Starting translation of content into {target_lang}...")
            
            translated_data: TranslatedData = translator.translate_from_file(input_path)
            translated_text: str = translated_data[0]
            tokens_used: int = translated_data[1]
            state.total_tokens_used += tokens_used
            return [translated_text]
       
        except TimeoutError:
            raise
        except FactoryError:
            raise

    def _write_output_data(self, data: list[str], input_path: str, lang_code: str) -> None:
        """Persists translated text into language-specific subfolders."""
        folder_name: str = "English" if lang_code == "en" else "Hebrew"
        target_dir: str = os.path.join(self.OUTPUT_DIR, folder_name)
        text_writer: TextWriter = TextWriter(target_dir)
        file_name: str = self._get_file_name(input_path, lang_code)
        processed: list[str] = TextProcessor(data).process()
        output_file_path: str = text_writer.write_list(processed, file_name)
        print(f"Created the output at {output_file_path}")

    @staticmethod
    def _validate_language_switch(input_path: str, lang_code: str) -> None:
        """
        Prevents redundant same-language translations based on file suffix.

        Raises:
            CommandError: If the input filename suffix already matches the target language.
        """
        filename: str = input_path.lower()
        if lang_code == "he" and any(s in filename for s in ["_heb", "_he"]):
            raise CommandError("Redundant action: The input file is already in Hebrew.")
        if lang_code == "en" and any(s in filename for s in ["_eng", "_en"]):
            raise CommandError("Redundant action: The input file is already in English.")

    @staticmethod
    def _init_translator_agent(state: AppState, lang_code: str, prompt_path: str) -> Translator:
        """Initializes a language-aware Translator agent."""
        model: Model = ModelFactory(state.api_key, prompt_path, state.current_model).init_llm_model()
        agent_factory: AgentFactory = AgentFactory()
        try:
            return agent_factory.init_agent(model, AgentType.TRANSLATOR, lang_code)
        except FactoryError:
            raise

    @staticmethod
    def _rate_limit_checks(state: AppState) -> None:
        """
        Blocks execution if the global rate limit state is active.

        Raises:
            CommandError: If the rate limit is currently active, with the remaining wait time.
        """
        state.check_rate_limit()
        if state.is_rate_limited:
            wait_time = state.get_remaining_wait_time()
            raise CommandError(f"API Rate limit in effect. Please wait {wait_time}s.")

    @staticmethod
    def _get_args(args: list[str]) -> tuple[str, str]:
        """
        Parses and validates command-line arguments for translation.

        Returns:
            A tuple of (input_path, lang_code).

        Raises:
            CommandError: If args is empty or the language code is not supported.
        """
        if not args:
            raise CommandError("Usage: translate <input_path> [he|en]")
        input_path: str = args[0]
        lang: str = args[1].lower() if len(args) > 1 else "he"
        if lang not in ["en", "he", "hebrew", "english"]:
            raise CommandError("Supported languages: 'en' (English), 'he' (Hebrew)")
        lang_code: str = "en" if lang in ["en", "english"] else "he"
        return (input_path, lang_code)

    @staticmethod
    def _check_path(input_path: str) -> None:
        """
        Validates that the source file exists on disk.

        Raises:
            FileNotFoundError: If no file exists at input_path.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"The file '{input_path}' doesn't exist.")

    @staticmethod
    def _get_file_name(input_path: str, lang_code: str) -> str:
        """Generates the output filename while cleaning redundant suffixes."""
        original_name: str = os.path.basename(input_path)
        stem: str = os.path.splitext(original_name)[0]
        for s in ["_eng", "_heb", "_he", "_en"]:
            if stem.endswith(s):
                stem = stem[:-len(s)]
        suffix: str = "heb" if lang_code == "he" else "eng"
        return f"{stem}_{suffix}.txt"
