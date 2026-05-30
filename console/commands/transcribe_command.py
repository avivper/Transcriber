from console.commands.command import Command, requires_key
from agents.transcriber import Transcriber, TranscribedData
from agents.models.model import Model
from agents.models.model_factory import ModelFactory
from agents.agent_factory import AgentFactory
from console.exceptions import CommandError
from console.app_state import AppState
from utils.splitter import VideoSplitter
from utils.text_writer import TextWriter
from utils.text_processor import TextProcessor
from google.genai.errors import APIError
from typing import Tuple
import os
import time
import re

class TranscribeCommand(Command):
    OUTPUT_DIR: str = "output"
    RESOURCE_EXHAUSTED: int = 429
    WAIT_TIME: int = 60

    @requires_key
    def execute(self, state: AppState, args: list[str] = None) -> None:
        try:
            self._rate_limit_checks(state)
            user_input: Tuple[str,str] = self._get_args(args)
            input_path: str = user_input[0]
            lang_code: str = user_input[1]
            if self._check_path(input_path):
                prompt_path: str = f"prompts/transcription_{lang_code}.md"
                self._create_transcribed_output(input_path, state, lang_code, prompt_path)
                print(f"Processed chunk. Total session usage so far: {state.total_tokens_used} tokens.")
        except APIError as e:
            if e.code == self.RESOURCE_EXHAUSTED:
                self._handle_rate_limit(state, e)
                raise CommandError(f"API Quota exceeded. {e.message}")
            raise e
    
    def _handle_rate_limit(self, state: AppState, e: APIError) -> None:
        state.is_rate_limited = True
        match = re.search(r"retry in ([\d.]+)s", str(e))
        wait_time: int = self.WAIT_TIME
        if match:
            wait_time = int(float(match.group(1))) + 1
        state.retry_after = time.time() + wait_time
        print(f"Rate limit hit. Application will wait for {wait_time}s.")
    
    def _split_videos_to_audios(self, input_path: str) -> list[str]:
        print(f"Splitting '{input_path}'...")
        video_splitter: VideoSplitter = VideoSplitter(input_path)
        print(f"Video duration: {video_splitter.duration_ms / 1000:.1f}s")
        return self._get_audio_parts(video_splitter)
    
    def _get_audio_parts(self, video_splitter: VideoSplitter) -> list[str]:
        parts: list[str] = video_splitter.split()
        print(f"\nCreated {len(parts)} parts:")
        for path in parts:
            print(f" {path}")
        return parts
    
    def _transcribe_audios(
            self, audio_paths: list[str], state: AppState, 
            lang_code: str, prompt_path: str
            ) -> dict[str, str]:
        transcriber: Transcriber = self._init_transcriber_agent(state, lang_code, prompt_path)
        print(f"\nTranscribing {len(audio_paths)} parts...")
        transcribed_data: TranscribedData = transcriber.transcribe_files(audio_paths)
        results: dict[str, str] = transcribed_data[0]
        tokens_used: int = transcribed_data[1]
        state.total_tokens_used += tokens_used
        return results
    
    def _write_output_to_files(self, data: dict[str, str], input_path: str, lang_code: str) -> None:
        text_writer: TextWriter = TextWriter(self.OUTPUT_DIR)
        processed: list[str] = self._get_processed_data(data)
        file_name: str = self._get_file_name(input_path, lang_code)
        output_file_path: str = text_writer.write_list(processed, file_name)
        print(f"Created the output at {output_file_path}")

    def _clean_up_audio_files(self, audio_paths: list[str]) -> None:
        for path in audio_paths:
            os.remove(path)
        print(f"Removed {len(audio_paths)} temporary audio file(s).")

    def _create_transcribed_output(
            self, input_path: str, state: AppState, 
            lang_code: str, prompt_path: str
            ) -> None:
        audio_paths: list[str] = []
        try:
            audio_paths = self._split_videos_to_audios(input_path)
            transcribed_data: dict[str, str] = self._transcribe_audios(
                audio_paths, state, lang_code, prompt_path
                )
            self._write_output_to_files(transcribed_data, input_path, lang_code)
        finally:
            if audio_paths:
                self._clean_up_audio_files(audio_paths)

    @staticmethod
    def _get_processed_data(data: dict[str, str]) -> list[str]:
        values: list[str] = list(data.values())
        text_processor: TextProcessor = TextProcessor(values)
        return text_processor.process()
    
    @staticmethod
    def _get_file_name(input_path: str, lang_code: str) -> str:
        original_name: str = os.path.basename(input_path)
        stem: str = os.path.splitext(original_name)[0]
        suffix: str = "heb" if lang_code == "he" else "eng"
        return f"{stem}_{suffix}.txt"
    
    @staticmethod
    def _rate_limit_checks(state: AppState) -> None:
        state.check_rate_limit()
        if state.is_rate_limited:
            wait_time = state.get_remaining_wait_time()
            raise CommandError(f"API Rate limit in effect. Please wait {wait_time}s.")
        
    @staticmethod
    def _get_args(args: list[str]) -> Tuple[str, str]:
        if not args:
            raise CommandError("Missing required argument. Usage: transcribe <input_path>")
        input_path: str = args[0]
        lang: str = args[1].lower() if len(args) > 1 else "en"
        if lang not in ["en", "he", "hebrew", "english"]:
            raise CommandError("Supported languages: 'en' (English), 'he' (Hebrew)")
        lang_code: str = "he" if lang in ["he", "hebrew"] else "en"
        return (input_path, lang_code)
    
    @staticmethod
    def _check_path(input_path: str) -> bool:
        if not os.path.exists(input_path):
            raise CommandError(f"The file '{input_path}' doesn't exist.")
        return True
    
    @staticmethod
    def _init_transcriber_agent(state: AppState, lang_code: str, prompt_path: str) -> Transcriber:
        model: Model = ModelFactory(state.api_key, prompt_path, state.current_model).init_llm_model()
        agent_factory: AgentFactory = AgentFactory()
        return agent_factory.init_agent(model, agent_factory.TRANSCRIBER, lang_code)
    