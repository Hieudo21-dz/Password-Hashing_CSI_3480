# Password-Hashing_CSI_3480
CSI 3480 project exploring secure password storage: hashing, salting, and resistance to brute-force attacks

A team project for CSI 3480 that explores secure password storage. Users can enter a password in a web interface, see how strong it is, and watch how it gets salted and hashed. The Python backend also generates strong random passwords.

Features

Frontend (UI)
Enter a password and test it in real time
Strength metrics: length, character variety, entropy estimate, and a strength rating
Show the generated salt and the resulting hash
Generate a secure password with one click

Backend (Python)
Salted password hashing (e.g. bcrypt / Argon2, with SHA-256 for comparison) <!-- edit to match -->
Unique random salt for every password, generated with a cryptographically secure source (secrets / os.urandom)
Password verification against a stored hash
Secure random password generation

How It Works
The user types a password into the interface.
The frontend calculates strength metrics and sends the password to the backend.
The backend generates a random salt, hashes the salted password, and returns the result.
To log in, the entered password is hashed again with the same salt and compared to the stored hash.
Hashing vs. Encryption

Encryption can be reversed with a key. Hashing is one-way: there's no way to get the password back from the hash, so systems compare hashes instead of storing passwords.

Why Salt?

A salt is a random value added to each password before hashing. Identical passwords end up with different hashes, which defeats precomputed rainbow tables.

Why Slow Hashes?

MD5 and SHA-256 are built to be fast, which makes brute-forcing them fast too. bcrypt, scrypt, and Argon2 are deliberately slow and have an adjustable cost factor, so every guess is expensive for an attacker.
