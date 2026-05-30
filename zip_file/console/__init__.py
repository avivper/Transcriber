"""
Console package for managing the interactive REPL.
Contains the main Session loop, shared AppState, and custom exceptions.
"""

from .session import Session
from .app_state import AppState
from .exceptions import CommandError
