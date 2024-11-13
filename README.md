So instead of doing a basic off-the-shelf take home which is probably now easily solved using chatgpt or something, I thought it'd be better to have it be more custom-fit to the problem Whisper is solving.

# Project Overview

This takehome is basically a super dumbed down version of the product Whisper makes. It uses DSPy, which is a tool useful for making LLM-based applications. It has some pretty interesting abstractions which I like and have found convenient for tinkering and building in the space we're working in.

The takehome already contains a somewhat functioning chatbot. The first step is to get the chatbot to run and talk to it. If you're using VS code, to do this, add the following vs code configuration and press play:

{
    "name": "Python: local_chat",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/brain/chat_interface.py",
    "console": "integratedTerminal",
    "env": {
        "TOGETHER_API_KEY": ${api key here, which I will give to you},
    }
},

Then you can chat with the chatbot. Let me know if you have issues doing this.

However, it's pretty basic. We want it to sound more like our client. We have already collected a few example conversations in training_data/conversations.json.

# Goals
1. **Improve Client Personality Emulation**  
   Use DSPy’s KNNFewShot optimizer (https://dspy.ai/learn/optimization/optimizers/) to make the chatbot’s responses reflect our client’s voice more authentically, based on examples in `conversations.json`.

2. **Incorporate Context Awareness**  
   Introduce context awareness in a way that makes the chatbot more responsive to the timing and circumstances of each interaction. Examples might include awareness of the current time or the duration of a conversation.

3. **Topic Filtering**  
   Ensure the chatbot avoids discussing specific topics that may not be suitable. For this exercise, keep responses free of mentions of social media platforms (except OnlyFans) and interactions suggesting in-person meetings with fans.

4. **Further Product Enhancements**  
   Identify and implement an additional enhancement that you believe would improve the product experience.

The first goal is probably the hardest, but I want it done first and it will be what I look at closest. The things I'm looking for are 1. Can you quickly learn a new framework/new technology 2. How do you think about product improvements 2. 
How do you think about implementing these product improvements using dspy

**Note**: Avoid spending time on extensive prompt engineering. At Whisper, we value modular and maintainable code, and we prefer optimizations within DSPy itself rather than large, static prompts. Also, to see the actual prompts dspy is generating, uncomment the lm.inspect_history(n=1) line in `chat_interface.py`.

Please leave comments or notes on your thought process and what you built in a separate README file for me to take a look at.

I am expecting you to work on this for 2-3 hours. You can work on it longer if you'd like, just let me know how long you end up working on it.

Good luck!