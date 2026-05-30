from pathlib import Path

class TextWriter:
    TXT_EXTENSION: str = ".txt"
    DEFAULT_ENCODING: str = "utf-8"
    SEPARATOR: str = "\n\n"

    def __init__(self, 
                 output_dir: str | Path, 
                 encoding: str = DEFAULT_ENCODING
                 ) -> None:
        
        self.output_dir: Path = Path(output_dir)
        self.encoding: str = encoding
        self._ensure_dir(self.output_dir)

    def write_list(self, data: list[str], filename: str) -> str:
        file_path: Path = self.output_dir / self._ensure_extension(filename)
        content: str = self.SEPARATOR.join(data)
        
        with open(file_path, "w", encoding=self.encoding, newline="\n") as file:
            file.write(content)
            if data:
                file.write("\n")

        return str(file_path)
    
    def _ensure_extension(self, filename: str) -> str:
        if filename.endswith(self.TXT_EXTENSION):
            return filename
        return filename + self.TXT_EXTENSION
    
    @staticmethod 
    def _ensure_dir(directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)