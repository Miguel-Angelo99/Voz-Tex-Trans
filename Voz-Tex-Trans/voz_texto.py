import io
import os
import wave
import sounddevice as sd
import numpy as np
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v2 as translate
import time

# Configurar credenciales de Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = #La credencial el json de Google Cloud

def grabar_audio(nombre_archivo, duracion_segundos):
    print(f"Grabando audio por {duracion_segundos} segundos...")
    for i in range(duracion_segundos, 0, -1):
        print(f"Tiempo restante: {i} segundos")
        time.sleep(1)
    print("Grabando, tiene 5 segundos.")

    grabacion = sd.rec(int(duracion_segundos * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    grabacion_mono = np.squeeze(grabacion)

    with wave.open(nombre_archivo, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(fs)
        wav.writeframes(grabacion_mono.tobytes())

def transcribir_audio(nombre_archivo):
    client = speech.SpeechClient()

    with io.open(nombre_archivo, "rb") as audio_file:
        contenido = audio_file.read()

    audio = speech.RecognitionAudio(content=contenido)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=fs,
        language_code="es-PE",
    )

    response = client.recognize(config=config, audio=audio)

    texto_transcrito = ""
    for result in response.results:
        texto_transcrito += result.alternatives[0].transcript + " "

    return texto_transcrito

def traducir_texto(texto, idioma_destino):
    client = translate.Client()

    traduccion = client.translate(texto, target_language=idioma_destino)

    return traduccion['translatedText']

# Configuración de la grabación de audio
fs = 44100  # Frecuencia de muestreo
duracion_grabacion_segundos = 5  # Duración de la grabación en segundos
nombre_archivo_audio = "grabacion.wav"  # Nombre del archivo de audio

# Grabar audio
grabar_audio(nombre_archivo_audio, duracion_grabacion_segundos)

# Transcribir audio
texto_transcrito = transcribir_audio(nombre_archivo_audio)
print("Texto transcrito:", texto_transcrito)

# Traducir texto
idioma_destino = "en"  # Idioma destino (por ejemplo, inglés)
texto_traducido = traducir_texto(texto_transcrito, idioma_destino)
print("Texto traducido:", texto_traducido)
