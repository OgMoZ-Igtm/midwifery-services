# utils/users_admin.py


def verifier_utilisateur(username: str, password: str) -> bool:
    utilisateurs_autorisés = {
        "admin": "secret",
        "doctor": "med123",
        "patient": "mypassword",
    }
    return utilisateurs_autorisés.get(username) == password
