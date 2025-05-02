import os
import json
import datetime
from groq import Groq
from json import load, dump

# Load API Key securely from environment variables
GroqAPIKey = "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"
if not GroqAPIKey:
    raise ValueError("API key not found! Set GROQ_API_KEY in environment variables.")

client = Groq(api_key=GroqAPIKey)

# User Information
Username = "Vedansh"
Assistantname = "Alera"

# Path to chat log file
CHATLOG_FILE = "Data/Chatlog.json"

# Ensure Data directory exists
os.makedirs(os.path.dirname(CHATLOG_FILE), exist_ok=True)

# System prompt setup
System = f"""Hello, I am {Username}. You are an advanced AI chatbot named {Assistantname} with real-time internet access.
*** Do not tell time unless asked, do not talk too much, just answer the question. ***
*** Reply in only English, even if the question is in Hindi. ***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": System}]

def get_realtime_info() -> str:
    """Generates real-time date and time information."""
    current_time = datetime.datetime.now()
    return f"Please use this real-time information if needed:\n" \
           f"Day: {current_time.strftime('%A')}\n" \
           f"Date: {current_time.strftime('%d')}\n" \
           f"Month: {current_time.strftime('%B')}\n" \
           f"Year: {current_time.strftime('%Y')}\n" \
           f"Time: {current_time.strftime('%H:%M:%S')}.\n"

def modify_answer(answer: str) -> str:
    """Removes empty lines from chatbot's response."""
    return "\n".join(filter(None, answer.split("\n")))

def load_chat_log() -> list:
    """Loads chat log from file."""
    try:
        with open(CHATLOG_FILE, "r") as f:
            data = f.read()
            if data.strip():
                return json.loads(data)
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error occurred while loading chat log.")
        return []

def save_chat_log(messages: list) -> None:
    """Saves chat log to file."""
    with open(CHATLOG_FILE, "w") as f:
        json.dump(messages, f, indent=4)

def ChatBot(query: str) -> str:
    """Handles chatbot interaction by sending user queries and retrieving responses."""
    messages = load_chat_log()
    
    try:
        # Append user query
        messages.append({"role": "user", "content": query})

        # Get response from Groq AI
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": get_realtime_info()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        answer = ""

        for chunk in completion:
            content = chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
            answer += content

        answer = answer.replace("</s>", "")

        # Append AI response to chat log
        messages.append({"role": "assistant", "content": answer})

        # Save chat log
        save_chat_log(messages)

        return modify_answer(answer)
    
    except Exception as e:
        print(f"Error: {e}")

        # Reset chat log on failure
        save_chat_log([])
        
        return "An error occurred. Please try again."

if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        print(ChatBot(user_input))
