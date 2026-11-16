import secrets
import string


def generate_password(length: int = 16, use_symbols: bool = True) -> str:
    """Generate a random password with at least one lowercase, uppercase,
    digit (and symbol, if enabled)."""
    if not 8 <= length <= 128:
        raise ValueError("Password length should be between 8 and 128")

    pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if use_symbols:
        pools.append("!@#$%^&*()-_=+[]{};:,.?")

    chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]

    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


if __name__ == "__main__":
    print(generate_password())