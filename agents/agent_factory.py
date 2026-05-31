"""
Factory for creating and initializing specialized AI agents.
Ensures agents are coupled with the correct Gemini model and target language.
"""

from .models import Model
from .transcriber import Transcriber
from .translator import Translator
from typing import TypeAlias 
from utils import FactoryError
from enum import Enum

class AgentType(Enum):
    """
    Supported AI agent types within the Transcriber ecosystem.
    """
    TRANSCRIBER = "Transcriber"
    TRANSLATOR = "Translator"

# Type alias for any supported agent type
Agent: TypeAlias = Transcriber | Translator
AgentCollection: TypeAlias = dict[AgentType, tuple[type[Agent], str]]

class AgentFactory:
    """Central factory class for agent instantiation."""

    _agents : AgentCollection = {
        AgentType.TRANSCRIBER: (Transcriber, "en"),
        AgentType.TRANSLATOR: (Translator, "he")
    }

    @classmethod
    def init_agent(
            cls, model: Model, agent_type: AgentType, language: str | None = None
            ) -> Agent:
        """
        Instantiates a specific agent based on the provided type.

        Args:
            model: An initialized Gemini Model wrapper.
            agent_type: The type of agent to create.
            language: Optional target language (defaults to 'en' for transcribe, 'he' for translate).

        Returns:
            The initialized Agent instance.

        Raises:
            FactoryError: If agent_type is not a registered agent.
        """
        try:
            agent_cls, default_language = cls._agents[agent_type]
            return agent_cls(model, language or default_language)
        except KeyError:
            raise FactoryError(
            f"Unknown agent type: {agent_type}"
            )
