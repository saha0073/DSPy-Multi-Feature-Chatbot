import os

# Get the brain directory path
brain_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(brain_dir, "saved_models", "optimized_knn_no_context.json")

# Debug print
print(f"Looking for model at: {model_path}")

from models import ChatMessage, ChatHistory
import dspy
from lms.together import Together
from modules.chatter import ChatterModule

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

# Initialize with proper error handling
chat_history = ChatHistory()
chatter = ChatterModule(examples=None)
try:
    chatter.load(path=model_path)
    print("Model loaded successfully")
except FileNotFoundError as e:
    print(f"Error: Model file not found at {model_path}")
    print("Current working directory:", os.getcwd())
    raise e

while True:
    # Get user input
    user_input = input("You: ")

    # Append user input to chat history
    chat_history.messages.append(
        ChatMessage(
            from_creator=False,
            content=user_input,
        ),
    )

    # Send request to endpoint
    response = chatter(chat_history=chat_history).output

    # Append response to chat history
    chat_history.messages.append(
        ChatMessage(
            from_creator=True,
            content=response,
        ),
    )
    # Print response
    print()
    print("Response:", response)
    print()
    # uncomment this line to see the 
    # lm.inspect_history(n=1)