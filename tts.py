import pyttsx3
ru_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Aleksandr"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') #даёт подробности о текущем установленном голосе
engine.setProperty('voice', ru_voice)  # 0-мужской , 1-женский

def va_speak(audio):
    engine.say(audio)
    engine.runAndWait()
