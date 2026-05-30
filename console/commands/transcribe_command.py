from console.commands.command import Command, requires_key
from agents.transcriber import Transcriber
from console.app_state import AppState
from utils.splitter import VideoSplitter
from utils.textwriter import TextWriter

class TranscribeCommand(Command):
    OUTPUT_DIR: str = "output"

    @requires_key
    def execute(self, state: AppState, args: list[str]) -> None:
        if (args is None or len(args) == 0):
            # TODO: raise error
            print("Error") 
        input_path: str = args[0]
        self._create_transcribed_output(input_path, state)
    
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
    
    def _transcribe_audios(self, audio_paths: list[str], api_key: str) -> dict[str, str]:
        transcriber: Transcriber = Transcriber(api_key)
        print(f"\nTranscribing {len(audio_paths)} parts...")
        results: dict[str, str] = transcriber.transcribe_files(audio_paths)
        return results
    
    def _write_output_to_files(self, data: dict[str,str], input_path: str) -> None:
        text_writer: TextWriter = TextWriter(self.OUTPUT_DIR)
        output_file_path: str = text_writer.write_dict(data, input_path)
        print(f"Created the output at {output_file_path}")

    def _create_transcribed_output(self, input_path: str, state: AppState) -> None:
        audio_paths: list[str] = self._split_videos_to_audios(input_path)
        transcribed_data: dict[str, str] = self._transcribe_audios(audio_paths, state.api_key)
        self._write_output_to_files(transcribed_data, input_path)