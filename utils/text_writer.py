"""
Utility for persisting processed text data to the local filesystem.
"""

from pathlib import Path
from .exceptions import CommandError

class TextWriter:
    """
    Handles file creation and content writing for transcriptions and translations.
    """
    TXT_EXTENSION: str = ".txt"
    DEFAULT_ENCODING: str = "utf-8"
    SEPARATOR: str = "\n\n"

    def __init__(self, 
                 output_dir: str | Path, 
                 encoding: str = DEFAULT_ENCODING
                 ) -> None:
        """
        Initializes the writer with a target directory.

        Args:
            output_dir: Path to the directory where files will be written.
            encoding: File encoding to use (default: utf-8).

        Raises:
            CommandError: If the output directory cannot be created.
        """
        self.output_dir: Path = Path(output_dir)
        self.encoding: str = encoding
        try:
            self._ensure_dir(self.output_dir)
        except OSError as e:
            raise CommandError(f"Failed to prepare output directory '{output_dir}': {e}")

    def write_list(self, data: list[str], filename: str) -> str:
        """
        Joins list items and writes them to a text file.

        Args:
            data: List of strings to persist.
            filename: Target filename (the .txt extension is added if missing).

        Returns:
            The absolute path to the created file.

        Raises:
            CommandError: If the file cannot be written due to permission or OS errors.
        """
        file_path: Path = self.output_dir / self._ensure_extension(filename)
        content: str = self.SEPARATOR.join(data)
        
        try:
            with open(file_path, "w", encoding=self.encoding, newline="\n") as file:
                file.write(content)
                if data:
                    file.write("\n")
        except PermissionError:
            raise CommandError(f"Permission denied: Cannot write to '{file_path}'. Check folder permissions.")
        except OSError as e:
            raise CommandError(f"Failed to save output to '{file_path}': {e}")

        return str(file_path)
    
    def _ensure_extension(self, filename: str) -> str:
        """Guarantees the filename ends with .txt."""
        if filename.endswith(self.TXT_EXTENSION):
            return filename
        return filename + self.TXT_EXTENSION
    
    @staticmethod 
    def _ensure_dir(directory: Path) -> None:
        """Creates the target directory if it does not exist."""
        directory.mkdir(parents=True, exist_ok=True)
