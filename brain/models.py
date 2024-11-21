from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class MessageContext(BaseModel):
    message_number: int
    time_of_day: str
    minutes_since_start: int
    minutes_since_last: int


class ChatMessage(BaseModel):
    from_creator: bool
    content: str
    context: Optional[MessageContext] = None

    def __str__(self):
        role = "YOU" if self.from_creator else "THE FAN"
        message = role + ": " + self.content
        return message

class ChatHistory(BaseModel):
    messages: List[ChatMessage] = []

    def __str__(self):
        messages = []
        for i, message in enumerate(self.messages):
            message_str = str(message)
            messages.append(message_str)
        return "\n".join(messages)
    
    def model_dump_json(self, **kwargs):
        return str(self)