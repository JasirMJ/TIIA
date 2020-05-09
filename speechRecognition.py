import requests
import speech_recognition as sr  # recognise speech
import random
from time import ctime  # get time details
import webbrowser  # open browser
import time
import pyttsx3
from Tiia.config import *


def engine_speak(audioString):
    print(audioString)

    engine = pyttsx3.init()
    # rate = engine.getProperty('rate')
    # engine.setProperty('rate', rate - 20)

    # volume = engine.getProperty('volume')
    # voice = engine.getProperty('voice')
    # rate = engine.getProperty('rate')
    # volume = engine.getProperty('volume')
    # voices = engine.getProperty('voices')

    engine.say(audioString)
    engine.runAndWait()

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


r = sr.Recognizer()  # initialise a recogniser
# main

# listen for audio and convert it to text:
def record_audio(ask=""):
    with sr.Microphone() as source:  # microphone as source
        if ask:
            engine_speak(ask)

        audio = r.listen(source, 5, 5)  # listen for the audio via source
        print("Done Listening")
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text

        except sr.UnknownValueError:  # error: recognizer does not understand
            print(sr.UnknownValueError)
            # engine_speak('I did not get that')
        except sr.RequestError:
            engine_speak('Sorry, the service is down')  # error: recognizer is not connected
        print(">>", voice_data.lower())  # print what user said
        return voice_data.lower()

def voiceMessage(yourmessage,message):
    API_ENDPOINT = URL+"detect/"

    print("You >",yourmessage)
    print("Bot >",message)

    data = {
        "bot": message,
        "you": yourmessage,
        KEY:"voice"
    }
    try:
        r = requests.post(url=API_ENDPOINT, data=data)
    except Exception as e:
        print("Please run your django server")
        engine_speak("Please run your django server")

def respond(voice_data):

    if there_exists(["train"]):
        message = "Next train is shornour nilamboor road passenger"
        print(MESSAGE, " : ", message)
        engine_speak(message)
        voiceMessage(voice_data,message)
        message = "bye the by Where you want to go? "
        # engine_speak(message)
        voiceMessage("",message)
        while True:
            print("Recording")
            voice_data = record_audio()
            print("Done")
            print("Voice>", voice_data)
            # if there_exists(["miyami"]):
            if "china" in voice_data:
                message="Ok its will arrive on third platform"
                # engine_speak(message)
                voiceMessage(voice_data,message)
                break
            elif "washington" in voice_data:
                message="There is no train to washington"
                # engine_speak(message)
                voiceMessage(voice_data,message)
                break
            elif "china" in voice_data:
                message="Sorry.. you are late, Its gone"
                # engine_speak(message)
                voiceMessage(voice_data,message)
                break
            elif "bye" in voice_data:
                message="ok have a nice day"
                # engine_speak(message)
                voiceMessage(voice_data,message)
                break
            elif "exit" in voice_data:
                message = "ok have a nice day"
                # engine_speak(message)
                voiceMessage(voice_data, message)
                break
            else:
                message="Sorry.. I dont know"
                # engine_speak(message)
                voiceMessage(voice_data,message)
                break




    #greeting
    if there_exists(['hey', 'hi', 'hello']):
        messages = ["hey, how can I help you" , "hey, what's up?",
                     "I'm listening" , "how can I help you?" ,
                     "hello" ]
        message = messages[random.randint(0, len(messages) - 1)]
        voiceMessage(voice_data,message)
        # engine_speak(message)

    #think
    if there_exists(["What are you thinking", "think", "thinking"]):
        messages = [
            "Im thinking you are brilliant",
            "Noting, you are awsome thats it",
        ]

        message = messages[random.randint(0, len(messages) - 1)]
        voiceMessage(voice_data, message)
        # engine_speak(message)
        time.sleep(3)
        voiceMessage("", "")
        # exit()

    if there_exists(["who are you"]):
        messages = ["I am Tiia, a prototype developed by Ruksana , Safla , Ulfath and Vibanjika" ,
                    "Ruksana , Safla , Ulfath and Vibanjika they developed me as a prototype",
                    ]
        message = messages[random.randint(0, len(messages) - 1)]
        voiceMessage(voice_data,message)

    if there_exists(['what you do']):
        message = "I can help human beings in several ways, i have the functionality to show adverticements relavent to you"
        voiceMessage(voice_data,message)
        # engine_speak(message)


    # 2: name
    if there_exists(["what is your name", "what's your name", "tell me your name","name"]):
        messages = [
            "Tiia my name ",
            "Tiia",
        ]

        message = messages[random.randint(0, len(messages) - 1)]
        # engine_speak(message)
        voiceMessage(voice_data,message)


    # greeting
    if there_exists(["how are you"]):
        # engine_speak("I'm very well, thanks for asking " )
        voiceMessage(voice_data, "I'm very well, thanks for asking " )

    #search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        # engine_speak("Here is what I found for" + search_term + "on google")
        voiceMessage(voice_data, "Here is what I found for" + search_term + "on google")

    # search youtube
    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        # engine_speak("Here is what I found for " + search_term + "on youtube")
        voiceMessage(voice_data, "Here is what I found for " + search_term + "on youtube")

    if there_exists(["price of"]):
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        # engine_speak("Here is what I found for " + search_term + " on google")
        voiceMessage(voice_data, "Here is what I found for " + search_term + " on google")


    if there_exists(["exit", "quit", "goodbye","bye"]):
        message="bye, have a nice day"
        voiceMessage(voice_data, message)
        # engine_speak(message)
        time.sleep(3)
        voiceMessage("", "")

    if there_exists(["goodnight","good night"]):
        message="Good night ,  sweet dreams"
        voiceMessage(voice_data, message)

        # engine_speak(message)
        time.sleep(3)
        voiceMessage("", "")
        # exit()


time.sleep(1)


engine = pyttsx3.init()
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)
engine_speak("Hi, i can assist you,")
while (1):
    print("Recording")
    voice_data = record_audio()  # get the voice input
    print("Done")
    print("Q:", voice_data)
    respond(voice_data)  # respond
