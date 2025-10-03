import requests, os

url = "http://localhost:5000/process"

# Vai mandar todas as imagens .jpg e .png da pasta atual
for file in os.listdir("."):
    if file.lower().endswith((".jpg", ".png")):
        print(f"Enviando {file}...")
        with open(file, "rb") as f:
            r = requests.post(url, files={"image": f})
        print("Resposta:", r.json())