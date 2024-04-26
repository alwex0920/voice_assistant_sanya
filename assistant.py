import json
import pyaudio
from vosk import Model, KaldiRecognizer, SetLogLevel
from fuzzywuzzy import fuzz
import time
import platform
import sys, webbrowser, colorama, datetime, tts, random, os

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
    # Приветствие
    def hello(self):
        hello_list = ['привет', 'ку', 'приветствую', 'хелоу', 'дарова', 'здорово']
        tts.va_speak(random.choice(hello_list))
    def shutdown(self):
        tts.va_speak("Выключение компьютера")
        os.system('shutdown /s /t 1')
    # Открытие браузера
    def open_browser(self, task):
        links = {
            ('ютуб', 'ютюб'): 'https://youtube.com/',
            ('вк', 'вконтакте', 'контакт'): 'https:vk.com/feed',
            ('браузер', 'интернет', 'гугл'): 'https://google.com/',
            ('телеграм', 'телега', 'телегу'): 'https://https://web.telegram.org/',
        }
        j = 0
        if 'и' in task:
            task = task.replace('и', '').replace('  ', ' ')
        double_task = task.split()
        if j != len(double_task):
            for i in range(len(double_task)):
                for vals in links:
                    for word in vals:
                        if fuzz.ratio(word, double_task[i]) > 75:
                            webbrowser.open(links[vals])
                            tts.va_speak('Открываю ' + double_task[i])
                            j += 1
                            os.system('cls')
                            tts.va_speak("Я вас слушаю...")
                            break

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
            com = co.read()
            command = json.loads(com)
            for command in commands:
               if any(kw in input_text.lower() for kw in command["keywords"]):
                  ...
                  continue # чтобы не продолжало итерироваться и взяло первую подходящую команду
                  match command[1:][0]:
                    case "webbrowser":
                       tts.va_speak("Открываю")  # эти ответы тоже можно в джсонку засунуть
                       webbrowser.open(command[0][1])
                    case "shell":
                       os.system(command[1][1])
                    case "speak":
                       now = datetime.datetime.now()
                       tts.va_speak(command[2][1])
                    case "browser":
                       self.open_browser(command[3][1])
                    case "google":
                       self.google(command[4][1].split()[1:])
                   
if __name__ == '__main__':
    registr()
