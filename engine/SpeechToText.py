from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables
env_vars = dotenv_values(".env")

InputLanguage = "en"

# Ensure Data directory exists
os.makedirs("Data", exist_ok=True)

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

with open("Data/Voice.html", "w") as f:
    f.write(HtmlCode)

current_dir = os.getcwd()
link = f"{current_dir}/Data/Voice.html"

chrome_option = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_option.add_argument(f"user-agent={user_agent}")
chrome_option.add_argument("--use-fake-ui-for-media-stream")
chrome_option.add_argument("--use-fake-device-for-media-stream")
chrome_option.add_argument("--headless")  # Removed for debugging
chrome_option.add_argument("--disable-gpu")  # Helps with stability on macOS
chrome_option.add_argument("--window-size=1920x1080")  # Ensures proper rendering

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_option)

TempDirPath = rf"{current_dir}/Frontend/Files"
os.makedirs(TempDirPath, exist_ok=True)

def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(Status)

def QueryModifier(Query: str):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "why", "where", "when", "which", "whose", "whom", "can you", "what's", "how's", "can you"]

    if any(word + " " in new_query for word in question_words):
        new_query = new_query.rstrip(".?!") + "?"
    else:
        new_query = new_query.rstrip(".?!") + "."

    return new_query.capitalize()

def UniversalTranslator(Text: str):
    try:
        return mt.translate(Text, "en", "auto").capitalize()
    except Exception as e:
        print("Translation error:", e)
        return Text.capitalize()

def SpeechRecognition():
    driver.get("file:///" + link)
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            Text = driver.find_element(By.ID, "output").text

            if Text:
                driver.find_element(By.ID, "end").click()
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    
    Text = SpeechRecognition()
    print(Text)
