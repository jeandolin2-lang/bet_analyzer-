import os
from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

# TA CLÉ API
API_KEY = "AIzaSyBrYUgfQP3E_ZV6nMTTJdR-XZVgGPJrIH4"

# CONFIGURATION FORCEE EN VERSION V1 (STABLE)
genai.configure(api_key=API_KEY, transport='rest') # 'rest' est plus stable sur Render

# Utilisation du nom complet du modèle
model = genai.GenerativeModel('models/gemini-1.5-flash')

@app.route('/', methods=['GET', 'POST'])
def index():
    analyse_resultat = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                img = Image.open(file.stream)
                
                # Le Prompt pour tes pronostics Bet261
                prompt = "Analyse cette capture Bet261. Donne un verdict : ASSURÉ, RISQUÉ ou DANGEREUX. Réponds en français simple (Style Gasy)."
                
                # Appel à l'IA
                response = model.generate_content([prompt, img])
                analyse_resultat = response.text
                
            except Exception as e:
                analyse_resultat = f"Erreur technique : {str(e)}"

    return render_template('index.html', resultat=analyse_resultat)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
