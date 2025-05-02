import pygame
import random
import asyncio
import edge_tts
import os
import re
import eel
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-CA-LiamNeural")  # Default if not found

# Initialize pygame mixer once
pygame.mixer.init()

async def TextToAudioFile(text: str) -> None:
    """Convert text to an audio file using edge-tts."""
    file_path = "Data/speech.mp3"
    eel.DisplayMessage(text)
    eel.receiverText(text)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)

        communicate = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate="+13%")
        await communicate.save(file_path)
    
    except Exception as e:
        print(f"Error generating speech: {e}")

def TTS(Text, func=lambda r=None: True):
    """Handles playing the generated audio file."""
    try:
        asyncio.run(TextToAudioFile(Text))

        pygame.mixer.music.load("Data/speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if func() == False:
                break
            pygame.time.Clock().tick(10)
        
        return True

    except Exception as e:
        print(f"Error in TTS: {e}")
    
    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error in cleanup: {e}")

def split_text(text):
    """Splits text into sentences properly."""
    return re.split(r'(?<=[.!?])\s+', text)

def TextToSpeech(Text, func=lambda r=None: True):
    """Splits long text and ensures proper speech output."""
    sentences = split_text(Text)
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(sentences) > 4 and len(Text) > 250:
        TTS(" ".join(sentences[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)

if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the Text: "))
