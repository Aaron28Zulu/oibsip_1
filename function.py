import os, os.path
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import datetime
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
import requests
import Joking

SCOPES = ["https://www.googleapis.com/auth/calendar"]
MONTHS = list(calendar.month_name)
DAYS = list(calendar.day_name)
DAY_EXTENSIONS = ["st", "nd", "rd"]


# WEATHER VARs

def get_weather(city: str):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = open('weather_api_key.txt', 'r').read()
    CITY = city

    url = BASE_URL + "q=" + CITY + "&appid=" + API_KEY

    response = requests.get(url).json()


    def temp_converter(kelvin):
        celcius = kelvin - 273.15
        fahrenheit = celcius * (9/5) + 32
        return celcius, fahrenheit


    temp_kelvin = response['main']['temp']
    temp_celcius, temp_fahrenheit = temp_converter(temp_kelvin)

    feels_like_kelvin = response['main']['feels_like']
    feels_like_celcius, feels_like_fahrenheit = temp_converter(feels_like_kelvin)

    description = response['weather'][0]['description']
    sunrise_time = datetime.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = datetime.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])


    temperature_desc = f"The city {CITY} is having a {description}, with Temperature {temp_celcius:.2f}°C or {temp_fahrenheit:.2f}°F"


    return temperature_desc


def get_joke():
    joke = Joking.random_joke()

    return joke


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def record_audio():
    """
    Records audio from mic sourse and output it as text
    """
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
    """
    Displays a summary of the argument(text) provided, summary generated from wikipedia
    """
    try:
        results = wk.summary(text, 2)
        print(results)
        return results
    except Exception as e:
        print("Exception error: " + str(e))


def authenticate_calendar():
    """Authenticate google api"""
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
    """Displays events saved on google calendar. Take two arguments, number of events to dispaly and service from google
    """
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

                