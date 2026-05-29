import os
from pydub import AudioSegment

class VideoSplitter:

    MP4_FORMAT: str = "mp4"
    MP3_FORMAT: str = "mp3"

    def __init__(
            self, input_path: str, 
            parts_to_split: int, 
            output_dir: str = None
            ) -> None:
        
        self.input_path: str = input_path
        self.parts_to_split: int = parts_to_split
        self._audio: AudioSegment = None
        self.output_dir: str = self._set_output_dir(output_dir)
    
    @property
    def duration_ms(self) -> int: 
        return len(self._load_audio())
    

    def split(self) -> list[str]:
        audio: AudioSegment = self._load_audio()
        chunk_ms: int = len(audio) // self.parts_to_split
        base_name: str = self._get_base_name()
        output_paths: list[str] = []

        start: int = 0
        end: int = 0

        for i in range(self.parts_to_split):
            start = i * chunk_ms
            end = self._init_end_time_to_split(i, start, chunk_ms, audio)
            
            chunk: AudioSegment = audio[start:end]
            out_path: str = self._create_output_path(base_name, i, chunk)
            output_paths.append(out_path)
        
        return output_paths
    
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
    
    def _init_end_time_to_split(self, 
                                index: int, start: int, 
                                chunk_ms: int, audio: AudioSegment
                                ) -> int:
        if (index < self.parts_to_split - 1):
            return start + chunk_ms
        return len(audio)
