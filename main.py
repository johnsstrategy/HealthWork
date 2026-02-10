from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Willkommen bei meiner REST API! Geh zu /quote für ein Zitat."}

@app.get("/quote")
def get_random_quote():
    url = "https://api.quotable.io/random"

    response = requests.get(url, verify=False)
    data = response.json()

    return {
        "autor": data["author"],
        "zitat": data["content"]
    }


# https://github.com/lukePeavey/quotable Zitat API
# https://libretranslate.com/ Übersetzer API