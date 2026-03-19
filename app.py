import os
from flask import Flask, render_template, request
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

# Ta clé API Gemini intégrée
API_KEY = "AIzaSyBrYUgfQP3E_ZV6nMTTJdR-XZVgGPJrIH4"
genai.configure(api_key=API_KEY)

# Configuration du modèle Gemini 1.5 Flash (le plus rapide pour l'analyse d'images)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET', 'POST'])
def index():
    analyse_resultat = None
    if request.method == 'POST':
        # Récupération de l'image (capture Bet261) envoyée par le client
        file = request.files.get('file')
        if file:
            try:
                # Lecture de l'image
                img = Image.open(file.stream)
                
                # Instruction précise pour l'IA (Le "Prompt" Gasy Style)
                prompt = """
                Tu es un expert analyste de paris sportifs à Madagascar. 
                Analyse cette capture d'écran de pari (Bet261 ou autre). 
                Nous sommes le vendredi 20 mars 2026.
                
                1. Liste les matchs présents sur le ticket.
                2. Vérifie la probabilité de réussite pour chaque match en 2026.
                3. Donne un verdict clair : 'ASSURÉ ✅', 'RISQUÉ ⚠️' ou 'DANGEREUX ❌'.
                4. Si c'est risqué, propose une alternative (ex: Plus de 1.5 buts au lieu de Victoire).
                5. Termine par un encouragement pour le parieur malgache.
                Réponds en français simple et direct.
                """
                
                # Génération de l'analyse
                response = model.generate_content([prompt, img])
                analyse_resultat = response.text
            except Exception as e:
                analyse_resultat = f"Erreur lors de l'analyse : {str(e)}"

    return render_template('index.html', resultat=analyse_resultat)

if __name__ == '__main__':
    # Utilisation du port 5000 par défaut (standard pour Flask/Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
