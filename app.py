import os
from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

# Ta clé API
API_KEY = "AIzaSyBrYUgfQP3E_ZV6nMTTJdR-XZVgGPJrIH4"
genai.configure(api_key=API_KEY)

# On utilise 'gemini-pro-vision', il est reconnu partout sans erreur 404
model = genai.GenerativeModel('gemini-pro-vision')

@app.route('/', methods=['GET', 'POST'])
def index():
    analyse_resultat = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                img = Image.open(file.stream)
                
                # Le prompt reste le même
                prompt = "Analyse cette capture de pari Bet261. Donne un verdict : ASSURÉ, RISQUÉ ou DANGEREUX. Réponds en français style Gasy."
                
                # Version simplifiée pour la compatibilité maximale
                response = model.generate_content([prompt, img])
                analyse_resultat = response.text
            except Exception as e:
                # Si ça rate encore, on affiche l'erreur pour comprendre
                analyse_resultat = f"Erreur technique : {str(e)}"

    return render_template('index.html', resultat=analyse_resultat)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
