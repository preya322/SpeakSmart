from engine.Model import FirstLayerDMM
from engine.RealtimeSearchEngine import RealtimeSearchEngine
from engine.Automation import Automation
from engine.SpeechToText import SpeechRecognition
from engine.ChatBot import ChatBot
from engine.TextToSpeech import TextToSpeech
from engine.ImageGeneration import main
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

Username = "Vedansh"
Assistantname = "Alera"
DefaultMessages = f"""{Username}: Hello {Assistantname}, How are you?
{Assistantname}: Welcome {Username}, I am doing well, How may I help you?"""
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChat():
    File = open("Data/Chatlog.json", "r", encoding="utf-8")
    if len(File.read()) < 5:
        with open("Database.data", "w", encoding="utf-8") as file:
            file.write("")
        with open("Response.data", "w", encoding="utf-8") as file:
            file.write(DefaultMessages)

def ReadChatLogJson():
    with open("Data/Chatlog.json", "r", encoding="utf-8") as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", Username)
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname)

    with open("Database.data", "w", encoding="utf-8") as file:
        file.write(formatted_chatlog)

def ShowChatsOnGUI():
    File = open("Database.data", "r", encoding="utf-8")
    Data = File.read()
    if len(str(Data)) > 0:
        lines = Data.split('\n')
        result = "\n".join(lines)
        File.close()
        File = open("Response.data", "w", encoding="utf-8")
        File.write(result)
        File.close()

def InitialExecution():
    # SetMicrophoneStatus("False")
    # ShowTextToScreen("")
    ShowDefaultChatIfNoChat()
    ChatLogIntegration()
    ShowChatsOnGUI()

def MainExecution(Query: str):
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    # SetAssistantStatus("Listening")
    # Query = SpeechRecognition()
    # Query = "generate image of Monkey D. Luffy , how are you and write a leave application"
    # ShowTextToScreen(f"{Username}: {Query}")
    # SetAssistantStatus("Thinking")
    Decision = FirstLayerDMM(Query)

    print("")
    print(f"Decision: {Decision}")
    print("")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])

    Mergered_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True
    
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True
    
    if ImageExecution == True:
        with open("Frontend/Files/ImageGeneration.data", "w") as file:
            file.write(f"{ImageGenerationQuery.replace('generate image ', '')}, True")
        
        try:
            main()
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")
    
    if G and R:
        # SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(Mergered_query)
        # ShowTextToScreen(f"{Assistantname}: {Answer}")
        # SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
        return True
    
    else:
        for Queries in Decision:
            if "general" in Queries:
                # SetAssistantStatus("Thinking...")
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryFinal)
                # ShowTextToScreen(f"{Assistantname}: {Answer}")
                # SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            
            elif "realtime" in Queries:
                # SetAssistantStatus("Searching...")
                QueryFinal = Queries.replace("realtime ", "")
                Answer = RealtimeSearchEngine(QueryFinal)
                # ShowTextToScreen(f"{Assistantname}: {Answer}")
                # SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryFinal)
                # ShowTextToScreen(f"{Assistantname}: {Answer}")
                # SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                # SetAssistantStatus("Answering...")
                os._exit()



def FirstThread():
    while True:
        CurrentStatus =  False #GetMicrophoneStatus()

        if CurrentStatus == True:
            MainExecution()

def SecondThread():
    # GraphicalUserInterface()
    pass

if __name__ == "__main__":
    # thread2 = threading.Thread(target=FirstThread, daemon=True)
    # thread2.start()
    # SecondThread()
    MainExecution("Can you play let her go for me?")