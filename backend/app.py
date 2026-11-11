import os

from flask import Flask, jsonify, request, send_from_directory
from generator import generate_password
from hasing import hash_bcrypt, hash_sha256, verify_bcrypt

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")

MIN_LENGTH = 8
MAX_LENGTH = 128
BCRYPT_MAX_BYTES = 72

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")


def get_password(data):
    password = data.get("password", "")
    if not isinstance(password, str) or not password:
        return None, (jsonify({"error": "Password is required"}), 400)
    if len(password.encode("utf-8")) > BCRYPT_MAX_BYTES:
        return None, (jsonify({"error": f"Password must be at most {BCRYPT_MAX_BYTES} bytes"}), 400)
    return password, None

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.post("/api/hash")
def api_hash():
    data = request.get_json(silent=True) or {}
    password, error = get_password(data)
    if error:
        return error
    return jsonify({
        "sha256": hash_sha256(password),
        "bcrypt": hash_bcrypt(password),
    })

@app.post("/api/verify")
def api_verify():
    data = request.get_json(silent=True) or {}
    password, error = get_password(data)
    if error:
        return error
    stored_hash = data.get("hash", "")
    if not isinstance(stored_hash, str) or not stored_hash:
        return jsonify({"error": "Hash is required"}), 400
    try:
        ok = verify_bcrypt(password, stored_hash)
    except ValueError:
        return jsonify({"error": "Invalid bcrypt hash"}), 400
    return jsonify({"match": ok})

@app.get("/api/generate")
def api_generate():
    try:
        length = int(request.args.get("length", 16))
    except ValueError:
        return jsonify({"error": "Length must be a whole number"}), 400
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        return jsonify({"error": f"Length must be between {MIN_LENGTH} and {MAX_LENGTH}"}), 400
    return jsonify({"password": generate_password(length)})

if __name__ == "__main__":
    app.run(debug=True)