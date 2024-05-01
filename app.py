import random
import sys
from function import *
from tags import *
from responses import *


import socket


def check_internet_connection():
    remote_server = "www.google.com"
    port = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((remote_server, port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()

def main():
    if check_internet_connection():

        print("Listening...")
        text = record_audio()

        # WAKE UP BOT
        for word in WAKE:
            wake_response = random.choice(wake_responses)
            if word in text:
                speak(wake_response)

                main()

        # NAME
        for phrase in NAME:
            name_response = random.choice(name_responses)
            if phrase == text:
                speak(name_response)

                main()

        # CAPABILITIES
        for phrase in CAPABILITIES:
            cap_response = random.choice(capability_responses)
            if phrase in text:
                speak(cap_response)

                main()

        # FAREWELL
        for phrase in FAREWELLS:
            farewell_response = random.choice(farewell_responses)
            if phrase in text:
                speak(farewell_response)

                print("Stopped Listening...")

                sys.exit()

        # TAKES NOTES
        for phrase in NOTE_STRS:
            if phrase == text:
                speak("What would you like me to note down?")
                note_text = record_audio()
                write_note(note_text)
                speak("I've made a note of that.")

                main()

        # WIKI SEARCH
        WIKIPEDIA_STRS = ["search", "wikipedia", "give insight", "summerize", "summerise"]
        for word in WIKIPEDIA_STRS:
            if word in text:
                speak("What would you like me to summerize?")
                text = record_audio()

                summarised_note = search_wiki(text)
                speak(summarised_note)

                main()

        # DATES
        DATE_STRS = ["what is the date today"]
        for phrase in DATE_STRS:
            if phrase in text:
                date = get_date()
                speak(date)

                main()

        # TELL JOKES
        for phrase in JOKES:
            if "joke" in text:
                joke = get_joke()
                speak(joke)

                main()

        #  WEATHER DATA
        for phrase in ["weather data", "weather forecast"]:
            if phrase in text:
                speak("You want the weather forecast for which city?")
                city = record_audio()
                if city is not None:
                    city_info = get_weather(city)
                    speak(city_info)
                else:
                    speak("Couldn't get the data. Kindly pass the command again")


while check_internet_connection():
    main()

speak("Can not sent request, please make sure you are online")
print("Internet is not connected.")
sys.exit()
