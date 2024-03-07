# Importación de los módulos necesarios
import AVMSpeechMath as sm
import AVMYT as yt
import speech_recognition as sr
import pyttsx3
import pywhatkit
import json
from datetime import datetime, date, timedelta
import wikipedia
import pyjokes
from time import time

# Inicialización del tiempo de inicio
start_time = time()

# Inicialización del motor de síntesis de voz
engine = pyttsx3.init()

# Nombre del asistente virtual
name = 'alexa'
attempts = 0



# Colores para la salida en consola
green_color = "\033[1;32;40m"
red_color = "\033[1;31;40m"
normal_color = "\033[0;37;40m"

# Obtención de las voces disponibles y selección de la primera
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Configuración adicional del motor de síntesis de voz
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.7)

# Carga de los nombres de los días en español e inglés desde archivos de texto
day_es = [line.rstrip('\n') for line in open('src/day/day_es.txt')]
day_en = [line.rstrip('\n') for line in open('src/day/day_en.txt')]

# Función para iterar los nombres de los días
def iterateDays(now):
    for i in range(len(day_en)):
        if day_en[i] in now:
            now = now.replace(day_en[i], day_es[i])
    return now

# Función para obtener el día actual
def getDay():
    now = date.today().strftime("%A, %d de %B del %Y").lower()
    return iterateDays(now)

# Función para obtener el día hace cierta cantidad de días
def getDaysAgo(rec):
    value = ""
    if 'ayer' in rec:
        days = 0
        value = 'ayer'
    elif 'antier' in rec:
        days = 2
        value = 'antier'
    else:
        rec = rec.replace(",", "")
        rec = rec.split()
        days = 0

        for i in range(len(rec)):
            try:
                days = float(rec[i])
                break
            except:
                pass

    if days != 0:
        try:
            now = date.today() - timedelta(days=days)
            now = now.strftime("%A, %d de %B del %Y").lower()

            if value != "":
                return f"{value} fue {iterateDays(now)}"
            else:
                return f"Hace {days} días fue {iterateDays(now)}"
        except:
            return "Aún no existíamos"
    else:
        return "No entendí"

# Función para sintetizar y reproducir un texto
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Función para obtener entrada de audio
def get_audio():
    r = sr.Recognizer()
    status = False

    with sr.Microphone() as source:
        print(f"{green_color}({attempts}) Escuchando...{normal_color}")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""

        try:
            rec = r.recognize_google(audio, language='es-ES').lower()

            if name in rec:
                rec = rec.replace(f"{name} ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                status = True
            else:
                print(f"Vuelve a intentarlo, no reconozco: {rec}")
        except:
            pass
    return {'text': rec, 'status': status}

# Bucle principal del programa
while True:
    # Obtener entrada de audio
    rec_json = get_audio()

    rec = rec_json['text']
    status = rec_json['status']

    if status:
        # Procesar la entrada de voz
        if 'estas ahi' in rec:
            speak('Por supuesto')

        elif 'que' in rec:
            if 'hora' in rec:
                hora = datetime.now().strftime('%I:%M %p')
                speak(f"Son las {hora}")

            elif 'dia' in rec:
                if 'fue' in rec:
                    speak(f"{getDaysAgo(rec)}")
                else:
                    speak(f"Hoy es {getDay()}")

        elif 'busca' in rec:
            order = rec.replace('busca', '')
            wikipedia.set_lang("es")
            info = wikipedia.summary(order, 1)
            speak(info)

        elif 'chiste' in rec:
            chiste = pyjokes.get_joke("es")
            speak(chiste)

        elif 'cuanto es' in rec:
            speak(sm.getResult(rec))
       
        # Terminar el programa si se recibe la orden
        elif 'descansa' in rec:
            speak("Saliendo...")
            break

        else:
            print(f"Vuelve a intentarlo, no reconozco: {rec}")

        attempts = 0
    else:
        attempts += 1

# Imprimir el tiempo de ejecución del programa al finalizar
print(f"{red_color} PROGRAMA FINALIZADO CON UNA DURACIÓN DE: {int(time() - start_time)} SEGUNDOS {normal_color}")
