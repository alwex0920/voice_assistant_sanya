import json
import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel
from fuzzywuzzy import fuzz
import time
import platform
import sys, webbrowser, colorama, datetime, tts, os

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
        url = f'https://www.google.com/search?q={" ".join(text)}'
        tts.va_speak(f'Ищу в интернете: {" ".join(text)}')
        webbrowser.open(url)
    # Слушание
    def listen(self):
        print("Я вас слушаю...")
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.rec.Result())
                if answer["text"]:
                    yield answer["text"]
    # Распознование речи
    def recognize(self):
        for input_text in self.listen():
            co = open("commands.json", "r")
            comm = co.read()
            command = json.loads(comm)
            input_text = input_text.lower()
            if any(i in command["commands"][0:][0] for i in input_text.split()) and command['action']['type'] == 'shell':
                os.system(command["commands"][0:]["action"]["input"])
            elif any(i in command["commands"][0:][0] for i in input_text.split()) and command['action']['type'] == 'speak':
                now = datetime.datetime.now()
                tts.va_speak(command["commands"][0:]["action"]["input"])
            elif any(i in command["commands"][0:][0] for i in input_text.split()) and command['action']['type'] == 'google':
                self.google(command["commands"][0:]["action"]["input"].split()[1:])
            elif any(i in command["commands"][0:][0] for i in input_text.split()) and command['action']['type'] == 'open_file':
                os.startfile(command["commands"][0:]["action"]["input"])
            else:
                print("Ваша команда не распознана")

if __name__ == '__main__':
    registr()
