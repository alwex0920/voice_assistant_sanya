import speech_recognition as sr
import webbrowser
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

def main():
    while True:
        input_text = recognize_speech()
        print(input_text)
        if "Найди" or "найди" in input_text:
            webbrowser.open(f"https://yandex.ru/search/?text={input_text}&lr=63&clid=2271258&win=569")
        elif "Открой ютуб" or "открой ютуб" in input_text:
            tts.va_speak("Приятного просмотра сэр!")
            webbrowser.open("https://youtube.com")
        elif "Открой ВК" or "открой ВК" in input_text:
            webbrowser.open("https://vk.com")
        elif "Открой Telegram" or "открой Telegram" in input_text:
            webbrowser.open("https://web.telegram.org")
            tts.va_speak("Запрос выполнен сэр")
        elif "Скачай" or "скачай" in input_text:
            webbrowser.open(f"https://yandex.ru/search/?text={input_text}&lr=63&clid=2271258&win=569")
            tts.va_speak("Не подхватите вирусы!")
        elif "Открой сервер" or "открой сервер" in input_text:
            webbrowser.open("https://aternos.org")
            tts.va_speak("Приятной игры сэр!")
        elif "Выключи компьютер" or "выключи компьютер" in input_text:
            tts.va_speak("Выключение компьютера")
            os.system('shutdown /s /t 1')
        elif "Закрой окно" or "закрой окно" in input_text:
            pyautogui.hotkey('alt', 'f4')
            tts.va_speak("Запрос выполнен сэр")
        elif "Давай в крестики-нолики" or "давай в крестики-нолики" in input_text:
            tts.va_speak("Хорошо я буду беспощаден")
            import tictactoe
            tictactoe.tic()
        elif "Поведай мудрость" or "поведай мудрость" in input_text:
            citata = citata.citata_gen()
            tts.va_speak(citata)
        elif "Что ты умеешь" or "что ты умеешь" in input_text:
            text = "Я умею открывать ваши запросы командой 'найди, ваш запрос' также я умею открывать ютуб, выключать компьютер, открывать телеграм, открывать ссылки для скачивания, поиграть с вами в крестики-нолики, запустить игру майнкрафт, дать рандомную цитату командой 'поведай мудрость' и всё"
            tts.va_speak(text)
        elif "Давай в карты" or "давай в карты" in input_text:
            tts.va_speak("Для этого позовите своего друга")
            import drunkard
            drunkard.game.play_game()
        elif "Запусти Minecraft" or "запусти Minecraft" in input_text:
            nm = open("rg.json", "r+")
            nam = json.load(nm)
            name = nam['name']
            os.startfile(f"C:\\Users\\{name}\\AppData\\Roaming\\.tlauncher\\legacy\\Minecraft\\TL.exe")
        elif "Скажи" or "скажи" in input_text:
            tts.va_speak(input_text)
        else:
            print(input_text)


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
