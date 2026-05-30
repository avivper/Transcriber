import re

class TextProcessor:
    TOKENS_PER_LINE: int = 18
    SPEAKER_PATTERN: str = r'(?=\*\*(?:Lecturer|מרצה):\*\*)'
    SEPARATOR: str = "\n\n"

    def __init__(self, data: list[str]) -> None:
        self.data = data

    def process(self) -> list[str]:
        return [self._process_chunk(chunk) for chunk in self.data]
    
    def _process_chunk(self, text: str) -> str:
        parts: list[str] = re.split(self.SPEAKER_PATTERN, text)
        header: str = parts[0]
        segments: list[str] = parts[1:]
        processed: list[str] = [
            self._process_segment(segment) for segment in segments
            ]
        if processed:
            return header.rstrip('\n') + self.SEPARATOR + self.SEPARATOR.join(processed)
        return text

    def _process_segment(self, segment: str) -> str:
        lines: list[str] = segment.split('\n', 1)
        speaker_line: str = lines[0]
        body: str = lines[1].strip() if len(lines) > 1 else ""
        return f"{speaker_line}\n{self._reflow(body)}"
    
    def _reflow(self, text: str) -> str:
        tokens: list[str] = text.split()
        chunks: list[str] = [
            ' '.join(tokens[i:i + self.TOKENS_PER_LINE])
            for i in range (0, len(tokens), self.TOKENS_PER_LINE)
        ]
        return '\n'.join(chunks)