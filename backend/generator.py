"""Secure random password generation.

Owner: John / Hieu  (update)
"""
import secrets
import string


def generate_password(length: int = 16, use_symbols: bool = True) -> str:
    """Generate a random password with at least one lowercase, uppercase,
    digit (and symbol, if enabled)."""
    if length < 8:
        raise ValueError("Password length should be at least 8")

    pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if use_symbols:
        pools.append("!@#$%^&*()-_=+[]{};:,.?")

    # One character from each pool, the rest from all of them combined
    chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]

    # Shuffle so the required characters aren't always at the start
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


if __name__ == "__main__":
    print(generate_password())
