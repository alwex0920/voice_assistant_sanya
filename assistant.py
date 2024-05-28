import json
import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel
from fuzzywuzzy import fuzz
import time
import platform
import sys, webbrowser, colorama, datetime, tts, os
from g4f.client import Client

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
            tts.va_speak("Здраствуйте, я ваш голосовой помощник Александр можно Саня.")
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
    # Слушание
    def listen(self):
        print(".")
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.rec.Result())
                if answer["text"]:
                    yield answer["text"]

    def google(self, text):
        tts.va_speak("Подождите ваш запрос выполняется")
        txt = text
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Твоё имя - Александр, ты искусственный интеллект от Alwex Developer"}, {"role": "user", "content": txt}]
        )
        print(response.choices[0].message.content)
        tts.va_speak(response.choices[0].message.content)
        time.sleep(10)
        os.system("cls")
        self.recognize()
    def dialog(self):
        for input_text in self.listen():
            stop = ["стоп", "хватит", "достаточно", "довольно"]
            if any(i in stop for i in input_text.lower()):
                tts.va_speak("Рад был с вами поговорить!")
                self.recognize()
            else:
                client = Client()
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Твоё имя - Александр, ты искусственный интеллект от Alwex Developer"}, {"role": "user", "content": input_text.lower()}]
                )
                print(response.choices[0].message.content)
                tts.va_speak(response.choices[0].message.content)

    # Распознование речи
    def recognize(self):
        for input_text in self.listen():
            co = open("commands.json", "r", encoding="utf8")
            comm = co.read()
            command = json.loads(comm)
            input_text = input_text.lower()
            sanya = ["саня", "сане", "санёк", "сандаль", "александр"]
            if any(i in sanya for i in input_text.split()):
                tts.va_speak("Слушаю вас сэр")
                for input_text in self.listen():
                    if any(i in command["commands"][0]["keywords"] for i in input_text.split()):
                        os.system(command["commands"][0]["action"]["input"])
                    elif any(i in command["commands"][1]["keywords"] for i in input_text.split()):
                        now = datetime.datetime.now()
                        tts.va_speak("Сейчас " + str(now.hour)  + "часов" + str(now.minute) + "минут")
                    elif any(i in command["commands"][2]["keywords"] for i in input_text.split()):
                        self.google(input_text)
                    elif any(i in command["commands"][3]["keywords"] for i in input_text.split()):
                        self.dialog()
                    elif any(i in command["commands"][4]["keywords"] for i in input_text.split()):
                        os.startfile(command["commands"][4]["action"]["input"])
                    else:
                        self.google(input_text)
            else:
                print('')

if __name__ == '__main__':
    registr()
