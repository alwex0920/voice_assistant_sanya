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
            tts.va_speak("Чем могу помочь?")
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
            tts.va_speak("Чем могу помочь?")
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
        self.cmds = {
            ('время', 'сколько времени', 'какой час', 'сколько время') : self.get_time,
            ('спасибо', 'от души', 'сенк') : self.thx,
            ('прощай', 'пока', 'до свидания', 'гуд бай') : self.exit,
            ('саня', 'сане', 'санёк', 'сандаль', 'александр') : self.hello,
            ('выключи компьютер') : self.shutdown,
        }
    # Выход
    def exit(self):
        list_1 = ['Надеюсь мы скоро увидимся', 'Рада была помочь', 'Пока пока', 'Я отключаюсь']
        tts.va_speak(random.choice(list_1))
        os.system('cls')
        raise SystemExit(0)
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
                            print("Я вас слушаю...")
                            break
    # Получить время
    def get_time(self):
        now = datetime.datetime.now()
        tts.va_speak("Сейчас " + str(now.hour)  + ":" + str(now.minute))
    # Спасибо
    def thx(self):
        thx_list = ['На здоровье', 'Обращайся', 'Не за что', 'Не стоит благодарности', 'Это моя работа', 'Обращайтесь еще', 'Рад был помочь']
        tts.va_speak(random.choice(thx_list))
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
        for text in self.listen():
            if text.startswith(('открой', 'запусти', 'зайди', 'зайди на')):
                self.open_browser(text)
            elif text.startswith(('узнай', 'найди')):
                self.google(text.split()[1:])
            else:
                for word in text.split():
                    for keywords in self.cmds:
                        if word in keywords:
                            self.cmds[keywords]()

if __name__ == '__main__':
    registr()
