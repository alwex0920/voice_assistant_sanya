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
    put_text = recognize_speech()
    input_text = put_text.lower()
    print(input_text)
    if input_text == "найди":
        import webbrowser
        webbrowser.open(f"https://yandex.ru/search/?text={input_text}&lr=63&clid=2271258&win=569")
    elif input_text == "Открой ютуб" or "открой ютуб":
        import webbrowser
        tts.va_speak("Приятного просмотра сэр!")
        webbrowser.open("https://youtube.com")
    elif input_text == "открой вк":
        import webbrowser
        webbrowser.open("https://vk.com")
    elif input_text == "открой telegram":
        import webbrowser
        webbrowser.open("https://web.telegram.org")
        tts.va_speak("Запрос выполнен сэр")
    elif input_text == "открой сервер":
        import webbrowser
        webbrowser.open("https://aternos.org")
        tts.va_speak("Приятной игры сэр!")
    else:
        print(input_text)
    exec(open("commands.txt", "r+").read())
    if input_text == "выключи компьютер":
        tts.va_speak("Выключение компьютера")
        os.system('shutdown /s /t 1')
    elif input_text == "закрой окно":
        pyautogui.hotkey('alt', 'f4')
        tts.va_speak("Запрос выполнен сэр")
    elif input_text == "давай в крестики-нолики":
        tts.va_speak("Хорошо я буду беспощаден")
        import tictactoe
        tictactoe.tic()
    elif input_text == "поведай мудрость":
        citata = citata.citata_gen()
        tts.va_speak(citata)
    elif input_text == "что ты умеешь":
        text = "Я умею открывать ваши запросы командой 'найди, ваш запрос' также я умею открывать ютуб, выключать компьютер, открывать телеграм, открывать ссылки для скачивания, поиграть с вами в крестики-нолики, открыть гитхаб, дать рандомную цитату командой 'поведай мудрость' и всё"
        tts.va_speak(text)
    elif input_text == "давай в карты":
        tts.va_speak("Для этого позовите своего друга")
        import drunkard
        drunkard.game.play_game()
    elif input_text == "скажи":
        tts.va_speak(input_text)
    elif input_text == "саня" or "санёк" or "сане" or "сандаль" or "александр":
        tts.va_speak("Слушаю вас сэр")
    else:
        print(input_text)

def main():
    while True:
        vo = recognize_speech()
        voice = vo.lower()
        print(voice)
        if voice == "саня" or "санёк" or "сане" or "сандаль" or "александр":
            tts.va_speak("Слушаю вас сэр")
            assistant()
        else:
            print(voice)

def registr():
    with open("rg.json", "r+") as f:
        registr = json.load(f)
        print("Reading file...")
        time.sleep(2)
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
