"""Salt generation.

Owner: John / Hieu  (update)
"""
import secrets


def generate_salt(num_bytes: int = 16) -> str:
    """Return a cryptographically secure random salt as a hex string."""
    return secrets.token_hex(num_bytes)
