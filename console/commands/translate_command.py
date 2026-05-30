from console.commands.command import Command, requires_key
from agents.translator import Translator, TranslatedData
from agents.models.model import Model
from agents.models.model_factory import ModelFactory
from agents.agent_factory import AgentFactory
from console.app_state import AppState
from console.exceptions import CommandError
from utils.text_writer import TextWriter
from utils.text_processor import TextProcessor
from google.genai.errors import APIError
import os
import time
import re

class TranslateCommand(Command):
    OUTPUT_DIR: str = "output"
    PROMPT_PATH: str = "prompts/translation_agent.md"
    RESOURCE_EXHAUSTED: int = 429

    @requires_key
    def execute(self, state: AppState, args: list[str] = None) -> None:
        state.check_rate_limit()
        if state.is_rate_limited:
            wait_time = state.get_remaining_wait_time()
            raise CommandError(f"API Rate limit in effect. Please wait {wait_time}s.")

        if not args:
            raise CommandError("Missing required argument. Usage: translate <input_path>")

        input_path: str = args[0]

        if not os.path.exists(input_path):
            raise CommandError(f"The file '{input_path}' doesn't exist.")

        try:
            self._create_translated_data(input_path, state)
            print(f"Processed chunk. Total session usage so far: {state.total_tokens_used} tokens.")
        except APIError as e:
            if e.code == self.RESOURCE_EXHAUSTED:
                self._handle_rate_limit(state, e)
                raise CommandError(f"API Quota exceeded. {e.message}")
            raise e

    def _handle_rate_limit(self, state: AppState, e: APIError) -> None:
        state.is_rate_limited = True
        wait_time = 60 # Default
        match = re.search(r"retry in ([\d.]+)s", str(e))
        if match:
            wait_time = int(float(match.group(1))) + 1
        state.retry_after = time.time() + wait_time
        print(f"Rate limit hit. Application will wait for {wait_time}s.")

    def _init_translator_agent(self, state: AppState) -> Translator:
        model: Model = ModelFactory(state.api_key, self.PROMPT_PATH, state.current_model).init_llm_model()
        agent_factory: AgentFactory = AgentFactory()
        return agent_factory.init_agent(model, agent_factory.TRANSLATOR)

    def _translate_data(self, input_path: str, state: AppState) -> list[str]:
        translator: Translator = self._init_translator_agent(state)
        translated_data: TranslatedData = translator.translate_from_file(input_path)
        translated_text: str = translated_data[0]
        tokens_used: int = translated_data[1]
        state.total_tokens_used += tokens_used
        return [translated_text]

    def _create_translated_data(self, input_path: str, state: AppState) -> None:
        translated_data: list[str] = self._translate_data(input_path, state)
        self._write_output_data(translated_data, input_path)

    def _write_output_data(self, data: list[str], input_path: str) -> None:
        text_writer: TextWriter = TextWriter(self.OUTPUT_DIR)
        file_name: str = self._get_file_name(input_path)
        processor: TextProcessor = TextProcessor(data).process()
        output_file_path: str = text_writer.write_list(processor, file_name)
        print(f"Created the output at {output_file_path}")

    @staticmethod 
    def _get_file_name(input_path: str) -> str: 
        original_name: str = os.path.basename(input_path)
        stem: str = os.path.splitext(original_name)[0]
        if stem.endswith("_eng"):
            stem = stem[:-4]
        return stem + "_heb.txt"
    