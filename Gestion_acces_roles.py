import logging
import os
from datetime import datetime

# --- Configuration et Données de l'Application ---

# Créer un dossier 'logs' si il n'existe pas
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configuration du logger pour enregistrer les accès refusés
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Définir les rôles et les "packs" (pages) auxquels ils ont accès.
# C'est la source de vérité pour le contrôle d'accès.
ROLE_ACCESS = {
    "ADMIN": [
        "ADMIN",
        "MESSAGES",
        "PATIENT",
        "DOCTOR",
        "MIDWIFE",
        "NURSE",
        "STUDENT",
        "DOCTORAL",
        "INTERN",
        "ORGANISATION",
    ],
    "PATIENT": ["PATIENT", "MESSAGES"],
    "DOCTOR": ["DOCTOR", "PATIENT", "MESSAGES"],
    "MIDWIFE": ["MIDWIFE", "MESSAGES"],
    "NURSE": ["NURSE", "MESSAGES"],
    "STUDENT": ["STUDENT", "MESSAGES"],
    "DOCTORAL": ["DOCTORAL", "MESSAGES"],
    "INTERN": ["INTERN", "MESSAGES"],
}


# Simule les "pages" ou "packs" de votre application.
# Chaque page doit avoir une fonction `app()` pour être considérée comme valide.
class Page:
    def __init__(self, name):
        self.name = name

    # Cette méthode simule la logique de la page et doit exister pour être une page valide
    def app(self, user_role):
        print(
            f"✅ La page '{self.name}' a été affichée pour l'utilisateur avec le rôle '{user_role}'."
        )


# Dictionnaire des pages disponibles avec leur fonction app()
PAGES = {
    "ADMIN": Page("ADMIN"),
    "MESSAGES": Page("MESSAGES"),
    "PATIENT": Page("PATIENT"),
    "DOCTOR": Page("DOCTOR"),
    "MIDWIFE": Page("MIDWIFE"),
    "NURSE": Page("NURSE"),
    "STUDENT": Page("STUDENT"),
    "DOCTORAL": Page("DOCTORAL"),
    "INTERN": Page("INTERN"),
    "ORGANISATION": Page("ORGANISATION"),
    "01_Admin_Logs.py": Page(
        "01_Admin_Logs.py"
    ),  # Simule le fichier mentionné par l'utilisateur
    "PageInvalide": "Ceci n'est pas une page valide car il n'a pas de fonction app()",
}

# --- Fonctions de Contrôle d'Accès ---


def is_valid_page(page_name):
    """
    Vérifie si la page demandée est un objet Page valide et a une méthode 'app()'.
    """
    page = PAGES.get(page_name)
    return hasattr(page, "app") and callable(getattr(page, "app"))


def check_access(user_role, page_name):
    """
    Cette fonction implémente le blocage anti-triche et la validation des pages.
    """
    if not is_valid_page(page_name):
        print(f"🚫 Accès refusé : La page '{page_name}' est invalide ou n'existe pas.")
        log_access_denied(user_role, page_name)
        return False

    allowed_pages = ROLE_ACCESS.get(user_role, [])

    if page_name in allowed_pages:
        print(f"✅ L'utilisateur '{user_role}' peut accéder à la page '{page_name}'.")
        return True
    else:
        print(
            f"🚫 Accès refusé : L'utilisateur '{user_role}' n'a pas les droits pour accéder à la page '{page_name}'."
        )
        log_access_denied(user_role, page_name)
        return False


def get_filtered_menu(user_role):
    """
    Retourne la liste des pages qu'un utilisateur peut voir dans son menu.
    """
    # Récupère les pages autorisées pour le rôle, sinon une liste vide
    allowed_pages = ROLE_ACCESS.get(user_role, [])
    # Filtre les pages pour s'assurer qu'elles sont valides (ont une fonction app())
    filtered_menu = [page for page in allowed_pages if is_valid_page(page)]
    return filtered_menu


def log_access_denied(user_role, page_name):
    """
    Enregistre les tentatives d'accès refusé dans le fichier de log.
    """
    logging.info(f"Tentative d'accès refusé : Rôle='{user_role}', Page='{page_name}'")


# --- Démonstration du Système ---
if __name__ == "__main__":
    print("--- Démonstration pour un utilisateur 'PATIENT' ---")
    patient_role = "PATIENT"

    # 1. Menus filtrés automatiquement selon le rôle
    menu_patient = get_filtered_menu(patient_role)
    print(f"Menu pour le rôle '{patient_role}': {menu_patient}")
    print("-" * 20)

    # 2. Blocage anti-triche
    print("Tentative d'accès à des pages...")
    check_access(patient_role, "PATIENT")  # Accès autorisé
    check_access(patient_role, "MESSAGES")  # Accès autorisé
    check_access(patient_role, "ADMIN")  # Accès refusé
    check_access(patient_role, "01_Admin_Logs.py")  # Accès refusé, simulant l'URL
    check_access(patient_role, "PageInvalide")  # Accès refusé, page invalide

    print("\n--- Démonstration pour un utilisateur 'ADMIN' ---")
    admin_role = "ADMIN"

    # 1. Menus filtrés automatiquement selon le rôle
    menu_admin = get_filtered_menu(admin_role)
    print(f"Menu pour le rôle '{admin_role}': {menu_admin}")
    print("-" * 20)

    # 2. Blocage anti-triche
    print("Tentative d'accès à des pages...")
    check_access(admin_role, "DOCTOR")  # Accès autorisé
    check_access(admin_role, "ORGANISATION")  # Accès autorisé

    print("\n--- Vérification des logs ---")
    print(
        "Les tentatives d'accès refusé ont été enregistrées dans le fichier 'logs/app.log'."
    )
    print("Exemple de contenu du log :")
    with open("logs/app.log", "r") as log_file:
        for line in log_file.readlines():
            print(line.strip())
