from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get configuration from environment variables
BOT_TOKEN = os.getenv('8041727281:AAGzXNoyYNG3tp7PVV-NQfLyN6tsolW8ShM')
MESSAGE = os.getenv('MESSAGE', '✅️Your verification was successful!')
SECRET_KEY = os.getenv('SECRET_KEY')  # For additional security

@app.route('/send', methods=['POST'])
def send_message():
    # Basic security check
    if request.headers.get('X-Secret-Key') != SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json
    chat_id = data.get('chat_id')
    
    if not chat_id:
        return jsonify({"error": "chat_id missing"}), 400

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": MESSAGE
    }
    
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()  # Raise exception for bad status codes
        return jsonify(r.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')