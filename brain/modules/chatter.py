import dspy
from typing import Optional

import os
from models import ChatHistory
from .responder import ResponderModule

class ChatterModule(dspy.Module):
    def __init__(self, examples: Optional[dict]):
        super().__init__()
        self.responder = ResponderModule()

    def forward(
        self,
        chat_history: ChatHistory,
    ):
        return self.responder(chat_history=chat_history)