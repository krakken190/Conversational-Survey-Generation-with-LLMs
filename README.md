Link for project being used:- https://drive.google.com/file/d/1iKiQO2lZFZbh07Ktv_wPno256bi2dUMk/view?usp=sharing

# *Conversational-Survey-Interview-Generation-with-LLMs*

# 1. Introduction
## 1.1 Purpose
The purpose of this conversational survey is to collect user feedback to improve
e-commerce websites. The survey is designed to engage users in a dynamic conversation
with an AI language model (LLM).
## 1.2 Overview
The conversational survey employs OpenAI's GPT-3.5-turbo language model to generate
survey questions and follow-up questions based on user input. The interaction is structured
to simulate a natural conversation, enhancing user engagement.
# 2. Prompt Design
## 2.1 Introduction and Purpose
The conversation begins with a friendly introduction, explaining the purpose of the survey.
Users are encouraged to share their recent experiences and thoughts on the e-commerce
website.
## 2.2 Conversational Loop
● User Input Prompt: Users provide input about their experience.
● AI Generates Survey Question: The LLM generates a survey question based on the
user input.
● Jailbreak Prevention: A profanity check is applied to filter out offensive content.
● Display Survey Question: If safe, the generated question is displayed to the user.
● User Responds: The loop continues with the user providing feedback.
## 2.3 Exiting the Loop
The loop can be terminated when the user inputs "exit," indicating the end of the survey.
# 3. LLM Integration Strategy
## 3.1 User Responses
User responses are captured and maintained in a list (user_responses) to provide context
for generating follow-up questions.
## 3.2 Jailbreak Prevention
A profanity check is implemented to filter out offensive content from both generated survey
questions and follow-up questions.
## 3.3 Conversational Flow
A dynamic conversational flow is established by maintaining a dialogue history between the
user and the AI. Each turn of the conversation is used as input for the LLM, creating a
context-aware interaction.
## 3.4 Dynamic Prompts
Prompts provided to the LLM are dynamically generated based on the user's input and the
context of the conversation.
# 4. Final Prompt Being Used
prompt = f"User said: '{user_input}'. Generate a survey question."
This prompt informs the LLM of the user's input and instructs it to generate a survey
question. The context of the conversation is maintained through the dialogue history
