from webbrowser import open as wb
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
from engine.TextToSpeech import TextToSpeech
import sqlite3

# Load environment variables
# env_vars = dotenv_values(".env")
# GroqAPIKey = env_vars.get("GroqAPIKey")
GroqAPIKey = "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"

# Define CSS classes for parsing specific elements in HTML content.
classes = [
    "zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", 
    "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", 
    "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", 
    "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

# Define user-agent for making web requests.
useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

SystemChatBot = [{"role": "system", "content": "Hello, I am Vedansh, a content writer. I create content like letters, codes, applications, essays, notes, songs, poems, etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

# GoogleSearch("Elon Musk")

def Content(Topic):
    def OpenNotepad(File):
        subprocess.Popen(["open", "-a", "TextEdit", File])  # macOS uses TextEdit

    def ContentWriterAI(prompt: str):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    os.makedirs("Data", exist_ok=True)  # Ensure the directory exists
    file_path = f"Data/{Topic.lower().replace(' ', '')}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(file_path)

# Content("Leave Application")

def YouTubeSearch(Topic):
    url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app):
    try:
        app = app.replace(".", "")
        con = sqlite3.connect("jarvis.db")
        cursor = con.cursor()
        sql_query = "SELECT path FROM sys_command WHERE name IN (?)"
        cursor.execute(sql_query, (app,))
        results = cursor.fetchall()
        if len(results) != 0:
            TextToSpeech(f"Opening {app}...")
            subprocess.call(["open", results[0][0]])
        elif len(results) == 0:
            sql_query = "SELECT path FROM web_command WHERE name IN (?)"
            cursor.execute(sql_query, (app,))
            results = cursor.fetchall()
            if len(results) != 0:
                TextToSpeech(f"Opening {app}...")
                wb.open(results[0][0])
            else:
                TextToSpeech(f"Opening {app}...")
                try:
                    os.system(f"open -a {app}")
                except:
                    TextToSpeech("Application not found...")
        con.close()
    except Exception as e:
        print(f"Error opening app: {e}")
        return False

def CloseApp(app):
    if "chrome" in app:
        pass  # Prevent accidental closing of Chrome
    else:
        try:
            subprocess.run(["pkill", app], check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Error: Could not close {app}. Maybe it's not running?")
            return False

def System(command):
    if command == "mute":
        keyboard.press_and_release("volume mute")
    elif command == "unmute":
        keyboard.press_and_release("volume mute")
    elif command == "volume up":
        keyboard.press_and_release("volume up")
    elif command == "volume down":
        keyboard.press_and_release("volume down")
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function Found for: {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands=commands):
        pass
    return True

if __name__ == "__main__":
    asyncio.run(Automation(["open terminal", "open Telegram", "play let her go", "content plaindrome program in python", "open pycharm ce"]))