from console.commands.command import Command, requires_key
from agents.translator import Translator
from console.app_state import AppState
from utils.textwriter import TextWriter

class TranslateCommand(Command):
    OUTPUT_DIR: str = "output"

    @requires_key
    def execute(self, state: AppState, args: list[str]) -> None:
        if (args is None or len(args) == 0):
            # TODO: raise error
            print("Error") 
        input_path: str = args[0]
        self._create_translated_data(input_path, state)
    
    def _translate_data(self, input_path: str, state: AppState) -> list[str]:
        translator: Translator = Translator(state.api_key)
        return translator.translate_from_file(input_path)
    
    def _write_output_data(self, data: list[str], input_path: str) -> None:
        text_writer: TextWriter = TextWriter(self.OUTPUT_DIR)
        output_file_path: str = text_writer.write_list(data, input_path)
        print(f"Created the output at {output_file_path}")
    
    def _create_translated_data(self, input_path: str, state: AppState) -> None:
        translated_data: list[str] = self._translate_data(input_path, state)
        self._write_output_data(translated_data, input_path)