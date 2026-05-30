from agents.models import Model
from .transcriber import Transcriber
from .translator import Translator
from typing import TypeAlias 

Agent: TypeAlias = Transcriber | Translator | None

class AgentFactory:
    TRANSCRIBER: str = "Transcriber"
    TRANSLATOR: str = "Translator"

    def init_agent(self, model: Model, agent: str, language: str = None) -> Agent:
        if agent == self.TRANSCRIBER:
            return Transcriber(model, language or "en")
        elif agent == self.TRANSLATOR:
            return Translator(model, language or "he")
        return None 
 