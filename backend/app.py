"""Flask server that connects the frontend to the hashing code.

Run:  python backend/app.py
Then open http://localhost:5000 in your browser.
"""
import os

from flask import Flask, jsonify, request, send_from_directory

from generator import generate_password
from hashing import hash_bcrypt, hash_sha256, verify_bcrypt

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.post("/api/hash")
def api_hash():
    password = request.json.get("password", "")
    if not password:
        return jsonify({"error": "Password is required"}), 400
    return jsonify({
        "sha256": hash_sha256(password),
        "bcrypt": hash_bcrypt(password),
    })


@app.post("/api/verify")
def api_verify():
    data = request.json
    ok = verify_bcrypt(data.get("password", ""), data.get("hash", ""))
    return jsonify({"match": ok})


@app.get("/api/generate")
def api_generate():
    length = int(request.args.get("length", 16))
    return jsonify({"password": generate_password(length)})


if __name__ == "__main__":
    app.run(debug=True)
