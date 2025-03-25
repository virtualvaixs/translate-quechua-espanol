import os
import json
from google.cloud import texttospeech
from google.oauth2 import service_account
import sys

from dotenv import load_dotenv
load_dotenv()
# 📌 Cargar credenciales desde la variable JSON
service_account_info = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "M:/engineer-works/translate-qechua-spanish/src-python/translate-quechua-spanish-v1.json"
# cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if len(sys.argv) < 2:
    print("Error: Se requiere el texto a convertir a voz.")
    sys.exit(1)
texto_quechua = texto_espanol = sys.argv[1]

client = texttospeech.TextToSpeechClient(credentials=credentials)

synthesis_input = texttospeech.SynthesisInput(text=texto_quechua)

voice = texttospeech.VoiceSelectionParams(
    language_code="es-ES", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = client.synthesize_speech(#aqui parece ser el error
    input=synthesis_input, voice=voice, audio_config=audio_config
)
output_audio_path = "output_audio_quechua.mp3"
with open(output_audio_path, "wb") as out:
    out.write(response.audio_content)
    print(output_audio_path)