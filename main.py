import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import wikipedia
import pyttsx3
import requests
import json
import datetime
import webbrowser
import subprocess
import pygame
import pygame.camera
import speech_recognition as sr
from googletrans import Translator
import wolframalpha
from urllib import request, parse
import re

#impostazioni assistente vocale
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[1].id')

#inizializzo il traduttore
translator = Translator()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour >= 0 and hour < 6:
        print("Buona notte")
        speak("Buona notte")
    elif hour>=6 and hour<12:
        print("Buongiorno")
        speak("Buongiorno")
    elif hour>=12 and hour<18:
        print("Buon pomeriggio")
        speak("Buon pomeriggio")
    else:
        speak("Buona sera")
        print("Buona sera")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Sto ascoltando")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='it')
            print("user:", statement,"\n")

        except Exception as e:
            speak("Scusami non ho capito, prova a ripetere")
            return "None"
        return statement


if __name__ == "__main__":

    print("Caricamente del tuo personale assistente DIANA")
    speak("Caricamento del tuo personale assistente DIANA")
    wishMe()

    while True:
        speak ("Dimmi come posso esserti utile?")
        statement = takeCommand().lower()

        if statement == 0:
            continue

        if "arrivederci" in statement or "ok ciao" in statement or "stop" in statement:
            speak('Il tuo personale assistente DIANA si sta spegnendo, a dopo')
            print('Il tuo personale assistente DIANA si sta spegnendo, a dopo')
            break
        elif 'wikipedia' in statement:
            statement = statement.replace("wikipedia", "")
            wikipedia.set_lang("it")
            speak('Cercando su Wikipedia ', statement)
            results = wikipedia.summary(statement, sentences=3)
            speak("Secondo Wikipedia")
            print(results)
            speak(results)

        elif 'ciao' in statement:
            print("È un piacere ascoltarti")
            speak("È un piacere ascoltarti")

        elif 'apri google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome è aperto")
            time.sleep(5)

        elif 'apri gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("GMail è aperto")
            time.sleep(5)

        elif 'apri youtube' in statement:
            webbrowser.open_new_tab("youtube.com")
            speak("YouTube è aperto")
            time.sleep(5)

        elif 'youtube' in statement:
            statement = statement.replace("youtube", "")
            query_string = parse.urlencode({'search_query': statement})
            html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
            # print(html_content.read().decode())
            search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
            webbrowser.open_new_tab('https://www.youtube.com/watch?v=' + search_results[0])

        elif 'ora' in statement or 'ore' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print("Sono le ", strTime)
            speak("Sono le ",strTime)

        elif 'chi sei' in statement or 'cosa puoi fare' in statement:
            speak(
                'Sono DIANA versione 1 punto 0, il tuo assistente personale. Sono programmata per eseguire funzioni minori per esempio, aprire youtube, google, gmail, cercare su wikipedia e dire l\'ora!')

        elif "chi ti ha fatto" in statement or "chi ti ha creato" in statement:
            speak("Sono stata creata da leo micida")
            print("Sono stata creata da leo micida")

        elif 'cerca' in statement:
            statement = statement.replace("cerca", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'attiva mysql' in statement:
            print("Vuoi attivare MySQL?")
            speak("Vuoi attivare MySQL?")

        else:
            question = translator.translate(statement, dest='en', source='it').text
            print(question)
            app_id = "HRV7K7-YHYG3AT6X9"
            client = wolframalpha.Client(app_id)
            try:
                res = client.query(question)
                answer = next(res.results).text
                answer = translator.translate(answer, dest='it', source='en').text
                print(answer)
                speak(answer)
            except Exception as e:
                print("Non penso di aver capito bene")
                speak("Non penso di aver capito bene")
