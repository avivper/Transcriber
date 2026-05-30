import os
import math
from pydub import AudioSegment

class VideoSplitter:
    MP4_FORMAT: str = "mp4"
    MP3_FORMAT: str = "mp3"
    MS_PER_MINUTE: int = 60 * 1000

    def __init__(
            self, input_path: str, 
            mintus_per_chunk: int = 20, 
            output_dir: str = None
            ) -> None:
        
        self.input_path: str = input_path
        self.chunk_ms: int = mintus_per_chunk * self.MS_PER_MINUTE
        self._audio: AudioSegment = None
        self.output_dir: str = self._set_output_dir(output_dir)
    
    def get_parts_to_split(self) -> int:
        audio: AudioSegment = self._load_audio()
        total_ms: int = len(audio)
        return self._get_number_of_parts(total_ms)
    
    @property
    def duration_ms(self) -> int: 
        return len(self._load_audio())
    
    def split(self) -> list[str]:
        audio: AudioSegment = self._load_audio()
        total_ms: int = len(audio)
        base_name: str = self._get_base_name()
        output_paths: list[str] = []
        number_of_parts: int = self._get_number_of_parts(total_ms)

        for i in range(number_of_parts):
            out_path: str = self._process_audio_data(i, total_ms, audio, base_name)
            output_paths.append(out_path)
        return output_paths
    
    def _process_audio_data(
            self, index: int, total_ms: int, 
            audio: AudioSegment, base_name: str
            ) -> str:
        start: int = index * self.chunk_ms
        end: int = self._determine_end_point(start, total_ms)
        chunk: AudioSegment = audio[start:end]
        return self._create_output_path(base_name, index, chunk)

    def _load_audio(self) -> AudioSegment:
        if self._audio is None:
            self._audio = AudioSegment.from_file(
                self.input_path, 
                self.MP4_FORMAT
                )
        return self._audio
    
    def _get_base_name(self) -> str:
        return os.path.basename(self.input_path)
    
    def _create_output_path(self, base_name: str ,index: int, chunk: AudioSegment) -> str: 
        file_name: str = f"{base_name}_part{index + 1}.mp3"
        out_path: str = os.path.join(self.output_dir, file_name)
        chunk.export(out_path, format=self.MP3_FORMAT)
        return out_path
    
    def _set_output_dir(self, output_dir = None) -> str:
        if (output_dir is None):
            return os.path.dirname(self.input_path)
        return output_dir
    
    def _determine_end_point(self, start: int, total_ms: int) -> int:
        return min(start + self.chunk_ms, total_ms)
    
    def _get_number_of_parts(self, total_ms: int) -> int:
        return math.ceil(total_ms / self.chunk_ms)
