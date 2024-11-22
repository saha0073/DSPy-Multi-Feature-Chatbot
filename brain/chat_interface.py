import os

from models import ChatMessage, ChatHistory, MessageContext
import dspy
from lms.together import Together
from modules.chatter import ChatterModule
from datetime import datetime
import time

# Get the brain directory path and set up model path
brain_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(brain_dir, "saved_models", "optimized_chatbot_with_context.json")

# Debug print
print(f"Looking for model at: {model_path}")

# Configure LM
lm = Together(
    model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    temperature=0.5,
    max_tokens=1000,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1.2,
    stop=["<|eot_id|>", "<|eom_id|>", "\n\n---\n\n", "\n\n---", "---", "\n---"],
)

dspy.settings.configure(lm=lm)

# Initialize chat components with proper error handling
chat_history = ChatHistory(messages=[])
chatter = ChatterModule(examples=None)
try:
    chatter.load(path=model_path)
    print("Model loaded successfully")
except FileNotFoundError as e:
    print(f"Error: Model file not found at {model_path}")
    print("Current working directory:", os.getcwd())
    raise e

# Initialize timing
start_time = time.time()
last_message_time = start_time
message_counter = 0

# Add these constants at the top with other imports
FORBIDDEN_TERMS = {
    'social_media': [
        'instagram', 'twitter', 'facebook', 'tiktok', 'snapchat', 
        'linkedin', 'youtube', 'reddit', 'discord', 'telegram'
    ],
    'meetup_terms': [
        'meet up', 'meet in person', 'get together', 'coffee', 
        'dinner', 'lunch', 'hangout', 'in person', 'meet somewhere',
        'location', 'address', 'place to meet'
    ]
}

# Add this after your existing imports
EMOJI_MAP = {
    "thank": "😊",
    "love": "❤️",
    "excited": "🎉",
    "content": "📸",
    "photo": "📷",
    "video": "🎥",
    "subscribe": "⭐",
    "exclusive": "✨",
    "special": "🌟",
    "chat": "💭",
    "new": "✨"
}

def add_emojis(response):
    """Add relevant emojis to the response"""
    modified_response = response
    for word, emoji in EMOJI_MAP.items():
        if word in response.lower():
            # Add emoji before exclamation marks or at the end
            modified_response = modified_response.replace("!", f" {emoji}!")
    
    # If no exclamation marks and emoji was needed, add to end
    if modified_response == response:
        for word, emoji in EMOJI_MAP.items():
            if word in response.lower():
                modified_response = modified_response + f" {emoji}"
    
    return modified_response

def validate_response(text):
    """Check if response contains forbidden topics"""
    text_lower = text.lower()
    
    # Check for forbidden social media (except OnlyFans)
    for platform in FORBIDDEN_TERMS['social_media']:
        if platform.lower() in text_lower:
            return False, f"Contains forbidden platform: {platform}"
            
    # Check for meetup suggestions
    for term in FORBIDDEN_TERMS['meetup_terms']:
        if term.lower() in text_lower:
            return False, f"Contains meetup suggestion: {term}"
            
    return True, ""

def get_safe_response(chatter, chat_str, context_str):
    """Get a response that doesn't contain forbidden topics and includes emojis"""
    max_attempts = 3
    
    for attempt in range(max_attempts):
        response = chatter(
            chat_history=chat_str,
            context=context_str
        )
        
        is_safe, reason = validate_response(response)
        if is_safe:
            return add_emojis(response)  # Add emojis to safe responses
        print(f"Filtered attempt {attempt + 1}: {reason}")
    
    return "I prefer to keep our interaction here on OnlyFans. How can I help you today? 💭"

def get_context(message_number):
    current_time = time.time()
    
    # Get time of day
    hour = datetime.now().hour
    if 5 <= hour < 12:
        time_of_day = "morning"
    elif 12 <= hour < 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"
    
    # Calculate times
    minutes_since_start = int((current_time - start_time) / 60)
    minutes_since_last = int((current_time - last_message_time) / 60)
    
    return MessageContext(
        message_number=message_number,
        time_of_day=time_of_day,
        minutes_since_start=minutes_since_start,
        minutes_since_last=minutes_since_last
    )

def format_chat_history(history):
    result = []
    for msg in history.messages:
        speaker = "Creator" if msg.from_creator else "Fan"
        context = f"[Time: {msg.context.time_of_day}, Message #{msg.context.message_number}]"
        result.append(f"{speaker} {context}: {msg.content}")
    return "\n".join(result)

def format_context(context):
    return (f"Current context: Time of day: {context.time_of_day}, "
            f"Message #{context.message_number}, "
            f"Minutes since start: {context.minutes_since_start}, "
            f"Minutes since last: {context.minutes_since_last}")

print("Chat started! (Type 'quit' to exit)")
print("-" * 50)

while True:
    # Get user input
    user_input = input("You: ")
    
    if user_input.lower() == 'quit':
        print("\nChat ended. Goodbye!")
        break

    # Update counter and get context
    message_counter += 1
    context = get_context(message_counter)

    # Append user input to chat history
    chat_history.messages.append(
        ChatMessage(
            from_creator=False,
            content=user_input,
            context=context
        )
    )

    try:
        # Format inputs as strings
        chat_str = format_chat_history(chat_history)
        context_str = format_context(context)
        
        # Get safe response using loaded model with context
        response = get_safe_response(chatter, chat_str, context_str)

        # Update timing
        last_message_time = time.time()
        
        # Update counter and get new context for response
        message_counter += 1
        context = get_context(message_counter)
        
        # Append response to chat history
        chat_history.messages.append(
            ChatMessage(
                from_creator=True,
                content=response,
                context=context
            )
        )
        
        # Print response
        print()
        print("Response:", response)
        print()
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please try again.")
        print("-" * 50)
    
    # Uncomment this line to see the LM history
    # lm.inspect_history(n=1)