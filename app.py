import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Store chat sessions (simple approach)
chat_sessions = {}

try:
    client = genai.Client()
    print("✅ Gemini client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
    client = None


def get_chat_session():
    """Get or create a chat session."""
    global chat_sessions
    if "default" not in chat_sessions:
        chat_sessions["default"] = client.chats.create(model="gemini-2.5-flash")
    return chat_sessions["default"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    if not client:
        return jsonify({"error": "Gemini client not initialized."}), 500

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        session = get_chat_session()
        response = session.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reset", methods=["POST"])
def reset_chat():
    if not client:
        return jsonify({"error": "Gemini client not initialized."}), 500
    try:
        chat_sessions["default"] = client.chats.create(model="gemini-2.5-flash")
        return jsonify({"status": "Chat session reset successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ THIS IS THE KEY CHANGE FOR DEPLOYMENT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
