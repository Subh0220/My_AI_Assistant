import httpx

# Monkey patch: make sure Client accepts "proxies" even if mismatched
_orig_init = httpx.Client.__init__

def _patched_init(self, *args, **kwargs):
    kwargs.pop("proxies", None)  # remove unsupported argument
    return _orig_init(self, *args, **kwargs)

httpx.Client.__init__ = _patched_init

from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import PyPDF2
import docx
from PIL import Image
import pytesseract

app = Flask(__name__)

# ==== GITHUB MODELS (TOKEN FROM .ENV) ====
load_dotenv()
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)

feedback_file = "feedback.txt"

# ==== File Upload Config ====
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "docx", "png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Store uploaded file text in memory
uploaded_file_text = ""

# ==== Routes ====

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    global uploaded_file_text

    data = request.get_json(force=True, silent=True) or {}
    user_input = data.get('input', '')

    if not user_input.strip():
        return jsonify({"error": "No input provided"}), 400

    # If file uploaded, include it in context
    if uploaded_file_text:
        prompt = f"The user uploaded a document. Use it if relevant.\n\nDocument content:\n{uploaded_file_text}\n\nUser's question: {user_input}"
    else:
        prompt = f"Answer concisely and accurately: {user_input}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that can answer normal questions and also reference uploaded documents if relevant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
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


@app.route("/upload", methods=["POST"])
def upload_file():
    global uploaded_file_text

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        file_text = ""
        ext = filename.rsplit(".", 1)[1].lower()

        try:
            if ext == "txt":
                with open(filepath, "r", encoding="utf-8") as f:
                    file_text = f.read()

            elif ext == "pdf":
                with open(filepath, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    file_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

            elif ext == "docx":
                doc = docx.Document(filepath)
                file_text = "\n".join([p.text for p in doc.paragraphs])

            elif ext in ["png", "jpg", "jpeg"]:
                img = Image.open(filepath)
                file_text = pytesseract.image_to_string(img)

            else:
                file_text = "Unsupported file format."

            if not file_text.strip():
                file_text = "No readable text found in file."

            # Save globally
            uploaded_file_text = file_text[:4000]

            return jsonify({"response": "✅ File uploaded successfully. You can now ask questions about it!"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file type"}), 400


if __name__ == "__main__":
    app.run(debug=True)
