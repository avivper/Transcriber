from agents.models.model import Model
from agents.transcriber import Transcriber
from agents.translator import Translator
from typing import TypeAlias 

Agent: TypeAlias = Transcriber | Translator | None

class AgentFactory:
    TRANSCRIBER: str = "Transcriber"
    TRANSLATOR: str = "Translator"

    def init_agent(self, model: Model, agent: str) -> Agent:
        if agent == self.TRANSCRIBER:
            return Transcriber(model)
        elif agent == self.TRANSLATOR:
            return Translator(model)
        return None 