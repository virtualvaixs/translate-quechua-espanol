import whisper
import sys
# Cargar modelo de Whisper (puedes usar "small" o "medium" si necesitas más precisión)
modelo = whisper.load_model("medium")

# 📌 Ruta del archivo de audio en español
# archivo_audio = "output_audio.mp3"  # Cambia esto por el nombre del audio
if len(sys.argv) < 2:
    print("Error: Se requiere la ruta del archivo de audio.")
    sys.exit(1)
audio_path = sys.argv[1]
# Transcribir el audio a texto
resultado = modelo.transcribe(audio_path, language="es")
texto_espanol = resultado["text"]

# Guardar la transcripción en un archivo
# with open("texto_espanol.txt", "w", encoding="utf-8") as f:
#     f.write(texto_espanol)

print(texto_espanol)
