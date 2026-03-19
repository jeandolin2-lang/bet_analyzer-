import os
import requests
from flask import Flask, render_template, request
import base64

app = Flask(__name__)

# TA CLÉ API
API_KEY = "AIzaSyBrYUgfQP3E_ZV6nMTTJdR-XZVgGPJrIH4"

@app.route('/', methods=['GET', 'POST'])
def index():
    analyse_resultat = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                # 1. Préparation de l'image
                image_data = base64.b64encode(file.read()).decode('utf-8')
                
                # 2. Utilisation de GEMINI-PRO-VISION (Le modèle le plus compatible)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={API_KEY}"
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Analyse cette capture Bet261. Donne un verdict : ASSURÉ, RISQUÉ ou DANGEREUX. Réponds en français simple (Style Gasy)."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": image_data}}
                        ]
                    }]
                }

                # 3. Envoi
                response = requests.post(url, json=payload)
                data = response.json()

                # 4. Extraction
                if "candidates" in data:
                    analyse_resultat = data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    # Si ça échoue encore, on affiche la réponse brute pour comprendre
                    analyse_resultat = f"Détails : {data}"

            except Exception as e:
                analyse_resultat = f"Erreur technique : {str(e)}"

    return render_template('index.html', resultat=analyse_resultat)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
