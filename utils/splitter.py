"""
Utility for splitting video files into manageable audio chunks.
Handles format conversion and directory management for temporary artifacts.
"""

import os
import math
from pydub import AudioSegment
from .exceptions import ProcessingError

class VideoSplitter:
    """
    Slices an MP4 video into equal-length MP3 audio parts.
    
    Attributes:
        MP4_FORMAT: Expected input format.
        MP3_FORMAT: Target output format.
        MS_PER_MINUTE: Conversion constant for milliseconds.
    """
    MP4_FORMAT: str = "mp4"
    MP3_FORMAT: str = "mp3"
    MS_PER_MINUTE: int = 60 * 1000

    def __init__(
            self, input_path: str,
            minutes_per_chunk: int = 20,
            output_dir: str = None
            ) -> None:
        """
        Initializes the splitter with path and chunk size.

        Args:
            input_path: Path to the source MP4 file.
            minutes_per_chunk: Maximum duration of each chunk in minutes.
            output_dir: Optional directory for output files (defaults to source folder).
        """
        self.input_path: str = input_path
        self.chunk_ms: int = minutes_per_chunk * self.MS_PER_MINUTE
        self._audio: AudioSegment = None
        self.output_dir: str = self._set_output_dir(output_dir)
    
    def get_parts_to_split(self) -> int:
        """
        Calculates how many chunks the file will be split into.

        Returns:
            The number of chunks based on total duration and chunk size.

        Raises:
            ProcessingError: If the audio file cannot be loaded.
        """
        try:
            audio: AudioSegment = self._load_audio()
            total_ms: int = len(audio)
            return self._get_number_of_parts(total_ms)
        except ProcessingError:
            raise
    
    @property
    def duration_ms(self) -> int:
        """
        Returns the total duration of the loaded audio in milliseconds.

        Raises:
            ProcessingError: If the audio file cannot be loaded.
        """
        try:
            return len(self._load_audio())
        except ProcessingError:
            raise
    
    def split(self) -> list[str]:
        """
        Performs the splitting operation.

        Returns:
            A list of paths to all generated MP3 chunks.

        Raises:
            ProcessingError: If the audio cannot be loaded or any chunk cannot be written to disk.
        """
        try:
            audio: AudioSegment = self._load_audio()
            total_ms: int = len(audio)
            base_name: str = self._get_base_name()
            output_paths: list[str] = []
            number_of_parts: int = self._get_number_of_parts(total_ms)
            
            for i in range(number_of_parts):
                out_path: str = self._process_audio_data(i, total_ms, audio, base_name)
                output_paths.append(out_path)
            return output_paths
            
        except ProcessingError:
            raise
    
    def _process_audio_data(
            self, index: int, total_ms: int, 
            audio: AudioSegment, base_name: str
            ) -> str:
        """Slices and exports a single chunk."""
        start: int = index * self.chunk_ms
        end: int = self._determine_end_point(start, total_ms)
        chunk: AudioSegment = audio[start:end]
        return self._create_output_path(base_name, index, chunk)

    def _load_audio(self) -> AudioSegment:
        """
        Loads the audio file into memory if not already cached, then returns it.

        Returns:
            The loaded AudioSegment, from cache or freshly read from disk.

        Raises:
            ProcessingError: If the file is missing, ffmpeg is not installed, or loading fails.
        """
        try:
            if self._audio is None:
                self._audio = AudioSegment.from_file(
                    self.input_path,
                    self.MP4_FORMAT
                    )
            return self._audio
        except FileNotFoundError:
            raise ProcessingError(
                f"Couldn't find the file: {self.input_path}"
            )
        except RuntimeError:
            raise ProcessingError(
                f"ffmpeg isn't installed. Please install ffmpeg to process videos."
            )
        except Exception as e:
            raise ProcessingError(
                f"Failed to process the video file: {str(e)}"
                )
    
    def _get_base_name(self) -> str:
        """Extracts the filename without path for chunk naming."""
        return os.path.basename(self.input_path)
    
    def _create_output_path(self, base_name: str ,index: int, chunk: AudioSegment) -> str:
        """
        Exports a chunk to disk and returns its path.

        Args:
            base_name: The source filename used as a naming prefix.
            index: Zero-based chunk index, used in the output filename.
            chunk: The audio segment to export.

        Returns:
            The absolute path to the written MP3 file.

        Raises:
            ProcessingError: If the chunk cannot be written to disk.
        """
        file_name: str = f"{base_name}_part{index + 1}.mp3"
        out_path: str = os.path.join(self.output_dir, file_name)
        try:
            chunk.export(out_path, format=self.MP3_FORMAT)
        except OSError as e:
            raise ProcessingError(f"Failed to write audio chunk '{out_path}': {e}")
        return out_path
    
    def _set_output_dir(self, output_dir = None) -> str:
        """Determines the target directory for chunks."""
        if output_dir is None:
            return os.path.dirname(self.input_path) or "."
        return output_dir
    
    def _determine_end_point(self, start: int, total_ms: int) -> int:
        """Calculates the end timestamp for a chunk slice."""
        return min(start + self.chunk_ms, total_ms)
    
    def _get_number_of_parts(self, total_ms: int) -> int:
        """Calculates chunk count based on total duration and chunk size."""
        return math.ceil(total_ms / self.chunk_ms)
