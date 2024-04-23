import speech_recognition as sr
import pyttsx3
import wikipedia as wk
import time
from gtts import gTTS
import playsound
import pyjokes
import os, sys


# TODO: Have the Mic active and listening to user' feed
# TODO: Convert audio to text
# TODO: Check for key words in the generated text
# TODO: Have a dictionary of responses according to user queries
# TODO: Trigger response to user' query 



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

