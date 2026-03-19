import os
from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

# TA CLÉ EST BIEN ICI :
API_KEY = "AIzaSyBrYUgfQP3E_ZV6nMTTJdR-XZVgGPJrIH4"
genai.configure(api_key=API_KEY)

# On utilise le nom court 'gemini-1.5-flash' qui est le plus standard
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET', 'POST'])
def index():
    analyse_resultat = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                # Lecture de l'image
                img = Image.open(file.stream)
                
                # On force l'IA à répondre simplement pour tester
                prompt = "Analyse ce ticket de pari Bet261. Est-ce un bon pronostic ? Réponds en français style Gasy."
                
                # Appel de l'IA
                response = model.generate_content([prompt, img])
                
                if response and response.text:
                    analyse_resultat = response.text
                else:
                    analyse_resultat = "L'IA a lu l'image mais n'a pas pu générer de texte."
                    
            except Exception as e:
                # Affichage de l'erreur précise pour le débuggage
                analyse_resultat = f"Détails technique : {str(e)}"

    return render_template('index.html', resultat=analyse_resultat)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
