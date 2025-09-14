import streamlit as st
import streamlit.components.v1 as components
import os
from streamlit_option_menu import option_menu
from datetime import datetime
import uuid
import pandas as pd


if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


# Initialiser l'état de la session si les variables n'existent pas
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# Dictionnaire des mots de passe pour chaque rôle
# C'est une méthode simple pour la démonstration. Dans un cas réel, il
# faudrait utiliser un système d'authentification plus robuste (ex: base de données).
user_passwords = {
    "ADMIN": "Admin",
    "MIDWIFE": "Midwife",
    "NURSE": "Nurse",
    "DOCTOR": "Doctor",
    "INTERN": "Intern",
    "STUDENT": "Student",
    "PATIENT": "Patient",
    "DOCTORAL": "Doctoral",
}


# Fonction pour l'authentification de l'utilisateur
def authenticate_user(username, password):
    username_upper = username.upper()
    if username_upper in user_passwords and user_passwords[username_upper] == password:
        st.session_state.authenticated = True
        st.session_state.user_name = username
        st.session_state.user_role = username_upper
        st.success(f"Connexion réussie ! Bienvenue, {username} !")
        st.balloons()
        return True
    else:
        st.error("Nom d'utilisateur ou mot de passe incorrect.")
        return False


# Fonction principale pour rendre le contenu de la page
def render():
    if not st.session_state.authenticated:
        st.markdown(
            """
            <style>
            .st-emotion-cache-1830b56 {
                display: none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.title("Bienvenue sur l'Espace Midwifery Services")
        st.subheader("Veuillez vous connecter pour accéder à l'application.")

        # Champs de formulaire pour la connexion
        login_container = st.container(border=True)
        with login_container:
            st.markdown("### Connexion")
            username = st.text_input(
                "Nom d'utilisateur", placeholder="Entrez votre rôle (ex: Admin)"
            )
            password = st.text_input(
                "Mot de passe", type="password", placeholder="Entrez votre mot de passe"
            )

            if st.button("Se connecter"):
                authenticate_user(username, password)
    else:
        # Afficher la page HTML avec la barre latérale une fois connecté
        st.title(
            f"Bienvenue, {st.session_state.user_name} ({st.session_state.user_role})"
        )
        st.success("Vous êtes maintenant connecté. Voici votre tableau de bord.")

        # Lire et afficher le fichier HTML
        try:
            with open("packs/ADMIN/progress_bar.html", "r", encoding="utf-8") as f:
                html_code = f.read()
            components.html(html_code, height=600, scrolling=True)
        except FileNotFoundError:
            st.error(
                "Le fichier HTML 'progress_bar.html' est introuvable. Veuillez vous assurer qu'il se trouve dans le dossier packs/ADMIN/."
            )


if __name__ == "__main__":
    render()
