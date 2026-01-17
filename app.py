from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Gemini config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Bạn là chatbot hỗ trợ học tập cho học sinh THCS Việt Nam. "
        "Trả lời bằng tiếng Việt, rõ ràng, dễ hiểu, đúng chương trình SGK. "
        "Không lan man, không dùng từ ngữ người lớn."
    )
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data_json = request.get_json()
    if not data_json or "message" not in data_json:
        return jsonify({"reply": "❌ Không nhận được message"}), 400

    user_input = data_json["message"]

    try:
        response = model.generate_content(user_input)
        return jsonify({
            "reply": response.text
        })
    except Exception as e:
        print("❌ GEMINI ERROR:", e)
        return jsonify({
            "reply": "❌ Lỗi Gemini API"
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
