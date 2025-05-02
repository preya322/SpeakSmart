from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values  # Load environment variables safely
from engine.TextToSpeech import TextToSpeech

# Load environment variables
env_vars = dotenv_values(".env")

# Username = env_vars.get("Usrename")
Username = "Vedansh"
# Assistantname = env_vars.get("Assistantname")
Assistantname = "Alera"
# GropAPIKey = env_vars.get("GropAPIKey")
GroqAPIKey = "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"

# Ensure GroqAPIKey is set
if not GroqAPIKey:
    raise ValueError("GroqAPIKey is missing! Ensure it's set in the .env file.")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# System message defining chatbot behavior
System = f"""Hello, I am {Username}. You are an advanced AI chatbot named {Assistantname} with real-time access to up-to-date internet information.
Provide answers in a professional manner with proper grammar, punctuation, and clarity.
Strictly answer questions based on provided data only.
"""

# Load or create chat log
chatlog_path = "Data/Chatlog.json"

try:
    with open(chatlog_path, "r") as f:
        messages = load(f)
except FileNotFoundError:
    messages = []
    with open(chatlog_path, "w") as f:
        dump(messages, f)


def GoogleSearch(query):
    """Performs a Google search and returns the top 5 results with titles and descriptions."""
    try:
        results = list(search(query, num_results=5))
        Answer = f"Search results for '{query}':\n[start]\n"
        for result in results:
            Answer += f"Title: {result.title}\nDescription: {result.description}\n\n"
        Answer += "[end]"
    except Exception as e:
        Answer = f"Error while searching: {str(e)}"
    return Answer


def AnswerModifier(answer):
    """Removes unnecessary empty lines from the answer."""
    return "\n".join(line for line in answer.split("\n") if line.strip())


SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]


def GetCurrentTime():
    """Generates a real-time timestamp for the chatbot."""
    now = datetime.datetime.now()
    return (
        f"Realtime Info:\n"
        f"Day: {now.strftime('%A')}, Date: {now.strftime('%d-%B-%Y')}, "
        f"Time: {now.strftime('%H:%M:%S')}.\n"
    )


def RealtimeSearchEngine(prompt):
    """Handles user queries using Google search results and Groq AI model."""
    global SystemChatBot, messages

    messages.append({"role": "user", "content": prompt})

    search_results = GoogleSearch(prompt)
    SystemChatBot.append({"role": "system", "content": search_results})
    TextToSpeech("Searching....")
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": GetCurrentTime()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True
    )

    Answer = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer)


if __name__ == "__main__":
    while True:
        prompt = input("Enter your query (or type 'exit' to quit): ").strip()
        if prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print(RealtimeSearchEngine(prompt))
