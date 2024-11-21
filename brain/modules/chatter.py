from dataclasses import dataclass
from datetime import datetime
import dspy
from typing import List, Dict

@dataclass
class MessageContext:
    message_number: int
    time_of_day: str
    minutes_since_start: int
    minutes_since_last: int

@dataclass
class ChatMessage:
    from_creator: bool
    content: str
    context: MessageContext

@dataclass
class ChatHistory:
    messages: List[ChatMessage]

def format_chat_history(chat_history):
    """Convert ChatHistory to formatted string"""
    result = []
    for msg in chat_history.messages:
        speaker = "Creator" if msg.from_creator else "Fan"
        context = f"[Time: {msg.context.time_of_day}, Message #{msg.context.message_number}]"
        result.append(f"{speaker} {context}: {msg.content}")
    return "\n".join(result)

def format_context(context):
    """Convert MessageContext to formatted string"""
    return (f"Current context: Time of day: {context.time_of_day}, "
            f"Message #{context.message_number}, "
            f"Minutes since start: {context.minutes_since_start}, "
            f"Minutes since last: {context.minutes_since_last}")

class ChatterModule(dspy.Module):
    def __init__(self, examples=None):
        super().__init__()
        
        self.responder = dspy.Predict(
            "chat_history: str, context: str -> reasoning: str, output: str",
            instructions="""You are an OnlyFans creator chatting with a fan.
            Consider the context:
            - Time of day (morning/afternoon/evening)
            - How long the conversation has been going
            - Number of messages exchanged
            - Time since last message
            Adjust your response style and energy accordingly."""
        )

    def forward(self, chat_history, context):
        # Convert inputs to strings if they aren't already
        chat_str = format_chat_history(chat_history) if isinstance(chat_history, ChatHistory) else chat_history
        context_str = format_context(context) if hasattr(context, 'time_of_day') else context
        
        # Get response
        response = self.responder(
            chat_history=chat_str,
            context=context_str
        )
        
        return response.output