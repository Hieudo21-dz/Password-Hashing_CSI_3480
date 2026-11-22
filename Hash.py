import bcrypt

def hash_password(password: str) -> str:
    # Convert string to bytes, generate salt, and hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12) # 12 is the standard work factor
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )
    
stored_hash = hash_password("my_secret_password")
print(f"Stored hash: {stored_hash}")