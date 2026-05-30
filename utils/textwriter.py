from pathlib import Path 

class TextWriter:
    TXT_EXTENSTION: str = ".txt"
    DEFAULT_ENCODING: str = "utf-8"
    SEPARATOR: str = "\n\n"

    def __init__(self, 
                 output_dir: str | Path, 
                 encoding: str = DEFAULT_ENCODING
                 ) -> None:
        
        self.output_dir: Path = Path(output_dir)
        self.encoding: str = encoding
        self._ensure_dir(self.output_dir)
    
    def write_dict(self, data: dict[str, str], filename: str) -> str:
        values: list[str] = list(data.values())
        return self.write_list(values, filename)
    
    def write_list(self, data: list[str], filename: str) -> str:
        file_path: Path = self.output_dir / self._ensure_extenstion(filename)
        content: str = self.SEPARATOR.join(data)
        
        with open(file_path, "w", encoding=self.encoding, newline="\n") as file:
            file.write(content)
            if data:
                file.write("\n")

        return str(file_path)

    def _write(self, filename: str, text: str) -> str:
        file_path: Path = self.output_dir / filename
        with open(file_path, "w", encoding=self.encoding, newline="\n") as file:
            file.write(text)
        return str(file_path)
    
    def _ensure_extenstion(self, filename: str) -> str:
        if filename.endswith(self.TXT_EXTENSTION):
            return filename
        return filename + self.TXT_EXTENSTION
    
    @staticmethod 
    def _ensure_dir(directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)