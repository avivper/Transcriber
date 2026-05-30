"""
Factory for creating and initializing specialized AI agents.
Ensures agents are coupled with the correct Gemini model and target language.
"""

from .models import Model
from .transcriber import Transcriber
from .translator import Translator
from typing import TypeAlias 

# Type alias for any supported agent type
Agent: TypeAlias = Transcriber | Translator | None

class AgentFactory:
    """
    Central factory class for agent instantiation.
    
    Attributes:
        TRANSCRIBER: Constant identifier for the transcription agent.
        TRANSLATOR: Constant identifier for the translation agent.
    """
    TRANSCRIBER: str = "Transcriber"
    TRANSLATOR: str = "Translator"

    def init_agent(self, model: Model, agent: str, language: str = None) -> Agent:
        """
        Instantiates a specific agent based on the provided identifier.
        
        Args:
            model: An initialized Gemini Model wrapper.
            agent: The identifier for the desired agent type.
            language: Optional target language (defaults to 'en' for transcribe, 'he' for translate).
            
        Returns:
            The initialized Agent instance, or None if the identifier is invalid.
        """
        if agent == self.TRANSCRIBER:
            return Transcriber(model, language or "en")
        elif agent == self.TRANSLATOR:
            return Translator(model, language or "he")
        return None 
