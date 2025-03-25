from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import sys

# VENV_PYTHON = r"M:\engineer-works\translate-qechua-spanish\coqui-env\Scripts\python.exe"  # Ruta al Python del entorno virtual

app = Flask(__name__)
CORS(app)  # Permite acceso desde cualquier origen (puedes restringirlo luego)


@app.route('/transcribe_quechua_to_spanish_text', methods=['POST'])
def transcribe_audio_and_translate_to_spanish():
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear la carpeta si no existe

    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    try:
        # Guardar el archivo temporalmente
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Ejecutar el script de Whisper y capturar la salida
        result_transcribe = subprocess.run(
            ["python", "whisper_quechua_to_text.py", file_path],
            capture_output=True, text=True)

        # Verificar si hubo error en la ejecución
        # if result_transcribe.returncode != 0:
        #     return jsonify({"error": "Error al procesar el audio", "details": result_transcribe.stderr}), 500
        if result_transcribe.returncode != 0:
            try:
                details = json.loads(result_transcribe.stdout)
            except:
                details = result_transcribe.stdout or "Error desconocido"
            return jsonify({"error": "Error al procesar el audio", "details": details}), 500
        # Obtener la transcripción desde stdout
                transcription_quechua_to_text = result_transcribe.stdout.strip()

        # Eliminar el archivo después de procesarlo
        os.remove(file_path)

        result_translation = subprocess.run(
            ["python", "google_text_quechua_to_spanish.py", transcription_quechua_to_text],
            capture_output=True, text=True)
        
        if result_translation.returncode != 0:
            return jsonify({"error": "Error al traducir el texto", "details": result_translation.stderr}), 500

        # Obtener la traducción desde stdout
        translated_to_spanish_text = result_translation.stdout.strip()
        return jsonify({"translation_spanish": translated_to_spanish_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/parse_to_sound_spanish', methods=['POST'])
def parse_to_sound_spanish():
    """Convierte texto en español a audio en MP3 usando Google Text-to-Speech"""
    data = request.get_json()

    if "text" not in data or not data["text"].strip():
        return jsonify({"error": "Debes proporcionar un texto en español"}), 400

    texto_espanol = data["text"].strip()

    try:
        # 🔹 Ejecutar el script para generar el audio
        result = subprocess.run(
            ["python", "google_text_to_sound_spanish.py", texto_espanol],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            return jsonify({"error": "Error al generar el audio", "details": result.stderr}), 500

        # Obtener la ruta del archivo de audio desde stdout
        audio_file_path = result.stdout.strip()

        # Enviar el archivo MP3 al cliente
        return send_file(audio_file_path, as_attachment=True, download_name="audio.mp3", mimetype="audio/mp3")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/transcribe_spansih_to_quechua_text', methods=['POST'])
def transcribe_audio_and_translate_to_quechua():
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear la carpeta si no existe

    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    try:
        # Guardar el archivo temporalmente
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Ejecutar el script de Whisper y capturar la salida
        result_transcribe = subprocess.run(
            ["python", "whisper_spanish_to_text.py", file_path],
            capture_output=True, text=True)

        # Verificar si hubo error en la ejecución
        if result_transcribe.returncode != 0:
            return jsonify({"error": "Error al procesar el audio", "details": result_transcribe.stderr}), 500

        # Obtener la transcripción desde stdout
        transcription_spanish_to_text = result_transcribe.stdout.strip()

        # Eliminar el archivo después de procesarlo
        os.remove(file_path)

        result_translation = subprocess.run(
            ["python", "google_text_spanish_to_quechua.py", transcription_spanish_to_text],
            capture_output=True, text=True)
        
        if result_translation.returncode != 0:
            return jsonify({"error": "Error al traducir el texto", "details": result_translation.stderr}), 500

        # Obtener la traducción desde stdout
        translated_to_quechua_text = result_translation.stdout.strip()
        return jsonify({"translation_quechua": translated_to_quechua_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/parse_to_sound_quechua', methods=['POST'])
def parse_to_sound_quechua():
    """Convierte texto en quechua a audio en MP3 usando Google Text-to-Speech"""
    data = request.get_json()

    if "text" not in data or not data["text"].strip():
        return jsonify({"error": "Debes proporcionar un texto en español"}), 400

    texto_quechua = data["text"].strip()

    try:
        # 🔹 Ejecutar el script para generar el audio
        result = subprocess.run(
            ["python", "google_text_to_sound_quechua-v1.py", texto_quechua],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            return jsonify({"error": "Error al generar el audio", "details": result.stderr}), 500

        # Obtener la ruta del archivo de audio desde stdout
        audio_file_path = result.stdout.strip()

        # Enviar el archivo MP3 al cliente
        return send_file(audio_file_path, as_attachment=True, download_name="audio_quechua.mp3", mimetype="audio/mp3")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
