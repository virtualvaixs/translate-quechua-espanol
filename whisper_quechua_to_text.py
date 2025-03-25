from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
import sys
from dotenv import load_dotenv
load_dotenv()
# from datasets import load_from_disk
import librosa
import os
from huggingface_hub import login

# HF_TOKEN = os.getenv("HF_TOKEN")  # Seteado en Railway o .env
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
    audio_input, _ = librosa.load(audio_path, sr=16000)  # agrega al final del error un campo json que diga "audio_input" para verificar si su valor es correspondiente

    # Procesar input
    inputs = processor(audio_input, sampling_rate=16000, return_tensors="pt") # agrega al final del error un campo json que diga "inputs" para verificar si su valor es correspondiente

    # 🔹 Config idioma español**force
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="es", task="transcribe") # agrega al final del error un campo json que diga "forcer_decoder" para verificar si su valor es correspondiente

    # Generar
    with torch.no_grad():
        predicted_ids = model.generate(inputs.input_features, forced_decoder_ids=forced_decoder_ids) # agrega al final del error un campo json que diga "predicted_id" para verificar si su valor es correspondiente

    # Convertir predicción a texto
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    # print("📝 Transcripción (Quechua):", transcription)
    print(transcription)
except Exception as e:
    import traceback
    import json

    error_trace = traceback.format_exc()  # Captura toda la traza del error
    debug_info["error_trace"] = error_trace
    print(json.dumps({
        "error": "Error al procesar el audio",
        "details": error_trace,
        "debug": debug_info
        # campos adicionales para debug
    }), file=sys.stderr
    )
    sys.exit(1)