from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
import sys
from dotenv import load_dotenv
load_dotenv()
# from datasets import load_from_disk
import librosa
import os
from huggingface_hub import login

HF_TOKEN = os.getenv("HF_TOKEN")  # Seteado en Railway o .env
# if HF_TOKEN:
#     login(HF_TOKEN)

if len(sys.argv) < 2:
    print("Error: Se requiere la ruta del archivo de audio.")
    sys.exit(1)

# Cargar y transcribir un audio de prueba
# audio_path = "2Q.wav"  # Asegúrate de usar un archivo de prueba
audio_path = sys.argv[1]
# Ruta del modelo refinado (último checkpoint)
model_path = "LastEngineer01/whisper-quechua"
# Cargar modelo y procesador
processor = WhisperProcessor.from_pretrained(model_path)
model = WhisperForConditionalGeneration.from_pretrained(model_path)

try:
    # 🔹 Cargar el archivo de audio manualmente
    audio_input, _ = librosa.load(audio_path, sr=16000)  # Cargar audio y forzar SR=16kHz

    # Procesar input
    inputs = processor(audio_input, sampling_rate=16000, return_tensors="pt")

    # 🔹 Config idioma español**force
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="es", task="transcribe")

    # Generar
    with torch.no_grad():
        predicted_ids = model.generate(inputs.input_features, forced_decoder_ids=forced_decoder_ids)

    # Convertir predicción a texto
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    # print("📝 Transcripción (Quechua):", transcription)
    print(transcription)
except Exception as e:
    print("Error al procesar audio enforce:", str(e))