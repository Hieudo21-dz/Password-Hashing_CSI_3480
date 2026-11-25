import secrets

def password_salt():
    salt = secrets.token_bytes(16)
    hashed_and_salted = hashed + salt.hex()