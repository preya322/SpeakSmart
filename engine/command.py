import os
# import speech_recognition as sr
import eel
import time
from engine.TextToSpeech import TextToSpeech
from engine.SpeechToText import SpeechRecognition
from engine.QueryHandling import MainExecution

# def speak(text):
#     text = str(text).replace("`", "").replace("'", "")
#     eel.DisplayMessage(text)
#     os.system(f"say -r 125 {text}")
#     eel.receiverText(text)

# def takeCommand():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         eel.DisplayMessage("Listening...")
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source)
#         try:
#             audio = r.listen(source, timeout=20, phrase_time_limit=15)
#             print("Recognizing...")
#             eel.DisplayMessage("Recognizing...")
#             query = r.recognize_google(audio, language="en-in")
#             eel.DisplayMessage(query)
#             print(f"User said: {query}")
#             time.sleep(5)
#         except sr.WaitTimeoutError:
#             print("Listening timeout, please try again.")
#             return ""
#         except sr.UnknownValueError:
#             print("Sorry, I didn't understand that.")
#             return ""
#         except sr.RequestError as e:
#             print(f"Request error from Google Speech Recognition: {e}")
#             return ""
#     return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = SpeechRecognition()
    else:
        query = message
        query = query.lower()
        eel.DisplayMessage(query)
    print(query)
    eel.senderText(query)
    query = query.lower()
    try:
        if "send message" in query:
            from engine.features import findContact, telegram
            message = ""
            api_id, api_hash = findContact(query.repalce(".", ""))
            if api_id != None and api_hash != None:
                if "send message" in query:
                    message = 'message'
                    TextToSpeech("what message to send")
                    query = SpeechRecognition()
                telegram(api_id, api_hash, query)
        elif "generate" in query and "slides" in query:
            from engine.helper import remove_words
            words_to_remove = ['create', 'generate', 'on', 'slides', '']
            result = remove_words(query, words_to_remove)
            result = result.split()
            total_slide = result[0]
            topic = " ".join(result[1:]).capitalize()
            from engine.features import presentation
            presentation(topic=topic, num=total_slide)
        elif "generate" in query and "short story" in query:
            from engine.helper import remove_words, textToTime
            words_to_remove = ['create', 'generate', 'on', 'short', 'story', 'a', '']
            result = remove_words(query, words_to_remove)
            from engine.ShortVideoGeneration import ShortVideo
            ShortVideo(result.capitalize())
        elif "set reminder" in query:
            from engine.helper import remove_words, textToTime
            words_to_remove = ["set", "reminder", "on", "at", "for"]
            result = remove_words(query, words_to_remove)
            reminder_inputs = textToTime(result)
            from engine.SetReminder import reminder
            reminder(reminder_inputs[1], reminder_inputs[0])
        elif "take a pic of me" in query:
            from engine.features import takePic
            takePic()
        # elif "generate an image of" in query:
        #     query = query.replace("generate an image of", "")
        #     from engine.features import generateImage
        #     generateImage(query)
        else:
            MainExecution(query)
            
    except Exception as e:
        print(f"Error: {e}")
    eel.ShowHood()


if __name__ == "__main__":
    allCommands()
