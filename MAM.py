# =========================================================
# 📦 FICHIER UNIQUE : MATERNITÉ CRIE APP - VERSION FINALE
# =========================================================

# ---------------------------------------------------------
# 1. CONFIGURATION, IMPORTS ET ENVIRONNEMENT
# ---------------------------------------------------------

import streamlit as st
import importlib
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from supabase import create_client, Client

# Configuration de la page doit être la première commande Streamlit
st.set_page_config(page_title="Plateforme Maternité Crie Simplifiée", layout="wide")

# Chargement des variables d'environnement
load_dotenv()


# ---------------------------------------------------------
# 2. MOCKS & CONSTANTES SIMULÉES (DATA & PLACEHOLDERS)
# ---------------------------------------------------------

# --- MOCK: USER_PASSWORDS
USER_PASSWORDS = {
    "MIDWIFE": "Test!1234@",
    "ADMIN": "Test!1234@",
    "NURSE": "Test!1234@",
    "DOCTOR": "Test!1234@",
    "INTERN": "Test!1234@",
    "STUDENT": "Test!1234@",
    "PATIENT": "Test!1234@",
    "DOCTORAL": "Test!1234@",
    # Mot de passe pour accéder au profil patient
    "PATIENT_PASSWORD": "P@tientAccess1!",
}

# ---------------------------------------------------------
# 3. FONCTIONS UTILITAIRES DE BASE (NON-UI / DONNÉES)
# ---------------------------------------------------------


def load_static_asset(filename):
    """
    Retourne le chemin absolu vers un fichier statique (pour st.image)
    ou le chemin relatif (pour st.markdown et HTML).
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "static", filename)
    return file_path


def validate_project(username, password):
    """Simule la validation des identifiants."""
    user_role = username.upper().replace(" ", "")
    st.session_state["role"] = user_role

    if USER_PASSWORDS.get(user_role) == password:
        # Simulation: Enregistrer l'heure de la connexion actuelle avant de valider
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Simuler la "dernière connexion" à partir de la session ou d'une valeur par défaut
        last_login = st.session_state.get("current_login", "Première connexion")
        st.session_state["last_login"] = last_login
        st.session_state["current_login"] = current_time
        return True
    return False


def get_greeting():
    """Ajoute les salutations selon l'heure du jour."""
    now = datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        return "Bonjour"
    elif 12 <= hour < 18:
        return "Bon après-midi"
    else:
        return "Bonsoir"


# ---------------------------------------------------------
# 4. RENDU DES COMPOSANTS UI (Éléments réutilisables)
# ---------------------------------------------------------

# Global CSS pour le style (identique)
st.markdown(
    """
    <style>
    /* NOUVEAU: Style des boutons Streamlit masqués dans le header */
    .nav-bar .stButton > button {
        background-color: transparent !important;
        border: none !important;
        padding: 8px 14px !important;
        color: #333 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        margin: 0 !important;
        height: auto !important;
    }
    .nav-bar .stButton > button:hover {
        background-color: #f0e0d6 !important; 
        color: #7d4f3b !important;
    }
    .active-link-button > button {
        background-color: #ba68c8 !important; 
        color: white !important; 
        font-weight: 700 !important;
        box-shadow: 0 2px 5px rgba(186,104,200,0.5) !important;
    }
    /* Styles pour le Login */
    .login-container {
        max-width: 800px; margin: 50px auto; padding: 30px;
        background-color: #fff8f0; 
        border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid #f0e0d6;
    }
    .login-form-card {
        padding: 25px; background-color: white; border-radius: 10px;
        box-shadow: 0 4px 15px rgba(186, 104, 200, 0.1);
        border-left: 5px solid #ba68c8;
    }
    .stButton>button {
        width: 100%; background-color: #ba68c8; color: white;
        border-radius: 8px; border: none; padding: 10px; font-weight: bold;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #9c4d9e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_public_header():
    """Affiche l'en-tête de navigation horizontal et fixe."""
    themes = {
        "Notre mission": "🎯",
        "Notre vision": "🌈",
        "Qui sommes-nous": "🧑‍🤝‍🧑",
        "Les Papotines": "🧵",
        "Organisation": "🏢",
        "Liens utiles": "🔗",
        "Pour nous joindre": "📞",
        "Infos": "ℹ️",
        "FAQ": "❓",
    }

    num_themes = len(themes)
    cols = st.columns(num_themes)

    st.markdown("<div class='nav-bar'>", unsafe_allow_html=True)
    active_page = st.session_state.get("info_page", "Notre mission")

    for i, (label, icon) in enumerate(themes.items()):
        with cols[i]:
            if st.button(
                f"{icon} {label}", key=f"nav_btn_{label}", help=f"Aller à {label}"
            ):
                st.session_state["info_page"] = label
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='padding-top: 5rem;'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# 5. RENDU DES PAGES COMPLÈTES (Vues principales)
# ---------------------------------------------------------


def render_info_section():
    """Rend le contenu dynamique de la section d'information publique."""
    if "info_page" not in st.session_state:
        st.session_state["info_page"] = "Notre mission"

    current_page = st.session_state["info_page"]

    st.markdown(
        f"<a name='{current_page.replace(' ', '_')}></a>", unsafe_allow_html=True
    )
    st.markdown(f"## {current_page}", unsafe_allow_html=True)

    if current_page == "Notre mission":
        st.write(
            "Notre mission est de tisser des liens solides entre les soins de maternité et la richesse culturelle crie, assurant une expérience de naissance empreinte de respect et de dignité."
        )
    elif current_page == "Les Papotines":
        st.write(
            "Le fil des Papotines, c'est un espace de parole, de partage et de guérison. Ici, les mères peuvent laisser un message, un poème, ou simplement un silence qui résonne avec leurs sœurs."
        )
        st.info("Espace de partage simulé.")
    elif current_page == "Organisation":
        st.write("Section Organisation : Détails sur la structure du projet MSA.")
    else:
        st.write(
            f"Contenu détaillé pour la section **{current_page}** à venir. En attendant, voici un aperçu de l'engagement de la communauté."
        )


def render_login_page():
    """Rend la page de connexion, simplifiée pour l'intégration."""

    st.markdown(
        """
        <div class='login-container'>
            <h1 style='text-align:center; color:#ba68c8;'>
                Bienvenue sur MSA ! 🤝
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_form, col_poem = st.columns([1, 1])

    with col_form:
        st.markdown("<div class='login-form-card'>", unsafe_allow_html=True)
        st.subheader("Connexion sécurisée")

        with st.form("login_form"):
            username = st.text_input(
                "Nom d'utilisateur (Rôle: MIDWIFE, PATIENT, DOCTOR, NURSE, ADMIN...)",
                key="login_username",
            )
            password = st.text_input(
                "Mot de passe (Test!1234@)", type="password", key="login_password"
            )
            submitted = st.form_submit_button("Se connecter ➡️")

            if submitted:
                if validate_project(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = username
                    # st.session_state["role"] est déjà défini dans validate_project
                    st.success("Connexion réussie ! Redirection...")
                    time.sleep(1)
                    st.session_state["main_section"] = "Tableau de bord"
                    st.rerun()
                else:
                    st.error("Identifiants incorrects. Veuillez réessayer.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_poem:
        st.markdown(
            "<div class='poem-card' style='padding: 25px; border: 1px solid #dcdcdc; border-radius: 10px; background-color: #fff4ec;'>",
            unsafe_allow_html=True,
        )
        cree_poem = """
        ---
        ### *Ici commence le souffle du monde.*
        Sous les couvertures de mousse et de ciel,
        une mère crie enlace son enfant,
        et le territoire écoute.
        ---
        """
        st.markdown(cree_poem, unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align:right; margin-top:20px;'>— Inspiré par l'Esprit de Eeyou Istchee</p>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_authenticated_dashboard():
    """
    Rend l'interface utilisateur pour un utilisateur authentifié avec le menu latéral.
    **CORRECTION : Importation dynamique des tableaux de bord et formulaires réactivée.**
    """
    role = st.session_state["role"]
    username_display = st.session_state["user"].capitalize()
    greeting = get_greeting()  # 1) Salutations

    # --- Barre latérale (Point 4 + 2) ---
    with st.sidebar:
        st.title(f"{greeting}, {username_display} 👋")  # 1) Affichage des salutations
        st.markdown("---")

        # 2) Détails de connexion
        st.markdown(
            f"**⏰ Connecté depuis:** {st.session_state.get('current_login', 'N/A')}"
        )
        st.markdown(
            f"**⏳ Dernière connexion:** {st.session_state.get('last_login', 'N/A')}"
        )
        st.markdown("---")

        # 3) Profil du Patient avec mot de passe
        AUTHORIZED_ROLES = ["ADMIN", "DOCTOR", "NURSE", "MIDWIFE"]
        if role in AUTHORIZED_ROLES:
            with st.expander(
                "🚨 Profil du Patient (Accès Sécurisé)",
                expanded=st.session_state.get("patient_expander_open", False),
            ):
                st.session_state["patient_expander_open"] = (
                    True  # Garde ouvert si on y est
                )

                patient_password = st.text_input(
                    "Mot de passe d'accès", type="password", key="patient_access_pwd"
                )

                if patient_password == USER_PASSWORDS["PATIENT_PASSWORD"]:
                    st.session_state["patient_access_granted"] = True
                    st.success(
                        "Accès autorisé. Informations sensibles affichées ci-dessous."
                    )
                    # Ajoutez ici les options spécifiques au profil patient
                    st.markdown("---")
                    st.markdown("### 🧑‍🍼 Fiches Patients")

                    # Utiliser un form pour les actions du sidebar (plus propre)
                    with st.form("patient_access_form", clear_on_submit=False):
                        st.text_input("Rechercher patient", key="patient_search_input")
                        search_submitted = st.form_submit_button("Rechercher 🔍")

                        if search_submitted:
                            st.session_state["main_section"] = "Patient Search"
                            st.rerun()

                elif (
                    patient_password
                ):  # Si le champ n'est pas vide et le mot de passe est incorrect
                    st.session_state["patient_access_granted"] = False
                    st.error("Mot de passe incorrect.")
                else:
                    st.session_state["patient_access_granted"] = False
                    st.info("Entrez le mot de passe pour accéder.")

        # Réinitialiser l'état de l'expander si l'utilisateur quitte
        if st.session_state.get("main_radio_nav") != "Tableau de bord":
            st.session_state["patient_expander_open"] = False

        st.markdown("---")

        st.markdown(f"### 🎛️ Menu {role.capitalize()}")

        # Logique pour éviter de rester bloqué
        if st.session_state.get("main_section") == "Patient Search" and (
            role not in AUTHORIZED_ROLES
            or not st.session_state.get("patient_access_granted")
        ):
            st.session_state["main_section"] = "Accueil"

        if "main_section" not in st.session_state:
            st.session_state["main_section"] = "Accueil"

        main_section = st.radio(
            "🧭 Que souhaitez-vous afficher ?",
            [
                "Accueil",
                "Tableau de bord",
                "Formulaire spécifique",
                "Fonction partagée",
            ],
            key="main_radio_nav",
            index=[
                "Accueil",
                "Tableau de bord",
                "Formulaire spécifique",
                "Fonction partagée",
            ].index(st.session_state.get("main_section", "Accueil")),
        )

        st.session_state["main_section"] = main_section

        # Liste des formulaires spécifiques par rôle (CORRIGÉ ADMIN)
        specific_forms = {
            "MIDWIFE": [
                "forms_midwife/form_birth_plan",
                "forms_midwife/form_postpartum",
                "forms_midwife/form_initial_routine",
                "forms_midwife/form_patient_file",
                "forms_midwife/form_patient_management",
                "forms_midwife/form_midwife_messages",
                "forms_midwife/form_consultation_prenatale",
                "forms_midwife/form_emotional_well_being",
                "forms_midwife/form_incident_report",
                "forms_midwife/form_demographics",
                "forms_midwife/form_prenatal_care",
                "forms_midwife/form_postnatal_care",
                "forms_midwife/form_intrapartum_care",
            ],
            "NURSE": [
                "forms_nurse/form_schedule_nurse",
                "forms_nurse/form_consultation_notes",
                "forms_nurse/form_nurse_shift_report",
                "forms_nurse/form_nursing_notes",
                "forms_nurse/form_nurse_inventory_management",
                "forms_nurse/form_nurse_medicament_admin",
                "forms_nurse/form_vital_signs",
                "forms_nurse/form_followup",
            ],
            "DOCTOR": [
                "forms_doctor/form_doctor_emergency_assessment",
                "forms_doctor/form_medicament_prescription",
                "forms_doctor/form_due_date_calculator",
                "forms_doctor/form_doctor_schedule",
                "forms_doctor/form_medical_report",
                "forms_doctor/form_prescription",
            ],
            "PATIENT": [
                "forms_patient/form_patient_satisfaction_survey",
                "forms_patient/form_patient_symptom",
                "forms_patient/form_patient_appointment_booking",
                "forms_patient/form_patient_communicatient_prefs",
                "forms_patient/form_patient_feedback",
                "forms_patient/form_patient_prescription_request",
                "forms_patient/form_feedback",
                "forms_patient/form_request",
            ],
            "STUDENT": [
                "forms_student/form_observation",
                "forms_student/form_reflection",
            ],
            "GUEST": [
                "forms_guest/form_utility_general_contact",
                "forms_guest/form_utility_service_request",
            ],
            "INTERN": [
                "forms_intern/form_clinical_observation",
                "forms_intern/form_inter_case_study",
                "forms_intern/form_intern_logbook",
                "forms_intern/form_intern_skill_checklist",
                "forms_intern/form_training_log",
            ],
            "DOCTORAL": [
                "forms_doctoral/form_research_note",
                "forms_doctoral/form_doctorant_ethics_submissions",
            ],
            # CORRIGÉ : Utilise le chemin de fichier (dossier/fichier)
            "ADMIN": [
                "forms_admin/form_user_management",
                "forms_admin/form_system_logs_viewer",
                "forms_admin/form_report_dashboard",
                "forms_admin/form_global_settings",
                "forms_admin/form_config_system",
            ],
        }

        shared_buttons = {
            "Agenda": "📅",
            "Calendrier": "🗓️",
            "Messages": "✉️",
            "Chat": "💬",
            "Profil": "👤",
            "Settings": "⚙️",
            "Signup": "📝",
        }

        selected_form = (
            st.selectbox("📄 Choisissez un formulaire", specific_forms.get(role, []))
            if main_section == "Formulaire spécifique"
            else None
        )
        selected_shared = (
            st.selectbox("🌐 Fonction partagée", list(shared_buttons.keys()))
            if main_section == "Fonction partagée"
            else None
        )

        st.markdown("---")
        if st.button("Déconnexion 🚪"):
            st.session_state["authenticated"] = False
            st.session_state["info_page"] = "Notre mission"
            # Nettoyage des variables de connexion
            for key in [
                "main_section",
                "user",
                "role",
                "last_login",
                "current_login",
                "patient_access_granted",
                "patient_expander_open",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # --- Affichage dynamique selon la sélection (IMPORT RÉACTIVÉ) ---
    current_section = st.session_state["main_section"]

    if current_section == "Accueil":
        st.markdown("## 🏠 Bienvenue dans votre espace personnel")
        st.markdown(
            f"Votre rôle est **{role.capitalize()}**. Utilisez le menu latéral pour naviguer."
        )

    elif (
        current_section == "Patient Search"
        and role in AUTHORIZED_ROLES
        and st.session_state.get("patient_access_granted", False)
    ):
        st.markdown("## 🔍 Recherche et Profils Patients")
        st.warning(
            "Ceci est une zone à haute sécurité. Les données patients y sont traitées."
        )
        st.info(
            f"Affichage du profil détaillé du patient: **{st.session_state.get('patient_search_input', 'Non spécifié')}**"
        )

    # Rendu du Tableau de bord (IMPORT RÉACTIVÉ)
    elif current_section == "Tableau de bord":
        st.markdown(f"## 📊 Tableau de bord {role.capitalize()}")
        try:
            # Assurez-vous que le module est accessible (doit être dashboard/dashboard_role.py)
            dashboard_module = importlib.import_module(
                f"dashboard.dashboard_{role.lower()}"
            )
            if hasattr(dashboard_module, "render_dashboard"):
                dashboard_module.render_dashboard()
            else:
                st.warning(
                    "⚠️ Le tableau de bord trouvé ne contient pas de fonction `render_dashboard()`."
                )
        except ModuleNotFoundError:
            st.error(
                f"❌ Module de tableau de bord introuvable: `dashboard.dashboard_{role.lower()}`."
            )
            st.info(
                "Veuillez créer le fichier `dashboard/dashboard_{role.lower()}.py` avec la fonction `render_dashboard()`."
            )

    # Rendu du Formulaire spécifique (IMPORT RÉACTIVÉ)
    elif current_section == "Formulaire spécifique" and selected_form:
        # Nettoyage du nom pour l'affichage
        display_name = selected_form.split("/")[-1].replace("_", " ").capitalize()
        st.markdown(f"## 📝 Formulaire Spécifique: {display_name}")
        try:
            # Remplacement des '/' par des '.' pour l'importation (ex: forms_admin/form_... -> forms_admin.form_...)
            module_path = selected_form.replace("/", ".")
            form_module = importlib.import_module(f"modules.{module_path}")
            if hasattr(form_module, "render_form"):
                form_module.render_form()
            else:
                st.warning(
                    "⚠️ Le formulaire trouvé ne contient pas de fonction `render_form()`."
                )
        except ModuleNotFoundError:
            st.error(f"❌ Formulaire introuvable : `modules.{module_path}`.")
            st.info(
                f"Veuillez créer le fichier `modules/{selected_form}.py` avec la fonction `render_form()`."
            )
        except Exception as e:
            st.error(f"Une erreur s'est produite lors du rendu du formulaire: {e}")
            st.info(
                f"Vérifiez le contenu de votre fichier `modules/{selected_form}.py`."
            )

    # Rendu de la Fonction partagée (IMPORT RÉACTIVÉ)
    elif current_section == "Fonction partagée" and selected_shared:
        st.markdown(f"## 🌐 Fonction Partagée: {selected_shared}")
        try:
            shared_key = selected_shared.lower().replace(" ", "_")
            shared_module = importlib.import_module(f"modules.shared.form_{shared_key}")
            if hasattr(shared_module, "render_form"):
                shared_module.render_form()
            else:
                st.warning(
                    "⚠️ La fonction partagée trouvée ne contient pas de fonction `render_form()`."
                )
        except ModuleNotFoundError:
            st.error(
                f"❌ Fonction partagée introuvable : `modules.shared.form_{shared_key}`"
            )
            st.info(
                f"Veuillez créer le fichier `modules/shared/form_{shared_key}.py` avec la fonction `render_form()`."
            )
        except Exception as e:
            st.error(
                f"Une erreur s'est produite lors du rendu de la fonction partagée: {e}"
            )
            st.info(
                f"Vérifiez le contenu de votre fichier `modules/shared/form_{shared_key}.py`."
            )

    else:
        # Cas par défaut ou après déconnexion/erreur
        st.session_state["main_section"] = "Accueil"
        st.markdown("## 🏠 Bienvenue")
        st.markdown("Veuillez choisir une option dans le menu latéral.")


# ---------------------------------------------------------
# 6. POINT D'ENTRÉE PRINCIPAL DE L'APPLICATION
# ---------------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    # 1. Rendu du tableau de bord authentifié (avec le menu latéral)
    render_authenticated_dashboard()
else:
    # 1. Rendu de l'en-tête public
    show_public_header()
    # 2. Rendu de la section d'information ou de connexion
    if st.session_state.get("info_page", "") != "Connexion":
        render_info_section()
    else:
        render_login_page()
    # 3. Bouton de connexion pour la page d'information
    st.sidebar.markdown("---")
    if st.sidebar.button("Se connecter au Portail 👤", key="sidebar_login"):
        st.session_state["info_page"] = "Connexion"
        st.rerun()
