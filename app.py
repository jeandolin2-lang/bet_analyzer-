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
                # 1. Préparation de l'image en Base64
                image_data = base64.b64encode(file.read()).decode('utf-8')
                
                # 2. Configuration de l'appel direct (On force la version v1 ici)
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Analyse cette capture Bet261. Donne un verdict : ASSURÉ, RISQUÉ ou DANGEREUX. Réponds en français simple (Style Gasy)."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": image_data}}
                        ]
                    }]
                }

                # 3. Envoi de la requête
                response = requests.post(url, json=payload)
                data = response.json()

                # 4. Extraction de la réponse
                if "candidates" in data:
                    analyse_resultat = data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    analyse_resultat = f"Erreur API : {data.get('error', {}).get('message', 'Réponse inconnue')}"

            except Exception as e:
                analyse_resultat = f"Erreur technique : {str(e)}"

    return render_template('index.html', resultat=analyse_resultat)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
