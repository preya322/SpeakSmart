import re
from time import strptime
import datetime
# from engine.config import ASSISTANT_NAME

def extract_yt_term(command: str):
    # Define a regular expression pattern t cature the song name
    pattern = r"play\s+(.*?)\s+on\s+youtube"

    # Use re.searchto find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)

    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None

def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)
    return result_string


from datetime import datetime

def convert24(time):
    # Convert 12-hour format to 24-hour format
    t = datetime.strptime(time, '%I:%M%p')  # Correct format
    return t.strftime('%H:%M')

def textToTime(query: str):
    query_listed = query.split()
    print(query_listed)
    # Extract date, month, and time
    date = query_listed[0].replace("th", "").replace("nd", "").replace("st", "").replace("rd", "")
    month = datetime.strptime(query_listed[1], '%B').month  # Full month name
    time = convert24(query_listed[2]+query_listed[3].replace(".", ""))  # Fixed function call

    # Get the current year
    year = datetime.today().year  

    # Format into "YYYY-MM-DD HH:MM"
    return [f"{year}-{month:02d}-{int(date):02d} {time}", " ".join(query_listed[4:])]

def remove_words(sentence, words_to_remove):
    return " ".join([word for word in sentence.split() if word.lower() not in words_to_remove])

if __name__ == "__main__":
    input_string = "set reminder on 7th march at 12:15 a.m. for project presentation"
    words_to_remove = ["set", "reminder", "on", "at", "for"]
    
    result = remove_words(input_string, words_to_remove)
    print(result)
    print(textToTime(result))

