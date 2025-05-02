import os
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credential():
    creds = None

    if os.path.exists("CREDENTIALS/token.json"):
        creds = Credentials.from_authorized_user_file("CREDENTIALS/token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("CREDENTIALS/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("CREDENTIALS/token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def create_event_with_reminder(service, event, start_time_str, reminder_time_str):
    try:
        # Convert input times to datetime objects
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
        reminder_time = datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M")

        # Calculate the minutes between the start time and reminder time
        minutes_after_start = int((reminder_time - start_time).total_seconds() // 60)

        event = {
            "summary": f"{event}",
            "start": {
                "dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": (start_time.replace(hour=start_time.hour + 1)).strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                "timeZone": "Asia/Kolkata"
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": minutes_after_start},
                    {"method": "email", "minutes": minutes_after_start}
                ]
            }
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")
        os.system(f"open {created_event.get('htmlLink')}")
        print("Reminder Setted Successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def reminder(event, dateTime):
    from engine.TextToSpeech import TextToSpeech
    TextToSpeech("Setting Reminder....")
    creds = get_credential()
    service = build("calendar", "v3", credentials=creds)

    # User inputs
    # event = input("Enter event name: ")
    # start_time_str = input("Enter event start time (YYYY-MM-DD HH:MM): ")
    # reminder_time_str = input("Enter reminder time (YYYY-MM-DD HH:MM): ")
    start_time_str = dateTime
    reminder_time_str = dateTime

    create_event_with_reminder(service, event, start_time_str, reminder_time_str)
    TextToSpeech("Reminder setted Successfully....")

if __name__ == "__main__":
    reminder("Project Presentation", "2025-03-07 11:40")
