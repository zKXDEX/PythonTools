import speech_recognition as sr
import pyttsx3
import time
from colorama import Fore, Back, Style

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')

    voice_index = 0
    selected_voice = voices[voice_index].id

    engine.setProperty('voice', selected_voice)

    with sr.Microphone() as source:
        print(f"{Fore.GREEN}{time.strftime('%H:%M:%S')}{Style.RESET_ALL} | Se inició correctamente")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language='es-ES')
        print(text)
        if text == "me puedes buscar en Google gatos":
            engine.say("buscando gatos en google")
            engine.runAndWait()
            engine.say("gatos encontrados")
            engine.runAndWait()
            engine.say("Analizando informacion")
            engine.runAndWait()


        # engine.say("Estás diciendo: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition no pudo entender el audio")
    except sr.RequestError as e:
        print(f"No se pudo obtener los resultados de Google Speech Recognition; {e}")

if __name__ == "__main__":
    recognize_speech_from_mic()