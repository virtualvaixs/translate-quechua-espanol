# import json
import requests
import sys
import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")  # Obtener la clave desde las variables de entorno
# 📌 Verificar si se proporcionó un texto como argumento
if len(sys.argv) < 2:
    print("❌ Error: Debes proporcionar un texto en Quechua para traducir.")
    sys.exit(1)

texto_quechua = sys.argv[1]  # Obtener el texto desde los argumentos

# 🔹 URL de la API de Google Translate
url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"

# 🔹 Datos de la solicitud
data = {
    "q": texto_quechua,
    "source": "qu",  # Idioma de origen: Quechua
    "target": "es",  # Idioma de destino: Español
    "format": "text"
}

# 🔹 Hacer la solicitud a la API
response = requests.post(url, json=data)

# 🔹 Mostrar la traducción si la solicitud fue exitosa
if response.status_code == 200:
    traduccion = response.json()["data"]["translations"][0]["translatedText"]
    print(traduccion)
else:
    print("❌ Error en la solicitud: {response.json()}")
