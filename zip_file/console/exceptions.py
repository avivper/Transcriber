"""
Custom exception definitions for the console application.
"""

class CommandError(Exception):
    """
    Exception raised to signify a user-recoverable error in command execution.
    Caught by the Session loop to display clean feedback instead of a stack trace.
    """
    pass
