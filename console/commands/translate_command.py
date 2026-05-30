from console.commands.command import Command, requires_key
from agents.translator import Translator
from agents.models.model import Model 
from agents.models.model_factory import ModelFactory
from console.app_state import AppState
from console.exceptions import CommandError
from utils.textwriter import TextWriter
import os

class TranslateCommand(Command):
    OUTPUT_DIR: str = "output"
    PROMPT_PATH: str = "prompts/translation_agent.md"

    @requires_key
    def execute(self, state: AppState, args: list[str]) -> None:
        if not args:
            raise CommandError("Missing required argument. Usage: translate <input_path>")
        
        input_path: str = args[0]

        if not os.path.exists(input_path):
            raise CommandError(f"The file '{input_path} doesn't exists.")

        self._create_translated_data(input_path, state.api_key)
    
    def _init_translator_agent(self, api_key: str) -> Translator:
        model: Model = ModelFactory(api_key, self.PROMPT_PATH).init_llm_model()
        return Translator(model)
    
    def _translate_data(self, input_path: str, api_key: str) -> list[str]:
        translator: Translator = self._init_translator_agent(api_key)
        return translator.translate_from_file(input_path)
    
    def _create_translated_data(self, input_path: str, api_key: str) -> None:
        translated_data: list[str] = self._translate_data(input_path, api_key)
        self._write_output_data(translated_data, input_path)

    def _write_output_data(self, data: list[str], input_path: str) -> None:
        text_writer: TextWriter = TextWriter(self.OUTPUT_DIR)
        output_file_path: str = text_writer.write_list(data, os.path.basename(input_path))
        print(f"Created the output at {output_file_path}")
    