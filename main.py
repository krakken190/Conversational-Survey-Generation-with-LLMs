import openai

# Set up your OpenAI API key
openai.api_key = 'sk-4L'

# User Management
user_responses = []


def capture_user_response(response):
    user_responses.append(response)


# Jailbreak Prevention function
def check_for_profanity(text):
    profane_words = [
        "expletive1",
        "expletive2",
        "inappropriate_word",
        "offensive_term",
        "vulgar_phrase",
        "offensive_language",
        "curse_word1",
        "curse_word2",
        "profanity3",
        "obscene_term",
        "vulgar_expression",
        "offensive_slang",
        "swear_word1",
        "swear_word2",
        # Add more profane words as needed
    ]

    # Converting the input text to lowercase for case-insensitive matching
    lower_text = text.lower()

    for word in profane_words:
        if word in lower_text:
            return True

    return False


def filter_unsafe_content(output):
    if check_for_profanity(output):
        print("AI: We apologize, but we cannot display content that may be offensive.")
        print("AI: Let's head back to the survey. Could you share your recent experiences with our website?")
        return None
    else:
        return output


intro_prompt = ("Hello! We're conducting a survey to improve our e-commerce website."
                "Could you share your recent experiences with our website?")

print(intro_prompt)

# Conversational Loop
while True:
    # User Input
    user_input = input("User: ")
    capture_user_response(user_input)

    if user_input.lower() == "exit":
        print("AI: I'm sorry if I couldn't assist you further. "
              "If you have any other questions or need assistance in the future, "
              "feel free to ask. Have a great day!")
        break

    # Here AI Generates Follow-up Question
    prompt_follow_up = f"User said: '{user_responses[-2] if len(user_responses) >= 2 else user_responses[-1]}'. Generate a follow-up question."
    response_follow_up = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{intro_prompt}\nUser: {user_responses[-2] if len(user_responses) >= 2 else user_responses[-1]}"},
            {"role": "assistant", "content": "Assistant:"},
        ],
        temperature=0.7,
        max_tokens=150
    )

    follow_up_question = response_follow_up["choices"][0]["message"]["content"].strip()

    follow_up_question = filter_unsafe_content(follow_up_question)

    if follow_up_question is None:
        continue

    print("AI: " + follow_up_question)

    # User Input
    user_input = input("User: ")
    capture_user_response(user_input)

    if user_input.lower() == "exit":
        print("AI: I'm sorry if I couldn't assist you further. "
              "If you have any other questions or need assistance in the future, "
              "feel free to ask. Have a great day!")
        break

    # Here AI Generates Survey Question
    prompt_survey = f"User said: '{user_responses[-1]}'. Generate a survey question."
    response_survey = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{intro_prompt}\nUser: {user_responses[-1]}"},
            {"role": "assistant", "content": "Assistant:"},
        ],
        temperature=0.7,
        max_tokens=150
    )

    survey_question = response_survey["choices"][0]["message"]["content"].strip()

    # Applying Jailbreak Prevention to Survey Question
    survey_question = filter_unsafe_content(survey_question)

    if survey_question is None:
        continue

    print("AI: " + survey_question)

    if user_input.lower() == "exit":
        print(
            "AI: I'm sorry if I couldn't assist you further. "
            "If you have any other questions or need assistance in the future, feel free to ask. Have a great day!")
        break
