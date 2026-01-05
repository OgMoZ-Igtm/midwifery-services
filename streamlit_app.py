import streamlit as st
import time

# =========================================================================
# 1. LOGIQUE DE ROUTAGE ET DE RÔLE (Simule dashboard_router.py)
# =========================================================================

# Définition des points d'entrée du tableau de bord principal par rôle
DASHBOARD_ENTRYPOINTS = {
    "admin": "form_admin_dashboard",
    "midwife": "form_midwife_dashboard",
    "doctor": "form_doctor_dashboard",
    "nurse": "form_nurse_dashboard",
    "patient": "form_patient_dashboard",
    "intern": "form_intern_dashboard",
    "doctoral": "form_doctoral_dashboard",
    "guest": "form_guest_dashboard",
}

# 🚀 Menus enrichis, organisés par rôle (Simplifié pour la démo)
ROLE_MENU_MAP = {
    "admin": [
        {
            "label": "Dashboard Admin",
            "icon": "👑",
            "module": "form_admin_dashboard",
            "theme": "Navigation",
        },
        {
            "label": "Gestion Utilisateurs",
            "icon": "🛠️",
            "module": "form_user_management",
            "theme": "Outils & Gestion",
        },
        {
            "label": "Logs Système",
            "icon": "📊",
            "module": "form_admin_logs",
            "theme": "Audit & Logs",
        },
    ],
    "midwife": [
        {
            "label": "Dashboard Sage-Femme",
            "icon": "🍼",
            "module": "form_midwife_dashboard",
            "theme": "Navigation",
        },
        {
            "label": "Suivi Grossesse",
            "icon": "🤰",
            "module": "form_pregnancy_tracking",
            "theme": "Suivi Médical",
        },
        {
            "label": "Soins Postnataux",
            "icon": "👶",
            "module": "form_postnatal_care",
            "theme": "Suivi Médical",
        },
    ],
    "patient": [
        {
            "label": "Mon Dashboard",
            "icon": "🧍",
            "module": "form_patient_dashboard",
            "theme": "Navigation",
        },
        {
            "label": "Rendez-vous",
            "icon": "🗓️",
            "module": "form_appointments",
            "theme": "Gestion Personnelle",
        },
        {
            "label": "Mon Profil",
            "icon": "👤",
            "module": "form_profile",
            "theme": "Gestion Personnelle",
        },
    ],
    "guest": [
        {
            "label": "Accueil Invité",
            "icon": "🌐",
            "module": "form_guest_dashboard",
            "theme": "Navigation",
        },
        {
            "label": "À Propos",
            "icon": "❓",
            "module": "form_qui_sommes_nous",
            "theme": "Informations",
        },
    ],
    # Menu général utilisé si le rôle n'est pas spécifié
    "general": [
        {
            "label": "Tableau de bord Général",
            "icon": "🏠",
            "module": "form_dashboard",
            "theme": "Navigation",
        },
    ],
}


def get_dashboard_module(role):
    """Récupère le module par défaut du tableau de bord pour le rôle donné."""
    return DASHBOARD_ENTRYPOINTS.get(role, "form_dashboard")


def get_menu_for_role(role):
    """Retourne la liste complète des éléments de menu pour le rôle donné."""
    return ROLE_MENU_MAP.get(role, ROLE_MENU_MAP.get("general", []))


def get_icon_for_role(role):
    """Récupère l'icône principale pour le rôle donné."""
    icons = {
        "admin": "👑",
        "midwife": "🍼",
        "doctor": "🧑‍⚕️",
        "nurse": "💉",
        "patient": "🧍",
        "intern": "🧠",
        "doctoral": "🎓",
        "guest": "👤",
    }
    return icons.get(role, "🏠")


# =========================================================================
# 2. MOCK DES FONCTIONS DES FORMULAIRES (Simule modules/forms)
# =========================================================================


# Les fonctions de formulaires réelles se trouveraient dans des modules Python distincts.
def mock_form_content(module_name):
    """Affiche le contenu simulé pour un module donné."""
    st.header(
        f"{get_icon_for_role(st.session_state['role'])} {module_name.replace('form_', '').replace('_', ' ').capitalize()}"
    )
    st.markdown(
        f"""
        Ceci est le contenu du formulaire `{module_name}`.

        Ce contenu est accessible au rôle : **{st.session_state['role'].capitalize()}**.
        
        ---
        Ici se trouveraient les widgets Streamlit spécifiques (champs de saisie, tableaux, graphiques, etc.) pour ce module.
    """
    )


# Mappe les noms de modules à la fonction de rendu simulée
FORM_RUNNERS = {
    name: lambda n=name: mock_form_content(n) for name in DASHBOARD_ENTRYPOINTS.values()
}
# Ajoute les modules de menu pour qu'ils soient exécutables
for menu_list in ROLE_MENU_MAP.values():
    for item in menu_list:
        if item["module"] not in FORM_RUNNERS:
            FORM_RUNNERS[item["module"]] = lambda n=item["module"]: mock_form_content(n)


# =========================================================================
# 3. GESTION DE LA SESSION ET DU FLUX PRINCIPAL (Simule app.py)
# =========================================================================


def init_session_state():
    """Initialise l'état de la session (simule supabase_client.py)"""
    if "is_initialized" not in st.session_state:
        # Rôle initial (changez ceci pour tester d'autres rôles : 'admin', 'patient', etc.)
        st.session_state["role"] = "midwife"
        st.session_state["selected_module"] = get_dashboard_module(
            st.session_state["role"]
        )
        st.session_state["is_initialized"] = True


def load_and_run_module(module_name):
    """Exécute la fonction de rendu pour le module sélectionné (simule module_loader.py)"""
    if module_name in FORM_RUNNERS:
        FORM_RUNNERS[module_name]()
    else:
        st.error(
            f"Le module '{module_name}' est introuvable ou n'a pas de fonction de rendu associée."
        )
        st.info(
            "Veuillez vous assurer que le module est correctement importé et mappé dans FORM_RUNNERS."
        )


# --- DÉMARRAGE DE L'APPLICATION ---

# 1. Initialisation
init_session_state()
role = st.session_state["role"]

# 2. Affichage principal d'accueil
st.title(f"Application Clinique - Rôle : {role.capitalize()}")
st.info(
    f"Votre rôle actuel est **{role.upper()}**. Le menu ci-contre s'y adapte automatiquement."
)

# 3. Rendu de la barre latérale basée sur le rôle
menu_items = get_menu_for_role(role)
st.sidebar.markdown(f"# {get_icon_for_role(role)} Menu {role.capitalize()}")

# 🧠 Regroupement par thème
grouped = {}
for item in menu_items:
    # Utilise "Navigation" si le thème n'est pas défini (via la clé 'theme' ajoutée ci-dessus)
    theme = item.get("theme", "Divers")
    grouped.setdefault(theme, []).append(item)

# Affichage des sections et des boutons
for theme, items in grouped.items():
    st.sidebar.markdown(f"--- \n ### {theme}")
    for item in items:
        # Si le bouton est cliqué, met à jour l'état du module sélectionné
        if st.sidebar.button(f"{item['icon']} {item['label']}", key=item["module"]):
            st.session_state["selected_module"] = item["module"]
            # Force un re-run immédiat pour afficher le nouveau module
            st.rerun()

# 4. Exécution du module sélectionné
selected_module = st.session_state["selected_module"]
load_and_run_module(selected_module)
