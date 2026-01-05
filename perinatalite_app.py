# ⚠️ import cassé : streamlit as st
# ⚠️ import cassé : os
# ⚠️ import cassé : json
# ⚠️ from datetime import datetime

# Import du module de sécurité (assurez-vous que ce fichier existe dans modules/utils/)
# Les fonctions nous permettent de savoir quel rôle peut voir quoi.
from modules.utils.security import (
    get_packs_for_role,
    est_autorise,
    log_action,
    get_menu_mapping,
)

# --- Fausse Base de Données (Simulée) ---
# En production, ces données seraient dans une base de données sécurisée
# (Firestore, etc.)
USER_DB = {
    # Rôle: Admin (accès complet)
    "alice.admin": {
        "password": "admin",
        "role": "admin",
        "permissions": [
            "read_record",
            "write_record",
            "access_phi",
            "schedule_apt",
            "view_reports",
            "edit_docs",
            "send_message",
            "access_lms",
        ],
    },
    # Rôle: Sage-femme (Midwife)
    "sara.midwife": {
        "password": "midwife",
        "role": "midwife",
        "permissions": ["read_record", "schedule_apt", "read_docs", "send_message"],
    },
    # Rôle: Étudiant (Student)
    "theo.student": {
        "password": "student",
        "role": "student",
        "permissions": ["read_docs", "access_lms"],
    },
    # Rôle: Patient (accès très limité)
    "pat.patient": {
        "password": "patient",
        "role": "patient",
        "permissions": ["schedule_apt", "read_docs"],
    },
}

# --- Configuration de la Page Streamlit ---
st.set_page_config(
    page_title="Système de Gestion Périnatale Sécurisé",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Utilisation de Tailwind CSS via un style interne pour une meilleure
# esthétique
st.markdown(
    """
<style>
    .st-emotion-cache-18ni7ap { padding-top: 2rem; } /* Centrer le contenu Streamlit */
    .st-emotion-cache-vk3wp9 { background-color: #f7f7f7; } /* Couleur de fond */
    .st-emotion-cache-czk5ad { border-radius: 12px; } /* Coins arrondis pour les conteneurs */
    .st-emotion-cache-12fmwca { max-width: 100%; padding: 1rem 2rem; } /* Layout fluide */
    h1 { color: #3b82f6; } /* Couleur principale pour les titres */
</style>
""",
    unsafe_allow_html=True,
)

# --- État de Session (Initialisation) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.user_permissions = []
    st.session_state.current_page = "dashboard"  # Page de destination par défaut

# --- Fonctions d'Authentification et de Déconnexion ---


def authenticate(username, password):
    """Simule la vérification des identifiants utilisateur."""
    if username in USER_DB and USER_DB[username]["password"] == password:
        user_data = USER_DB[username]
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = user_data["role"]
        st.session_state.user_permissions = user_data["permissions"]

        # Audit: Enregistrement de la connexion réussie
        log_action(username, "LOGIN_SUCCESS", f"Rôle: {user_data['role']}")
        return True

    # Audit: Enregistrement de la tentative de connexion échouée
    log_action(username, "LOGIN_FAILED", "Mot de passe ou utilisateur incorrect.")
    return False


def logout():
    """Déconnecte l'utilisateur et réinitialise l'état de la session."""
    if st.session_state.username:
        log_action(st.session_state.username, "LOGOUT", "Déconnexion de l'application.")

    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.user_permissions = []
    st.session_state.current_page = "dashboard"
    st.rerun()


# --- Interface de Connexion (Login) ---


def show_login_page():
    """Affiche l'interface de connexion."""
    st.title("Connexion au Système Périnatal 🏥")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.info(
            "Utilisateurs de Test:\n\n- **Admin** (admin/admin)\n- **Sage-femme** (sara.midwife/midwife)\n- **Étudiant** (theo.student/student)\n- **Patient** (pat.patient/patient)"
        )

    with col2:
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur", placeholder="admin")
            password = st.text_input(
                "Mot de passe", type="password", placeholder="admin"
            )
            submitted = st.form_submit_button("Se Connecter", type="primary")

            if submitted:
                if authenticate(username, password):
                    st.success("Connexion réussie! Redirection...")
                    st.rerun()
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect.")


# --- Interface de l'Application Principale (Dashboard et Routage) ---


# Fonction pour simuler le rendu des pages spécifiques
def render_page_content(page_id):
    """Simule l'affichage du contenu spécifique à chaque pack."""
    st.subheader(f"Contenu du Pack : {page_id.replace('_', ' ').title()}")

    if page_id == "patient_records":
        st.markdown(
            f"""
        ### 📁 Dossiers Patients Périnataux
        *Role actuel: **{st.session_state.role.upper()}***

        Seul les utilisateurs avec les permissions **'read_record'** ET **'access_phi'** et ayant un accès par rôle peuvent voir l'intégralité de cette page.

        ---
        **Permissions de l'utilisateur:** `{', '.join(st.session_state.user_permissions)}`

        """
        )
        st.warning(
            "⚠️ Ceci est une page sécurisée, uniquement pour le personnel autorisé."
        )
    elif page_id == "dashboard":
        st.subheader(
            f"Bienvenue, {
                st.session_state.username} ({
                st.session_state.role.title()})!"
        )
        st.metric("Total de Patients Suivis", 420)
        st.metric("Rendez-vous Aujourd'hui", 15)
        st.info("Utilisez la barre latérale pour naviguer vers vos outils autorisés.")
    else:
        st.info(f"Page en construction pour le pack '{page_id}'.")


def show_main_app():
    """Affiche la navigation sécurisée et le contenu de la page active."""

    # 1. Configuration de la Barre Latérale (Menu)
    with st.sidebar:
        st.header(f"Menu - {st.session_state.role.title()}")

        # Récupère les packs autorisés pour le rôle actuel
        allowed_packs = get_packs_for_role(st.session_state.role)

        # Construction des boutons de navigation
        for pack in allowed_packs:
            pack_id = pack["id"]

            # Vérification de l'autorisation granulaire avant d'afficher le
            # bouton
            is_authorized = est_autorise(
                st.session_state.role, pack_id, st.session_state.user_permissions
            )

            # Si le pack est listé pour le rôle ET que l'utilisateur a les
            # permissions requises
            if is_authorized:
                # Création du bouton pour changer de page
                if st.button(
                    f'{pack["icon"]} {pack["label"]}',
                    key=f"nav_{pack_id}",
                    width='stretch',
                ):
                    st.session_state.current_page = pack_id
                    log_action(
                        st.session_state.username,
                        "NAVIGATE",
                        f"Accès à la page: {pack_id}",
                    )
                    # Pas de st.rerun ici, car le changement de
                    # st.session_state.current_page est suffisant
            else:
                # Affichage d'un bouton désactivé si l'accès par permission est
                # refusé
                st.button(
                    f'❌ {pack["label"]} (Accès Refusé)',
                    disabled=True,
                    width='stretch',
                )

        st.divider()
        st.button(
            "Déconnexion", on_click=logout, type="secondary", width='stretch'
        )
        st.markdown(
            f'<p style="font-size: 0.8em; color: #888;">Utilisateur: {st.session_state.username}</p>',
            unsafe_allow_html=True,
        )

    # 2. Rendu du Contenu Principal

    current_page_id = st.session_state.current_page

    # Vérification d'autorisation finale avant le rendu du contenu
    # Cette vérification est essentielle pour protéger l'URL ou les liens
    # directs
    final_check = est_autorise(
        st.session_state.role, current_page_id, st.session_state.user_permissions
    )

    if final_check:
        render_page_content(current_page_id)
    else:
        # Cas où l'utilisateur tente d'accéder à une page non autorisée (ex:
        # via un lien direct ou une erreur)
        st.error(
            f"Accès refusé. Vous n'avez pas l'autorisation d'accéder au pack '{current_page_id}'."
        )
        log_action(
            st.session_state.username,
            "ACCESS_DENIED",
            f"Tentative d'accès non autorisé à: {current_page_id}",
        )


# --- Point d'Entrée Principal ---
if st.session_state.logged_in:
    show_main_app()
else:
    show_login_page()
