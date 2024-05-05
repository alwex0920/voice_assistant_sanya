import json
import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel
from fuzzywuzzy import fuzz
import time
import platform
import sys, webbrowser, colorama, datetime, tts, os
import g4f

def registr():
    with open("rg.json", "r+") as f:
        registr = json.load(f)
        print("Reading file...")
        time.sleep(2)
        if registr['reg'] == "yes":
            print("Success! Starting...")
            f.close()
            Helper().recognize()
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
            Helper().recognize()

class Helper():
    def __init__(self):
        SetLogLevel(-1)
        model = Model("./vosk-model-small-ru-0.22")
        self.rec = KaldiRecognizer(model, 16000)
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16, channels=1,
                        rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()
    # Поиск
    def google(self, text):
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            stream=True
        )
        for message in response:
            print(message, flush=True, end='')
    # Слушание
    def listen(self):
        print(".")
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.rec.Result())
                if answer["text"]:
                    yield answer["text"]
    # Распознование речи
    def recognize(self):
        for input_text in self.listen():
            co = open("commands.json", "r", encoding="utf8")
            comm = co.read()
            command = json.loads(comm)
            input_text = input_text.lower()
            sanya = ["саня", "санёк", "сандаль", "александр"]
            if any(i in sanya for i in input_text.split()):
                tts.va_speak("Слушаю вас сэр")
                for input_text in self.listen():
                    if any(i in command["commands"][0]["keywords"] for i in input_text.split()):
                        os.system(command["commands"][0]["action"]["input"])
                    elif any(i in command["commands"][1]["keywords"] for i in input_text.split()):
                        now = datetime.datetime.now()
                        tts.va_speak(command["commands"][1]["action"]["input"])
                    elif any(i in command["commands"][2]["keywords"] for i in input_text.split()):
                        self.google(command["commands"][2]["action"]["input"].split()[1:])
                    elif any(i in command["commands"][3]["keywords"] for i in input_text.split()):
                        os.startfile(command["commands"][3]["action"]["input"])
                    else:
                        print(input_text)
            else:
                print(input_text)

if __name__ == '__main__':
    registr()
