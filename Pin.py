import streamlit as st
import modules.Login as Login
import modules.Home as Home
from utils.navigation import display_menus, load_menu_mapping
from utils.logger import log_action
from utils.permissions import can_access
import importlib.util
import os

st.set_page_config(page_title="Midwifery Tool", page_icon="👩‍🍼", layout="wide")

# --- Initialisation de l'état de session ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_page" not in st.session_state:
    st.session_state.current_page = None
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None


def load_module_from_file(file_path):
    """Charge un module Python à partir de son chemin absolu"""
    try:
        spec = importlib.util.spec_from_file_location("dynamic_page", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement de {file_path} : {e}")
        return None


def main():
    if not st.session_state.authenticated:
        Login.page_connexion()
    else:
        role = st.session_state.get("role", "")
        st.sidebar.info(f"Rôle actuel dans la session : {st.session_state.role}")

        display_menus(role)
        current_page = st.session_state.get("current_page")

        if current_page:
            try:
                # Vérification des autorisations et autres logiques...
                mapping = load_menu_mapping()
                authorized = False
                for entries in mapping.values():
                    for entry in entries:
                        if entry["file"] == current_page and role in entry.get(
                            "roles", []
                        ):
                            authorized = True
                            break
                    if authorized:
                        break

                if not authorized:
                    st.error("⛔ Accès interdit à cette page pour votre rôle.")
                    return

               if not can_access(st.session_state.role, "DOCTOR", action="view"):
                st.warning("⛔ Accès refusé à cette section pour votre rôle.")
                return

                # --- NOUVELLE LOGIQUE DE CHARGEMENT DE PAGE ---
                file_path = os.path.join(os.getcwd(), current_page)
                with open(file_path, "r") as f:
                    code = f.read()

                # Exécute le code du formulaire
                exec(code, globals())

                # Appelle la fonction de rendu (render) du formulaire
                if "render" in globals() and callable(globals()["render"]):
                    globals()["render"]()
                else:
                    st.warning(
                        f"⚠️ La page {current_page} ne contient pas de fonction 'render'."
                    )

            except Exception as e:
                st.error(f"Erreur de chargement de la page : {e}")

        else:
            Home.page_home()

        if st.sidebar.button("🚪 Se déconnecter"):
            log_action(st.session_state.username, role, "Déconnexion")
            st.session_state.clear()
            st.rerun()


if __name__ == "__main__":
    main()
