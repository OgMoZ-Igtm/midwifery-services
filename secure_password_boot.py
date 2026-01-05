# secure_password_boot.py
import secrets
import string
import hashlib


def generate_secure_password(length=16) -> str:
    """Génère un mot de passe robuste d'au moins 8 caractères."""
    if length < 8:
        length = 8  # Sécurité minimale
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def hash_password(password: str) -> str:
    """Retourne le hash SHA-256 du mot de passe."""
    return hashlib.sha256(password.encode()).hexdigest()


def boot_password():
    password = generate_secure_password()
    hashed = hash_password(password)
    print("🔐 Mot de passe généré au démarrage :", password)
    print("🔒 Hash SHA-256 :", hashed)
    return password, hashed


# Exécution automatique au démarrage
if __name__ == "__main__":
    boot_password()
