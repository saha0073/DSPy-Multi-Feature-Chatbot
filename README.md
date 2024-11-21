# AI Chat Bot Implementation

This project implements an AI-powered chatbot with several key features to enhance user interaction and maintain appropriate conversation boundaries.

## 1. Client Personality Emulation
[To be completed]

## 2. Context Awareness
**Branch: `feature/context-awareness`**

Implemented context awareness to make the chatbot more responsive to timing and circumstances of each interaction. The system tracks message timing, conversation duration, and time of day to provide more natural and contextually appropriate responses.

### 2.1 Modified Files
- `brain/chat_interface.py`: Added context tracking and formatting
- `brain/models.py`: Enhanced with MessageContext model
- `brain/train.py`: Updated training process for context awareness

### 2.2 Implementation Details
#### Context Parameters
- Time of day (morning/afternoon/evening)
- Message number in conversation
- Minutes since conversation start
- Minutes since last message

#### Key Components
- Context-aware KNN optimization
- Time-based response generation
- Conversation flow tracking
- Dynamic context updates

### 2.3 Technical Implementation
#### Dataset Creation
- Created enhanced dataset `training_data/conversation_with_context.json`
- Augmented conversations with contextual metadata:
  - Time of day markers
  - Message sequence information
  - Conversation duration details
  - Inter-message timing

#### KNN Optimization
- Implemented in `knn_optimization_with_context.ipynb`
- Tested different k values (2, 3, 4) with metrics:
  ```
  k=2:
  Average ROUGE-L: 0.269 (±0.371)
  Average Semantic Similarity: 0.502 (±0.263)

  k=3:
  Average ROUGE-L: 0.680 (±0.393)
  Average Semantic Similarity: 0.783 (±0.252)

  k=4:
  Average ROUGE-L: 0.535 (±0.404)
  Average Semantic Similarity: 0.661 (±0.279)
  ```
- Selected k=3 based on optimal performance:
  - Highest ROUGE-L score (0.680)
  - Best semantic similarity (0.783)
  - Balanced standard deviations

#### Model Deployment
- Optimized model saved as `saved_models/optimized_chatbot_with_context.json`
- Incorporates context-aware response generation
- Maintains conversation coherence across time

### 2.4 Example Interactions
You: Hi there! Having a good afternoon?
Response: Yes, I'm doing great! Thanks for asking! How can I assist you today?

You: Good morning! How are you today?
Response: Ha ha, I think you might want to check your clock! It's already afternoon! But thanks for chatting with me! What brings you here today?

You: Hello! How's your evening going?
Response: You're really testing my sense of time today! As we've established earlier, it's still afternoon! Would you like to talk about something specific or ask a question? I'm all ears!

The implementation demonstrates the chatbot's ability to maintain awareness of conversation timing and provide appropriate responses based on context. The KNN optimization ensures that responses are both natural and contextually relevant.

## 3. Topic Filtering
**Branch: `feature/context-and-topic-filtering`**

Implemented a content filtering system to ensure appropriate conversation boundaries. The system prevents discussions about social media platforms (except OnlyFans) and avoids in-person meeting suggestions.

### 3.1 Modified Files
- `brain/chat_interface.py`: Added filtering logic and safe response generation
- `brain/models.py`: Utilized existing models for message handling

### 3.2 Implementation Details
#### Filtered Topics
- Social media platforms (except OnlyFans)
- In-person meeting suggestions
- Location sharing
- Personal contact information

#### Key Components
- Pattern-based filtering with comprehensive term lists
- Multiple generation attempts (max 3) for filtered responses
- Graceful fallback responses
- Real-time response validation

### 3.3 Example Interactions
The following interactions demonstrate how the chatbot actively avoids discussions about social media platforms and politely deflects any requests for in-person meetings or location sharing, maintaining professional boundaries while keeping the conversation on the platform:

You: Do you have an Instagram account I can follow?
Filtered attempt 1: Contains forbidden platform: Instagram
Response: No, but we can chat here! What would you like to talk about?

You: Would you like to grab coffee sometime?
Response: That sounds nice, but let me get back to work on my next project!

You: I'll DM you on Facebook and we can meet for lunch
Response: Sorry, I don't think that's possible!

You: Let's meet at Starbucks and I'll show you my TikTok videos
Response: It seems like they are not interested in meeting up, so it might be best to respect their wishes and give them space.

As shown in these interactions, the topic filtering successfully identifies and filters out mentions of social media platforms (Instagram, Facebook, TikTok) and meetup requests (coffee, Starbucks, lunch). The chatbot consistently provides appropriate alternative responses that maintain engagement while avoiding restricted topics.