# import json
import requests
import sys

# 📌 Cargar la API Key desde el archivo JSON
# json_path = "google_api_key.json"
# with open(json_path, "r") as file:
#     config = json.load(file)
#     API_KEY = config["API_KEY"]
API_KEY = os.getenv("API_KEY")  # Obtener la clave desde las variables de entorno
# Leer el texto en español transcrito
# with open("texto_espanol.txt", "r", encoding="utf-8") as f:
#     texto_espanol = f.read()
if len(sys.argv) < 2:
    print("❌ Error: Debes proporcionar un texto en Quechua para traducir.")
    sys.exit(1)

texto_espanol = sys.argv[1] 

# 🔹 URL de la API de Google Translate
url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"

# 🔹 Datos de la solicitud
data = {
    "q": texto_espanol,
    "source": "es",  # Español
    "target": "qu",  # Quechua (Boliviano)
    "format": "text"
}

# 🔹 Hacer la solicitud a la API de Google Translate
response = requests.post(url, json=data)

# 🔹 Procesar la respuesta
if response.status_code == 200:
    traduccion = response.json()["data"]["translations"][0]["translatedText"]
    print(traduccion)
else:
    print("❌ Error en la solicitud: {response.json()}")
