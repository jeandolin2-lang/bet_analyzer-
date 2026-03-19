import os
from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

# TA CLÉ API INTÉGRÉE
API_KEY = "AIzaSyBrYUgfQP3E_ZV6nMTTJdR-XZVgGPJrIH4"
genai.configure(api_key=API_KEY)

# Modèle standard reconnu par Render
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET', 'POST'])
def index():
    analyse_resultat = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', resultat="Aucun fichier trouvé")
            
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', resultat="Fichier vide")
            
        if file:
            try:
                img = Image.open(file.stream)
                prompt = "Analyse cette capture Bet261. Donne un verdict : ASSURÉ, RISQUÉ ou DANGEREUX. Réponds en français simple (Style Gasy)."
                response = model.generate_content([prompt, img])
                analyse_resultat = response.text
            except Exception as e:
                analyse_resultat = f"Erreur : {str(e)}"

    return render_template('index.html', resultat=analyse_resultat)

if __name__ == '__main__':
    # TRÈS IMPORTANT : Render a besoin de cette configuration pour lancer le site
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
