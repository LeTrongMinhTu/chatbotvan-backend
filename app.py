from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google import genai

# Load .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Init Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "❌ Thiếu message"}), 400

        msg = data["message"]

        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=msg
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("❌ GEMINI ERROR:", e)
        return jsonify({"reply": "⚠️ Lỗi server"}), 500


if __name__ == "__main__":
    app.run(debug=True)
