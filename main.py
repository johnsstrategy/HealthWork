import os
import requests
import deepl
import urllib3
from fastapi import FastAPI
from dotenv import load_dotenv

deepl_client = None

def setup():
    global deepl_client

    load_dotenv()
    auth_key = os.getenv("DEEPL_API_KEY")
    if not auth_key:
        raise ValueError("Kein DeepL API Key angegeben.")

    deepl_client = deepl.DeepLClient(auth_key)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

setup()
app = FastAPI()

# Funktion zum Übersetzen
def translate(englischer_text):
    try:
        deutscher_text = deepl_client.translate_text(englischer_text, target_lang="DE")

    except Exception:
        deutscher_text = f"(Übersetzung fehlgeschlagen) {englischer_text}"

    return deutscher_text.text

# Willkommensnachricht
@app.get("/")
def read_root():
    return {"message": "Willkommen bei meiner REST API! Geh zu /quote für ein Zitat."}

# Random Zitat abrufen
@app.get("/quote")
def get_random_quote(kategorie: str = "motivational", max_laenge: int = 120):
    url = f"https://api.quotable.io/random?tags={kategorie}&maxLength={max_laenge}"

    response = requests.get(url, verify=False)

    if response.status_code != 200:
        return {"error": "Kategorie nicht gefunden oder API-Fehler"}

    data = response.json()

    zitat = translate(data["content"])
    return {
        "autor": data["author"],
        "zitat": zitat,
        "original_zitat": data["content"],
        "tags": data["tags"],
        "laenge": data["length"]
    }

def translate(englischer_text):
    try:
        deutscher_text = deepl_client.translate_text(englischer_text, target_lang="DE")

    except Exception:
        deutscher_text = f"(Übersetzung fehlgeschlagen) {englischer_text}"

    return deutscher_text.text