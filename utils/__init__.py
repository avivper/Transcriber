"""
Utility package for audio/video processing and text manipulation.
Provides tools for splitting files, reflowing text, and writing outputs to disk.
"""

from .splitter import VideoSplitter
from .text_processor import TextProcessor
from .text_writer import TextWriter
from .exceptions import ProcessingError, CommandError, FactoryError
