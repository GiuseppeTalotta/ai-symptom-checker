from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import openai

# variables
load_dotenv()

# API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("OPENAI_API_KEY non trovata! Controlla il file .env")

openai.api_key = api_key

app = Flask(__name__)

# List symptoms
symptoms = []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', symptoms=symptoms)

@app.route('/add-symptom', methods=['POST'])
def add_symptom():
    symptom = request.form.get('symptom')
    if symptom:
        symptoms.append(symptom)
    return redirect(url_for('home'))

@app.route('/get-diagnosis', methods=['POST'])
def get_diagnosis():
    if not symptoms:
        return redirect(url_for('home'))

    prompt = "Given these symptoms: " + ", ".join(symptoms) + \
             ". Suggest possible medical conditions."

    try:
        # API openai >= 1.0.0
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        diagnosis = response.choices[0].message.content.strip()
    except Exception as e:
        diagnosis = f"Errore nella chiamata API: {e}"

    return render_template('diagnosis.html', diagnosis=diagnosis, symptoms=symptoms)


if __name__ == '__main__':
    app.run(debug=True)
