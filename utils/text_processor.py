"""
Utility for refining and formatting transcription text.
Handles regex-based splitting and line-wrapping for better readability.
"""

import re

class TextProcessor:
    """
    Processes raw LLM output to enforce formatting and line constraints.
    """
    TOKENS_PER_LINE: int = 18
    SPEAKER_PATTERN: str = r'(?=\*\*(?:Lecturer|מרצה):\*\*)'
    SEPARATOR: str = "\n\n"

    def __init__(self, data: list[str]) -> None:
        """Initializes the processor with a list of text chunks."""
        self.data: list[str] = data

    def process(self) -> list[str]:
        """Runs the formatting pipeline on all data chunks."""
        return [self._process_chunk(chunk) for chunk in self.data]
    
    def _process_chunk(self, text: str) -> str:
        """Splits a chunk by speaker labels and reflows the body text."""
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
        """Formats a single speaker segment."""
        lines: list[str] = segment.split('\n', 1)
        speaker_line: str = lines[0]
        body: str = lines[1].strip() if len(lines) > 1 else ""
        return f"{speaker_line}\n{self._reflow(body)}"
    
    def _reflow(self, text: str) -> str:
        """Wraps text to a specific token count per line."""
        tokens: list[str] = text.split()
        chunks: list[str] = [
            ' '.join(tokens[i:i + self.TOKENS_PER_LINE])
            for i in range (0, len(tokens), self.TOKENS_PER_LINE)
        ]
        return '\n'.join(chunks)
