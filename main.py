import os
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import speech_recognition as sr
import pyttsx3
import wikipedia as wk
import time
from gtts import gTTS
import playsound

# TODO: Have the Mic active and listening to user' feed
# TODO: Convert audio to text
# TODO: Check for key words in the generated text
# TODO: Have a dictionary of responses according to user queries
# TODO: Trigger response to user' query 

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def speak(text):
    tts = gTTS(text="OK! " + text, lang="en", slow=False)
    filename = "voice.mp3"
    tts.save(filename)

    playsound.playsound(filename)


def record_text():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        # Recognizer receive input 
        r.adjust_for_ambient_noise(mic, duration=0.2)
        
        # Capture user voice
        audio = r.listen(mic)
        myText = ""
        try:
            myText = r.recognize_google(audio) # Service to recognize audio (i.e google)
        except sr.RequestError as e:
            print(f"Could not request results: {e}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")
    return myText

def search_wiki(text):
    while True:
        try:
            if "search" in text:

                print("What should I look for...")

                userText = "llama model"

                results = wk.summary(userText, 2)
                
                print(results)


                speak(results)

                break

        except Exception as e:
            print("Exception error: " + str(e))


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


service = authenticate_calendar()

get_event(4, service=service)
