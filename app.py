from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Server läuft!"

@app.route('/generate-description', methods=['POST'])
def generate_description():
    data = request.get_json()
    image_url = data.get("image_url")
    if not image_url:
        return jsonify({"error": "Missing image_url"}), 400
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # ✅ Neue Modellbezeichnung
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "Describe the fashion item in this image for a Vinted listing. Be clear, friendly, and realistic."},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ],
            max_tokens=300
        )
        return jsonify({"description": response.choices[0].message.content.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
