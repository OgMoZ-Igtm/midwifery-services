# main.py
import streamlit as st
import os
from modules import Login, Home
from utils.navigation import display_menus, load_menu_mapping
from utils.logger import log_action, log_debug
from utils.session import init_session_state

# Initialisation de la session
init_session_state(
    {
        "authenticated": False,
        "current_page": None,
        "username": None,
        "role": None,
        "init_logged": False,
        "init_done": False,
    }
)

# Logging unique par session
if not st.session_state.init_logged:
    log_debug("Initialisation du projet réussie.")
    st.session_state.init_logged = True

# Impression unique du contexte
if not st.session_state.init_done:
    print("📂 Working dir:", os.getcwd())
    print("📑 Menu file exists:", os.path.exists("utils/menu_mapping.json"))
    st.session_state.init_done = True

# Configuration de la page
st.set_page_config(page_title="Midwifery Tool", page_icon="👩‍🍼", layout="wide")


def main():
    # Message de bienvenue selon le rôle
    if st.session_state.role == "Midwife":
        st.success("Bienvenue, Midwife.")
    elif st.session_state.role:
        st.info(f"Bienvenue, {st.session_state.role}.")
    else:
        st.warning("⚠️ Le rôle n’a pas été défini.")

    # Étape 1 : Login
    if not st.session_state.authenticated:
        Login.login()
    else:
        # Étape 2 : Accueil
        Home.page_home()

    # Déconnexion
    if st.sidebar.button("🚪 Se déconnecter"):
        log_action(st.session_state.username, st.session_state.role, "Déconnexion")
        st.session_state.clear()
        st.rerun()


# Appel de la fonction principale
if __name__ == "__main__":
    main()
