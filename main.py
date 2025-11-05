import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import requests
from openai import OpenAI
import os, threading, pygame
from gtts import gTTS

recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 180)  # Faster speech
engine.setProperty('volume', 1.0)
newsapi = ""  # News API Key 

def speak_old() :
    # engine.say("Yes Sir!")
    # engine.runAndWait()
        threading.Thread(target=lambda: (engine.say(), engine.runAndWait())).start()

def speak(text):
    def _speak():
        tts = gTTS(text=text, lang='en')
        tts.save("temp.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
        os.remove("temp.mp3")
    threading.Thread(target=_speak).start()

def aiProcess(command) :
    client = OpenAI( api_key = " ")  # OpenAI key 
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are a virtual assistant, skilled in explaining complex programming contents with creative flares. Give short responses please"},
            {"role":"user","content":command}
        ]
    )
    return completion.choices[0].message.content

music = {
        "love": "https://www.youtube.com/watch?v=CnEqrgMlWLQ",
        "mirza": "https://www.youtube.com/watch?v=3hq_DhGOzik&list=RD3hq_DhGOzik&start_radio=1",
        "millionaire": "https://www.youtube.com/watch?v=XO8wew38VM8&list=RDXO8wew38VM8&start_radio=1",
        "sarphira": "https://www.youtube.com/watch?v=ynQOrNd8Ri0&list=RDynQOrNd8Ri0&start_radio=1",
        "champion": "https://www.youtube.com/watch?v=J3gsv9q6brY&list=RDJ3gsv9q6brY&start_radio=1"}

def processCommand(c) :
    if "open google" in c.lower() :
        webbrowser.open("https://www.google.com")
        engine.say("Opening Google")
    elif "open facebook" in c.lower() :
        webbrowser.open("https://www.facebook.com")
        engine.say("Opening Facebook")
    elif "open youtube" in c.lower() :
        webbrowser.open("https://www.youtube.com")
        engine.say("Opening YouTube")
    elif "open github" in c.lower() :
        webbrowser.open("https://github.com/JawadkhanHakim")
        engine.say("Opening GitHub")
    elif "open linkedin" in c.lower() :
        webbrowser.open("https://www.linkedin.com/in/jawad-khan-hakim/")
        engine.say("Opening LinkedIn")
    elif "open spotify" in c.lower() :
        webbrowser.open("https://open.spotify.com/user/31unbnmi7deloctfum2fpnbvpvnm?si=2ab40eea8a1e4ef7")
        engine.say("Opening Spotify")
    elif c.lower().startswith("play ") :
        song = c.lower().split(" ")[1]
        link = music.get(song)
        engine.say(f"Playing {song}")
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parsh the JSON respons
            data = r.json()
            # Extract the articles
            articles = data.get('articles',[])
            # Print the headlines 
            for article in articles:
                engine.say(article['title'])
    else :
        # Let OpenAI handle this 
        output = aiProcess(c)
        engine.say(output)
        
if __name__ == "__main__" :
    engine.say("Initializing NOVA....")
    engine.runAndWait()
    while True :
        # Obtain audio from the microphone
        recognizer = sr.Recognizer()
        print("Recognizing...")
        try :
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                print("Listening....")
                audio = recognizer.listen(source, timeout = 3, phrase_time_limit = 3)
            word = recognizer.recognize_google(audio)
            if(word.lower() == "nova") :
                engine.say("Yes Jawad!")
                time.sleep(1.2)
                # Listen for user command
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    print("Nova Active....")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)  
                    print(command)
                    processCommand(command)
        except sr.WaitTimeoutError:
            continue
        except Exception as e :
            print("Error; {0}".format(e))
 