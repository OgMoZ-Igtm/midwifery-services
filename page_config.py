# Fichier: page_config.py

# --- Fonctions de rendu factices pour l'exemple ---
# Ces fonctions simulent le rendu des pages/formulaires réels de l'application.
# Elles seront appelées par la fonction de navigation de Streamlit.
import streamlit as st


def render_birth_plan():
    """Simule le rendu du formulaire Plan de Naissance."""
    st.title("Plan de Naissance")
    st.info(
        "Ceci est le contenu du formulaire 'Plan de Naissance'. Accessible aux Sages-Femmes et Admins."
    )


def render_vitals_signs():
    """Simule le rendu du formulaire Signes Vitaux."""
    st.title("Signes Vitaux")
    st.info(
        "Ceci est le contenu du formulaire 'Signes Vitaux'. Accessible à plusieurs rôles."
    )


def render_admin_tools():
    """Simule le rendu des outils d'administration."""
    st.title("Outils d'Administration")
    st.info("Ceci est le panneau réservé aux administrateurs.")


def render_midwife_dashboard():
    """Simule le rendu du Tableau de bord Sages-Femmes."""
    st.title("Tableau de Bord Sages-Femmes")
    st.success("Bienvenue ! C'est votre page d'accueil par défaut.")


def render_login_form():
    """Simule le rendu de la page de connexion."""
    st.title("Connexion à l'Application")
    # La vraie logique de connexion sera dans app.py
    st.info("Veuillez entrer vos identifiants pour continuer.")


# --------------------------------------------------

# Carte d'aiguillage des tableaux de bord par défaut (répond à votre question 1)
# Cette carte est utilisée pour déterminer la page d'atterrissage après la connexion.
DASHBOARD_MAP = {
    "Midwife": "birth_plan",
    "Doctor": "vital_signs",  # Le Docteur commence peut-être directement par les signes vitaux
    "Admin": "admin_tools",
    "Secretary": "birth_plan",  # La Secrétaire atterrit sur la création de plans
    "Nurse": "vital_signs",
    "guest": "login_page",
}

# Définition de la carte des pages complète (FULL_PAGE_MAP) avec les rôles autorisés.
# C'est la source unique de vérité pour toutes les pages de l'application.
FULL_PAGE_MAP = {
    # 1. PAGE D'ACCUEIL (Dashboard par défaut pour Midwife)
    "midwife_dashboard": {
        "label": "Tableau de Bord",
        "icon": "🏠",
        "group": "Accueil",
        "renderer": render_midwife_dashboard,
        "roles": ["Midwife", "Doctor", "Secretary", "Nurse", "Admin"],
    },
    # 2. PAGES SPÉCIFIQUES (Formulaires)
    "birth_plan": {
        "label": "Plan de Naissance",
        "icon": "👶",
        "group": "Spécifiques",
        "renderer": render_birth_plan,
        "roles": ["Midwife", "Secretary", "Admin"],
    },
    "vital_signs": {
        "label": "Signes Vitaux",
        "icon": "💖",
        "group": "Partagés",
        "renderer": render_vitals_signs,
        "roles": ["Midwife", "Doctor", "Nurse", "Admin"],
    },
    # 3. PAGES D'ADMINISTRATION
    "admin_tools": {
        "label": "Outils Admin",
        "icon": "⚙️",
        "group": "Administration",
        "renderer": render_admin_tools,
        "roles": ["Admin"],
    },
    # 4. PAGE DE CONNEXION (Accessible uniquement avant l'authentification)
    "login_page": {
        "label": "Connexion",
        "icon": "🔑",
        "group": "Authentification",
        "renderer": render_login_form,
        "roles": ["guest"],
    },
    # Ajoutez ici tous les autres render_FORMULAIRE / render_PAGE
}

# Ajoutez ici tous les autres render_FORMULAIRE / render_PAGE


# # # Exemple de structure
# FULL_PAGE_MAP = {
#     "midwife_dashboard": {
#         "label": "Tableau de Bord",
#         "icon": "🏠",
#         "group": "Accueil",
#         "renderer": render_midwife_dashboard,
#         "roles": ["Midwife", "Admin", "Doctor"], # Rôles autorisés
#     },
#     "patient_file": {
#         "label": "Dossier Patient",
#         "icon": "📄",
#         "group": "Spécifiques",
#         "renderer": render_patient_file,
#         "roles": ["Midwife", "Doctor", "Admin"], # Rôles autorisés
#     },
#     "vital_signs": {
#         "label": "Signes Vitaux",
#         "icon": "💖",
#         "group": "Spécifiques",
#         "renderer": render_vitals_signs,
#         "roles": ["Midwife", "Nurse", "Admin"], # Rôles autorisés
#     },
#     "admin_tools": {
#         "label": "Outils Admin",
#         "icon": "⚙️",
#         "group": "Partagés",
#         "renderer": render_admin_tools,
#         "roles": ["Admin"], # SEULEMENT Admin
#     },
#     "login_page": {
#         "label": "Connexion",
#         "icon": "🔑",
#         "group": "Accueil",
#         "renderer": render_login_form,
#         "roles": ["guest"], # SEULEMENT les invités
#     },
#     # ... et ainsi de suite pour TOUTES les autres pages de l'application.
# }
