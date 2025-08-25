from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os

app = Flask(__name__)

# ==== GITHUB MODELS (TOKEN FROM .ENV) ====
load_dotenv()  # loads .env at project root
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")  # read safely from .env
)

feedback_file = "feedback.txt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(force=True, silent=True) or {}
    user_input = data.get('input', '')

    if not user_input.strip():
        return jsonify({"error": "No input provided"}), 400

    prompt = f"Answer concisely and accurately: {user_input}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful, creative AI assistant that can answer factual questions, summarize text, generate creative content, or give advice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        ai_reply = response.choices[0].message.content.strip()
        return jsonify({"response": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json(force=True, silent=True) or {}
    fb = data.get("feedback", "")
    if fb.strip():
        with open(feedback_file, "a") as f:
            f.write(f"{datetime.now()} - {fb}\n")
    return jsonify({"status": "Feedback recorded"})

if __name__ == "__main__":
    app.run(debug=True)