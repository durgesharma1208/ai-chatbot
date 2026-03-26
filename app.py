# app.py
import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Initialize Gemini client
try:
    client = genai.Client()
    chat_session = client.chats.create(model="gemini-2.5-flash")
    print("✅ Gemini client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
    print("Did you set the GEMINI_API_KEY environment variable?")
    client = None
    chat_session = None


@app.route("/")
def index():
    """Serve the chat frontend."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle incoming chat messages."""
    global chat_session

    if not chat_session:
        return jsonify({"error": "Gemini client not initialized. Check your API key."}), 500

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reset", methods=["POST"])
def reset_chat():
    """Reset the chat session to start a new conversation."""
    global chat_session

    if not client:
        return jsonify({"error": "Gemini client not initialized."}), 500

    try:
        chat_session = client.chats.create(model="gemini-2.5-flash")
        return jsonify({"status": "Chat session reset successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
