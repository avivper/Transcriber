"""
Custom exception hierarchy for the Transcriber application.
Centralizes error types used for specialized failure states in agents, factories, and utilities.
"""

class CommandError(Exception):
    """
    Exception raised to signify a user-recoverable error in command execution.
    Caught by the Session loop to display clean feedback instead of a stack trace.
    """
    pass

class FactoryError(ValueError):
    """
    Exception raised when a factory (e.g., AgentFactory) fails to initialize a requested component.
    Typically indicates an invalid identifier or missing configuration.
    """
    pass

class ProcessingError(Exception):
    """
    Exception raised when a data processing utility (e.g., TextProcessor) encounters 
    structural or logical inconsistencies in the input data.
    """
    pass
