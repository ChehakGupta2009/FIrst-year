#This is a chat-bot which answers the questions asked by the user.
import os

from groq import Groq

def chat_history():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: set the GROQ_API_KEY environment variable before starting the chatbot.")
        return

    client = Groq(api_key=api_key)
    history = [{
        "role": "system",
        "content": "Strictly give responses in English only. No other language allowed.",
    }]

    while True:
        try:
            user_prompt = input("user: ").strip()
        except (EOFError, KeyboardInterrupt):
            # Treat a closed input stream or Ctrl+C as a normal exit.
            print("\nChat ended.")
            break

        if user_prompt.upper() == "BYE":
            break

        history.append({"role": "user", "content": user_prompt})

        try:
            result = client.chat.completions.create(
                model="allam-2-7b",
                messages=history,
                temperature=1.0,
            )
            response = result.choices[0].message.content
        except Exception as error:
            # Keep the conversation running if the provider or network is unavailable.
            print(f"Chat request failed: {error}")
            history.pop()
            continue

        if not response:
            print("Chat request returned an empty response.")
            history.pop()
            continue

        print("bot:", response)
        history.append({"role": "assistant", "content": response})

chat_history()
