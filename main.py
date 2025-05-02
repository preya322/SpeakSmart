import eel
import subprocess
import time
from engine.features import *
from engine.command import *

def start():
    eel.init('www')
    playAssistantSound()
    eel.start("index.html", mode=None, host='localhost', block=False)
    time.sleep(2)
    subprocess.Popen([
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--app=http://localhost:8000/index.html"
    ])
    eel.sleep(10**6)

if __name__ == "__main__":
    start()
