import speech_recognition as sr
import os
import tts
import time
import pyautogui
import citata
import json
import platform

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(".")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "Не могу получить доступ к сервису распознавания речи"

def assistant():
    input_text = recognize_speech()
    print(input_text)
    exec(open("commands.txt", "r+").read())

def main():
    while True:
        voice = recognize_speech()
        print(voice)
        if "Саня" or "саня" in voice:
            tts.va_speak("Слушаю вас сэр")
            assistant()
        else:
            print(voice)

def registr():
    with open("rg.json", "r+") as f:
        registr = json.load(f)
        print("Reading file...")
        time.sleep(3)
        if registr['reg'] == "yes":
            print("Success! Starting...")
            f.close()
            tts.va_speak("Чем могу помочь?")
            main()
        if registr['reg'] == "no" or "":
            print("Make sure that you have set the voice(Убедитесь что вы установили голос)")
            comp = input("Enter the user name: ")
            windows = platform.platform()
            f.close()
            freg = open("rg.json", "w")
            data = {
                "reg": "yes",
                "name": comp,
                "win": windows
            }
            json.dump(data, freg)
            freg.close()
            print("Starting...")
            tts.va_speak("Здраствуйте, я ваш голосовой помощник Саня.")
            tts.va_speak("Чем могу помочь?")
            main()

registr()
