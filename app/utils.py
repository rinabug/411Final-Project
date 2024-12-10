import hashlib

def hash_password(password, salt):
    """Hash a password with the given salt."""
    pwdhash = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000
    )
    return pwdhash.hex()
