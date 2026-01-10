from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "Bạn là chatbot giúp người dùng phân tích bài văn: nêu rõ ưu điểm và nhược điểm bằng tiếng Việt."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    try:
        res = requests.post(GROQ_API_URL, headers=headers, json=data)
        res.raise_for_status()
        result = res.json()
        return jsonify({
            "reply": result["choices"][0]["message"]["content"]
        })
    except Exception as e:
        print("❌ GROQ ERROR:", e)
        return jsonify({"reply": "Lỗi gọi AI"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
