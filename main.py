import os
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import tkinter as tk
import calendar
import speech_recognition as sr
import pyttsx3
import wikipedia as wk
import subprocess
import threading
from PIL import Image, ImageTk

# TODO: Have the Mic active and listening to user' feed
# TODO: Convert audio to text
# TODO: Check for key words in the generated text
# TODO: Have a dictionary of responses according to user queries
# TODO: Trigger response to user' query 

SCOPES = ["https://www.googleapis.com/auth/calendar"]
MONTHS = list(calendar.month_name)
DAYS = list(calendar.day_name)
DAY_EXTENSIONS = ["st", "nd", "rd"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        # Recognizer receive input 
        r.adjust_for_ambient_noise(mic, duration=0.2)
        
        # Capture user voice
        audio = r.listen(mic)
        r.adjust_for_ambient_noise(mic)
        said = " "

        try:
            said = r.recognize_google(audio) # Service to recognize audio (i.e google)
            print(said)
        except sr.RequestError as e:
            print(f"Could not request results: {e}".format(e))
        except sr.UnknownValueError:
            print("Unknown error")

        return said.lower()


def search_wiki(text):
    try:
        results = wk.summary(text, 2)
        print(results)
        return results
    except Exception as e:
        print("Exception error: " + str(e))
        icon.config(fg="black")


def authenticate_calendar():
    creds = None
    userFile = "token.json"

    if os.path.exists(userFile):
        creds = Credentials.from_authorized_user_file(userFile)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open(userFile, "w") as token:
            token.write(creds.to_json())


    service = build("calendar", "v3", credentials=creds)

    return service


def get_event(num_of_events, service):

    now = datetime.datetime.now().isoformat() + "Z"

    print(f"Getting the upcoming {num_of_events} events")

    event_result = service.events().list(calendarId="primary", 
                                         timeMin=now, 
                                         maxResults=num_of_events, 
                                         singleEvents=True, 
                                         orderBy="startTime").execute()
    events = event_result.get("items", [])

    if not events:
        print("No upoming events found! ")


    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))

        print(start, event["summary"])

service = authenticate_calendar() # To authenticate google calendar api


def get_date():
    today = datetime.date.today()
    return today


def write_note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as file:
        file.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def main():
    isBot_of = False
    WAKE = ["hey bot", "bot", "wake", "wake up"]

    while not isBot_of:
        print("Listening...")
        text = record_audio()

        if text is not None:
            icon.config(fg="green")
            
        else:
            icon.config(fg="black")

        # WAKE UP BOT
        for word in WAKE: 
            if word in text:
                speak("Hi, I'm Bot. How can I assist you?")
        
                text = record_audio() # Reinitilise mic to get new input

        # TAKES NOTES
        NOTE_STRS = ["make a note", "write this down", "remember this", "take notes"]
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("What would you like me to note down?")
                note_text = record_audio()
                write_note(note_text)
                speak("I've made a note of that.")

        # WIKI SEARCH
        WIKIPEDIA_STRS = ["search", "wikipedia", "give insight", "summerize", "summerise"]
        for word in WIKIPEDIA_STRS:
            if word in text:
                speak("What would you like me to summerize?")
                text = record_audio()

                summarised_note = search_wiki(text)
                speak(summarised_note)

        # DATES
        DATE_STRS = ["what is the date today"]
        for phrase in DATE_STRS:
            if phrase in text:
                date = get_date()
                speak(date)

#GUI
root = tk.Tk()
root.title("Bot Assistant")
root.minsize(width=300, height=300)
root.resizable(False, False)


gui_msg = tk.Message(root, text="Try saying", justify="center", pady=30)
gui_msg.grid(column=1, row=0)

icon = tk.Label(root, text="🔊", font=("Arial", 50, "bold"))
icon.grid(column=0, row=1)

msg = tk.Message(root, text="tell me a joke", justify="center")
msg.grid(column=1, row=1)

threading.Thread(target=main).start()

root.mainloop()