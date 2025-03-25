import os
from google.cloud import texttospeech
import sys

# 📌 Configurar la variable de entorno con las credenciales de Google Cloud
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "M:/engineer-works/translate-qechua-spanish/src-python/translate-quechua-spanish-v1.json"
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# 🔹 Texto en español para convertir a voz
if len(sys.argv) < 2:
    print("Error: Se requiere el texto a convertir a voz.")
    sys.exit(1)
texto_espanol = sys.argv[1]

# 🔹 Configurar cliente de Google Text-to-Speech
client = texttospeech.TextToSpeechClient()

# 🔹 Configurar la solicitud
synthesis_input = texttospeech.SynthesisInput(text=texto_espanol)
voice = texttospeech.VoiceSelectionParams(
    language_code="es-ES",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# 🔹 Generar audio
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# 🔹 Guardar el archivo de audio
output_audio_path = "output_audio.mp3"
with open(output_audio_path, "wb") as out:
    out.write(response.audio_content)
    print(output_audio_path)
