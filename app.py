import os
from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

# Ta clé API
API_KEY = "AIzaSyBrYUgfQP3E_ZV6nMTTJdR-XZVgGPJrIH4"
genai.configure(api_key=API_KEY)

# Utilisation du nom de modèle complet pour éviter l'erreur 404
# gemini-1.5-flash-latest est le plus compatible sur Render
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

@app.route('/', methods=['GET', 'POST'])
def index():
    analyse_resultat = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                img = Image.open(file.stream)
                
                prompt = """
                Analyse cette capture de pari Bet261 (Madagascar). 
                Nous sommes le 20 Mars 2026.
                Donne un verdict : ASSURÉ, RISQUÉ ou DANGEREUX.
                Propose une alternative si besoin.
                Réponds en français direct (Style Gasy).
                """
                
                # Utilisation de generate_content qui est la méthode standard
                response = model.generate_content([prompt, img])
                analyse_resultat = response.text
            except Exception as e:
                # On affiche l'erreur proprement si ça persiste
                analyse_resultat = f"Erreur technique : {str(e)}"

    return render_template('index.html', resultat=analyse_resultat)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
