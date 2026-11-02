"""Password hashing and verification.

Owner: John / Hieu  (update)

Two methods are included so the project can compare them:
  - SHA-256 + salt: fast, shown for comparison (NOT recommended for real passwords)
  - bcrypt: slow, salted, adjustable cost (recommended)
"""
import hashlib
import hmac

import bcrypt

from salting import generate_salt


# ---------- SHA-256 (for comparison) ----------

def hash_sha256(password: str, salt: str | None = None) -> dict:
    """Hash password with a salt using SHA-256."""
    if salt is None:
        salt = generate_salt()
    digest = hashlib.sha256((salt + password).encode()).hexdigest()
    return {"algorithm": "sha256", "salt": salt, "hash": digest}


def verify_sha256(password: str, salt: str, stored_hash: str) -> bool:
    """Check a password against a stored SHA-256 hash."""
    candidate = hash_sha256(password, salt)["hash"]
    return hmac.compare_digest(candidate, stored_hash)  # constant-time compare


# ---------- bcrypt (recommended) ----------

def hash_bcrypt(password: str, rounds: int = 12) -> dict:
    """Hash password with bcrypt. The salt is generated and stored inside the hash."""
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return {"algorithm": "bcrypt", "salt": salt.decode(), "hash": hashed.decode()}


def verify_bcrypt(password: str, stored_hash: str) -> bool:
    """Check a password against a stored bcrypt hash."""
    return bcrypt.checkpw(password.encode(), stored_hash.encode())


if __name__ == "__main__":
    # Quick self-test: python hashing.py
    s = hash_sha256("test123")
    b = hash_bcrypt("test123")
    print("SHA-256:", s)
    print("bcrypt: ", b)
    print("SHA-256 verify:", verify_sha256("test123", s["salt"], s["hash"]))
    print("bcrypt verify: ", verify_bcrypt("test123", b["hash"]))
    print("Wrong password:", verify_bcrypt("wrong", b["hash"]))
