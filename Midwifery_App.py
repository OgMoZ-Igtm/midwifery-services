import streamlit as st
import time
from datetime import datetime
from typing import Dict, Any, Callable
import os
import sys
import importlib

# --- ATTENTION : Ce bloc de code s'exécute immédiatement au démarrage et peut causer une erreur
# --- si le module n'existe pas ou si Streamlit n'a pas encore initialisé l'UI.
# --- Nous le commentons et utilisons le ROUTING_MAP et la fonction load_form_module.
# module_path = "modules.forms_doctor.form_doctor_dashboard"
# form_module = importlib.import_module(module_path)
# form_module.render_form()

# ------------------------------------------------------------------------------
# 🔧 Fonctions de Simulation (Stubs) & Utilitaires Modulaires
# ------------------------------------------------------------------------------


# Placeholder pour la fonction add_document.
def add_document(collection: str, data: dict):
    # Ceci est une simulation d'une opération de base de données (ex: Firestore)
    print(f"SIMULATION : Ajout à {collection} -> {data}")
    return {"id": "simulated_id", **data}


# NOUVELLE FONCTION: Chargement Dynamique des Modules pour la modularisation
def load_form_module(role: str, form_name: str) -> Callable:
    """
    Tente de charger dynamiquement un module de formulaire.
    Si le module n'est pas trouvé, retourne un rendu de page de placeholder.
    La structure de chemin attendue est 'modules.{role}.{form_name}'.
    """
    base_path = f"modules.{role}.{form_name}"

    try:
        # Assure un rechargement si nécessaire pour le développement
        if base_path in sys.modules:
            importlib.reload(sys.modules[base_path])

        # Le nom du fichier de module est {form_name}.py dans le dossier modules/{role}/
        form_module = importlib.import_module(base_path)

        # Assurez-vous que la fonction de rendu attendue est présente
        if hasattr(form_module, "render_form") and callable(form_module.render_form):
            return form_module.render_form
        else:
            # Si le module est chargé mais n'a pas la bonne fonction, on utilise le placeholder
            st.error(
                f"Erreur de module: La fonction 'render_form' est manquante dans {base_path}."
            )
            title = f"{role.capitalize()} - {form_name.replace('_', ' ').title()} (Fonction manquante)"
            return lambda: render_placeholder_page(f"⚠️ {title}")

    except ModuleNotFoundError:
        # Fallback élégant si le fichier/module n'existe pas encore
        # st.warning(f"Module non trouvé: {base_path}. Affichage du placeholder.")
        title = f"{role.capitalize()} - {form_name.replace('_', ' ').title()}"
        return lambda: render_placeholder_page(f"🏗️ {title}")
    except Exception as e:
        # Erreur générale d'importation (syntaxe, etc.)
        st.error(f"Erreur critique lors du chargement du module {base_path}: {e}")
        return lambda: render_placeholder_page(
            f"❌ Erreur de Module pour {form_name.replace('_', ' ').title()}"
        )


# ------------------------------------------------------------------------------
# 0. CONFIGURATION DES IDS DE PAGE
# ------------------------------------------------------------------------------

# Identifiants de Page Internes (Strings uniques pour toutes les pages implémentées)
PAGE_ID_HOME = "DASHBOARD_MIDWIFE"
PAGE_ID_PRENATAL = "FORM_PRENATAL"
PAGE_ID_POSTNATAL = "FORM_POSTNATAL"
PAGE_ID_PATIENT_MGMT = "PATIENT_MGMT"

# NOUVEAUX IDS pour les autres rôles
PAGE_ID_NURSE_DASH = "DASHBOARD_NURSE"
PAGE_ID_DOCTOR_DASH = "DASHBOARD_DOCTOR"
PAGE_ID_STUDENT_DASH = "DASHBOARD_STUDENT"
PAGE_ID_INTERN_DASH = "DASHBOARD_INTERN"
PAGE_ID_DOCTORAL_DASH = "DASHBOARD_DOCTORAL"
PAGE_ID_PATIENT_HOME = "PATIENT_HOME"
PAGE_ID_ADMIN_DASH = "DASHBOARD_ADMIN"  # NOUVEAU: ID pour le tableau de bord Admin

# Nouveaux FORM IDs pour harmonisation (Spécifiques par Rôle)
# NURSE
PAGE_ID_NURSE_NOTES = "FORM_NURSE_PATIENT_NOTES"
PAGE_ID_NURSE_REPORT = "FORM_NURSE_SHIFT_REPORT"
PAGE_ID_NURSE_INVENTORY = "FORM_NURSE_INVENTORY"

# DOCTOR
PAGE_ID_DOCTOR_PRESCRIPTION = "FORM_DOCTOR_PRESCRIPTION"
PAGE_ID_DOCTOR_SURGERY = "FORM_DOCTOR_SURGERY_PLAN"
PAGE_ID_DOCTOR_CONSULT = "FORM_DOCTOR_CONSULTATION"

# STUDENT
PAGE_ID_STUDENT_OBSERVATION = "FORM_STUDENT_OBSERVATION"
PAGE_ID_STUDENT_QUIZ = "FORM_STUDENT_QUIZ"
PAGE_ID_STUDENT_LOGBOOK = "FORM_STUDENT_LOGBOOK"

# INTERN
PAGE_ID_INTERN_TASK = "FORM_INTERN_TASK_ASSIGN"
PAGE_ID_INTERN_CHECKLIST = "FORM_INTERN_CHECKLIST"
PAGE_ID_INTERN_CASE_STUDY = "FORM_INTERN_CASE_STUDY"

# DOCTORAL
PAGE_ID_DOCTORAL_RESEARCH = "FORM_DOCTORAL_RESEARCH_LOG"
PAGE_ID_DOCTORAL_ETHICS = "FORM_DOCTORAL_ETHICS_FORM"
PAGE_ID_DOCTORAL_THESIS = "FORM_DOCTORAL_THESIS_EDIT"

# PATIENT
PAGE_ID_PATIENT_SYMPTOMS = "FORM_PATIENT_SYMPTOMS"
PAGE_ID_PATIENT_FEEDBACK = "FORM_PATIENT_FEEDBACK"
PAGE_ID_PATIENT_PREFERENCES = "FORM_PATIENT_PREFERENCES"

# GUEST
PAGE_ID_GUEST_CONTACT = "FORM_GUEST_CONTACT"
PAGE_ID_GUEST_INFO = "FORM_GUEST_INFO"
PAGE_ID_GUEST_DEMO = "FORM_GUEST_DEMO_REQUEST"

# NOUVEAU FORMULAIRE : Rapport d'Incident
PAGE_ID_INCIDENT_REPORT = "FORM_INCIDENT_REPORT"

# Identifiants de Page Partagés (utilisés directement dans FORM_MAP)
PAGE_ID_SHARED_USER_MGMT = "UserManagement"
PAGE_ID_SHARED_SYSTEM_LOGS = "SystemLogs"
PAGE_ID_SHARED_PATIENT_HISTORY = "PatientHistory"
PAGE_ID_SHARED_APPOINTMENT = "AppointmentBooking"
PAGE_ID_SHARED_CALENDAR = "Calendar"
PAGE_ID_SHARED_STATS = "Stats"
PAGE_ID_SHARED_MESSAGES = "Messages"
PAGE_ID_SHARED_PROFILE = "Profile"
PAGE_ID_SHARED_SETTINGS = "Settings"
PAGE_ID_SHARED_DEFAULT_DASHBOARD = "DefaultDashboard"
PAGE_ID_SHARED_HOME = "Home"
PAGE_ID_SHARED_NO_ACCESS = "NoAccess"


# ------------------------------------------------------------------------------
# 1. FONCTIONS DE RENDU DU CONTENU PRINCIPAL
# ------------------------------------------------------------------------------


def render_placeholder_page(title: str):
    """Rend un contenu simple pour les pages en cours de développement."""
    st.title(title)
    st.info(f"Page en cours de développement: {title}. Navigation réussie.")


def render_midwife_dashboard_home():
    """Rend le contenu du tableau de bord Sage-femme."""
    st.title("🩺 Tableau de Bord Sage-femme - Accueil")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Patients Actifs", 42, delta="1 nouveau ce mois-ci")
    with col2:
        st.metric("RDV Aujourd'hui", 5, delta="-2 par rapport à hier")
    with col3:
        st.metric("Alertes Postnatales (J+10)", 3)

    st.markdown("## Tâches Rapides")
    st.markdown("...")  # Contenu abrégé
    st.success("Toutes les données sont à jour.")


def render_prenatal_form():
    """Rend le formulaire de Consultation Pré-natale."""
    st.subheader("🧑‍🍼 Formulaire de Consultation Pré-natale")
    st.markdown("---")

    with st.form(key="prenatal_form"):
        col_1, col_2, col_3 = st.columns(3)

        with col_1:
            name = st.text_input("Nom", value="DUPONT")
            prenom = st.text_input("Prénom", value="Sophie")

        with col_2:
            age = st.number_input("Âge", value=32, min_value=0, max_value=120)
            dpa_date = st.date_input(
                "Date Prévue d'Accouchement (DPA)", value=datetime(2026, 3, 15)
            )

        with col_3:
            st.selectbox(
                "Stade de la grossesse (Semaines d'aménorrhée)",
                options=list(range(1, 42)),
            )
            st.text_input("Tension Artérielle (mmHg)", placeholder="Ex: 120/80")

        st.markdown("---")
        st.text_area("Notes et Observations du Jour", height=150)

        submitted = st.form_submit_button(
            "💾 Enregistrer la Consultation", type="primary"
        )

        if submitted:
            data = {
                "type": "prenatal_consultation",
                "name": name,
                "age": age,
                "prenom": prenom,
                "dpa": str(dpa_date),
            }
            try:
                result = add_document("patients", data)
                if result is not None:
                    st.success(f"✅ Consultation pour {name} enregistrée avec succès.")
                else:
                    st.error("❌ Erreur lors de l'enregistrement.")
            except Exception as e:
                st.error(f"❌ Erreur lors de l'enregistrement (simulé) : {e}")


def render_postnatal_form():
    """Rend le formulaire pour le suivi postnatal."""
    st.subheader("👶 Formulaire de Suivi Postnatal")
    st.markdown("---")
    st.date_input("Date du retour à domicile", value="today")
    st.number_input(
        "Poids du bébé (en grammes)", min_value=100, max_value=8000, value=3500
    )
    st.text_area(
        "Observations sur l'allaitement et le bien-être de la mère", height=150
    )

    if st.button("Enregistrer le Suivi", key="btn_postnatal_save"):
        st.success("✅ Données de suivi postnatal enregistrées (simulé).")


def render_patient_management():
    """Rend le contenu pour la gestion des patients (Page PatientManagement)."""
    st.title("📂 Gestion des Dossiers Patients")
    st.markdown("---")
    st.subheader("Recherche de Patient")
    search_term = st.text_input(
        "Entrez le nom ou le numéro de dossier", key="patient_search_term"
    )

    if search_term:
        st.info(f"Recherche en cours pour: **{search_term}**")
        st.dataframe(
            {"ID": ["1001", "1002"], "Nom": ["DUPONT", "MARTIN"]},
            width='stretch',
        )
    else:
        st.warning("Veuillez entrer un terme de recherche.")


def render_incident_report_form():
    """Rend le formulaire pour la déclaration d'événement indésirable."""
    st.subheader("🚨 Déclaration d'Événement Indésirable")
    st.markdown("---")

    with st.form(key="incident_report_form"):
        st.date_input("Date de l'incident", value="today")
        st.selectbox(
            "Gravité de l'incident", options=["Mineur", "Modéré", "Sérieux", "Critique"]
        )
        st.text_area(
            "Description de l'événement",
            height=150,
            placeholder="Détaillez ici ce qui s'est passé...",
        )
        submitted = st.form_submit_button("Soumettre le Rapport", type="primary")
        if submitted:
            st.success("✅ Rapport d'incident soumis (simulé) pour révision.")


def render_admin_dashboard():
    """Rend le contenu pour le tableau de bord Admin."""
    st.title("💻 Tableau de Bord Administrateur")
    st.markdown("---")
    st.warning(
        "Attention : Vous êtes en mode Administration. Modifiez les configurations avec prudence."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Utilisateurs Totaux", 150, delta="+5 ce mois-ci")
    with col2:
        st.metric("Taux d'Erreur (Logs)", "0.5%", delta="-0.1%", delta_color="inverse")

    st.markdown("## Outils d'Administration")
    st.button("Gérer les Rôles Utilisateurs", key="btn_admin_roles")
    st.button("Vérifier l'Intégrité de la Base de Données", key="btn_admin_db")


# ------------------------------------------------------------------------------
# 2. CONFIGURATION GLOBALE & CARTES DE ROUTAGE
# ------------------------------------------------------------------------------

# RÔLES MIS À JOUR
ALL_ROLES = [
    "admin",
    "midwife",
    "doctor",
    "guest",
    "patient",
    "nurse",
    "student",
    "intern",
    "doctoral",
]

PERSISTENCE_KEY = "previous_session_end"

# --- Carte de Routage des Fonctions (ROUTING_MAP) ---
# Tous les IDs de page (chaîne de caractères) pointent vers leur FONCTION de rendu.
ROUTING_MAP: Dict[str, Callable] = {
    # PAGES SAGES-FEMMES (EXISTANTES)
    PAGE_ID_HOME: render_midwife_dashboard_home,
    PAGE_ID_PRENATAL: render_prenatal_form,
    PAGE_ID_POSTNATAL: render_postnatal_form,
    PAGE_ID_PATIENT_MGMT: render_patient_management,
    PAGE_ID_INCIDENT_REPORT: render_incident_report_form,  # NOUVEAU
    # DASHBOARDS DES AUTRES RÔLES
    PAGE_ID_ADMIN_DASH: render_admin_dashboard,
    PAGE_ID_NURSE_DASH: load_form_module(
        "nurse", "dashboard_nurse"
    ),  # Uniformisation pour la modularité
    PAGE_ID_DOCTOR_DASH: load_form_module(
        "doctor", "dashboard_doctor"
    ),  # Uniformisation pour la modularité
    PAGE_ID_STUDENT_DASH: load_form_module(
        "student", "dashboard_student"
    ),  # Uniformisation pour la modularité
    PAGE_ID_INTERN_DASH: load_form_module(
        "intern", "dashboard_intern"
    ),  # Uniformisation pour la modularité
    PAGE_ID_DOCTORAL_DASH: load_form_module(
        "doctoral", "dashboard_doctoral"
    ),  # Uniformisation pour la modularité
    PAGE_ID_PATIENT_HOME: load_form_module(
        "patient", "dashboard_patient"
    ),  # Uniformisation pour la modularité
    # FORMULAIRES SPÉCIFIQUES PAR RÔLE (UNIFORMISÉS AVEC load_form_module)
    PAGE_ID_NURSE_NOTES: load_form_module("nurse", "form_patient_notes"),
    PAGE_ID_NURSE_REPORT: load_form_module("nurse", "form_shift_report"),
    PAGE_ID_NURSE_INVENTORY: load_form_module("nurse", "form_inventory"),
    PAGE_ID_DOCTOR_PRESCRIPTION: load_form_module(
        "doctor", "form_prescription"
    ),  # Correction et Uniformisation
    PAGE_ID_DOCTOR_SURGERY: load_form_module("doctor", "form_surgery_plan"),
    PAGE_ID_DOCTOR_CONSULT: load_form_module("doctor", "form_consultation"),
    PAGE_ID_STUDENT_OBSERVATION: load_form_module("student", "form_observation"),
    PAGE_ID_STUDENT_QUIZ: load_form_module("student", "form_quiz"),
    PAGE_ID_STUDENT_LOGBOOK: load_form_module("student", "form_logbook"),
    PAGE_ID_INTERN_TASK: load_form_module("intern", "form_task_assign"),
    PAGE_ID_INTERN_CHECKLIST: load_form_module("intern", "form_checklist"),
    PAGE_ID_INTERN_CASE_STUDY: load_form_module("intern", "form_case_study"),
    PAGE_ID_DOCTORAL_RESEARCH: load_form_module("doctoral", "form_research_log"),
    PAGE_ID_DOCTORAL_ETHICS: load_form_module("doctoral", "form_ethics"),
    PAGE_ID_DOCTORAL_THESIS: load_form_module("doctoral", "form_thesis_edit"),
    PAGE_ID_PATIENT_SYMPTOMS: load_form_module("patient", "form_symptoms"),
    PAGE_ID_PATIENT_FEEDBACK: load_form_module("patient", "form_feedback"),
    PAGE_ID_PATIENT_PREFERENCES: load_form_module("patient", "form_preferences"),
    PAGE_ID_GUEST_CONTACT: load_form_module("guest", "form_contact"),
    PAGE_ID_GUEST_INFO: load_form_module("guest", "form_info"),
    PAGE_ID_GUEST_DEMO: load_form_module("guest", "form_demo_request"),
    # FORMULAIRES PARTAGÉS PAR ID (Restent des placeholders pour l'instant)
    PAGE_ID_SHARED_USER_MGMT: lambda: render_placeholder_page(
        "👥 Gestion Utilisateurs"
    ),
    PAGE_ID_SHARED_SYSTEM_LOGS: lambda: render_placeholder_page("Logs Système"),
    PAGE_ID_SHARED_PATIENT_HISTORY: lambda: render_placeholder_page(
        "Historique Médical du Patient"
    ),
    PAGE_ID_SHARED_APPOINTMENT: lambda: render_placeholder_page(
        "Réservation de Rendez-vous"
    ),
    PAGE_ID_SHARED_CALENDAR: lambda: render_placeholder_page("📅 Calendrier"),
    PAGE_ID_SHARED_STATS: lambda: render_placeholder_page("📈 Statistiques"),
    PAGE_ID_SHARED_MESSAGES: lambda: render_placeholder_page("📨 Messagerie"),
    PAGE_ID_SHARED_PROFILE: lambda: render_placeholder_page("👤 Mon Profil"),
    PAGE_ID_SHARED_SETTINGS: lambda: render_placeholder_page("🛠️ Paramètres"),
    PAGE_ID_SHARED_DEFAULT_DASHBOARD: lambda: render_placeholder_page(
        "Tableau de Bord Par Défaut"
    ),
    PAGE_ID_SHARED_HOME: lambda: render_placeholder_page(
        "Page d'Accueil Après Connexion"
    ),
    PAGE_ID_SHARED_NO_ACCESS: lambda: st.error(
        "Accès refusé. Aucun contenu défini pour votre rôle."
    ),
}

# --- Carte de Routage Spécifique aux Rôles (FORM_MAP) ---
# Chaque entrée mappe le label UI vers l'ID de page interne (string).
FORM_MAP: Dict[str, Dict[str, str]] = {
    "midwife": {
        "Accueil (Sage-femme)": PAGE_ID_HOME,
        "Gestion des Patients": PAGE_ID_PATIENT_MGMT,
        "Consultation Pré-natale": PAGE_ID_PRENATAL,
        "Suivi Postnatal": PAGE_ID_POSTNATAL,
        "Rapport d'Incident": PAGE_ID_INCIDENT_REPORT,  # Spécifique
    },
    "nurse": {
        "Accueil (Infirmière)": PAGE_ID_NURSE_DASH,
        "Gestion des Patients": PAGE_ID_PATIENT_MGMT,  # Partagé
        "Calendrier des Soins": PAGE_ID_SHARED_CALENDAR,  # Partagé
        "Notes Patient": PAGE_ID_NURSE_NOTES,  # Spécifique
        "Rapport de Quart": PAGE_ID_NURSE_REPORT,  # Spécifique
        "Inventaire": PAGE_ID_NURSE_INVENTORY,  # Spécifique
    },
    "doctor": {
        "Accueil (Médecin)": PAGE_ID_DOCTOR_DASH,
        "Historique Complet": PAGE_ID_SHARED_PATIENT_HISTORY,  # Partagé
        "Statistiques Médicales": PAGE_ID_SHARED_STATS,  # Partagé
        "Prescription": PAGE_ID_DOCTOR_PRESCRIPTION,  # Spécifique
        "Planification Chirurgicale": PAGE_ID_DOCTOR_SURGERY,  # Spécifique
        "Consultation Spécialisée": PAGE_ID_DOCTOR_CONSULT,  # Spécifique
    },
    "student": {
        "Tableau de Bord Étudiant": PAGE_ID_STUDENT_DASH,
        "Accès Documentation": PAGE_ID_SHARED_SETTINGS,  # Partagé
        "Fiche d'Observation": PAGE_ID_STUDENT_OBSERVATION,  # Spécifique
        "Quiz Théorique": PAGE_ID_STUDENT_QUIZ,  # Spécifique
        "Journal de Stage": PAGE_ID_STUDENT_LOGBOOK,  # Spécifique
    },
    "intern": {
        "Tableau de Bord Stagiaire": PAGE_ID_INTERN_DASH,
        "Historique Patient Limité": PAGE_ID_SHARED_PATIENT_HISTORY,  # Partagé
        "Assignation de Tâches": PAGE_ID_INTERN_TASK,  # Spécifique
        "Liste de Contrôle": PAGE_ID_INTERN_CHECKLIST,  # Spécifique
        "Étude de Cas": PAGE_ID_INTERN_CASE_STUDY,  # Spécifique
    },
    "doctoral": {
        "Tableau de Bord Doctorant": PAGE_ID_DOCTORAL_DASH,
        "Accès aux Logs": PAGE_ID_SHARED_SYSTEM_LOGS,  # Partagé
        "Log de Recherche": PAGE_ID_DOCTORAL_RESEARCH,  # Spécifique
        "Formulaire d'Éthique": PAGE_ID_DOCTORAL_ETHICS,  # Spécifique
        "Édition de Thèse": PAGE_ID_DOCTORAL_THESIS,  # Spécifique
    },
    "admin": {
        "Tableau de Bord Admin": PAGE_ID_ADMIN_DASH,  # Spécifique
        "Gestion Utilisateurs": PAGE_ID_SHARED_USER_MGMT,  # Partagé
        "Logs Système": PAGE_ID_SHARED_SYSTEM_LOGS,  # Partagé
    },
    "patient": {
        "Mon Espace Personnel": PAGE_ID_PATIENT_HOME,  # Spécifique
        "Mon Historique Médical": PAGE_ID_SHARED_PATIENT_HISTORY,  # Partagé
        "Prendre RDV": PAGE_ID_SHARED_APPOINTMENT,  # Partagé
        "Déclaration de Symptômes": PAGE_ID_PATIENT_SYMPTOMS,  # Spécifique
        "Questionnaire de Satisfaction": PAGE_ID_PATIENT_FEEDBACK,  # Spécifique
        "Préférences": PAGE_ID_PATIENT_PREFERENCES,  # Spécifique
    },
    "guest": {
        "Tableau de Bord": PAGE_ID_SHARED_DEFAULT_DASHBOARD,  # Partagé
        "Formulaire de Contact": PAGE_ID_GUEST_CONTACT,  # Spécifique
        "Demande d'Information": PAGE_ID_GUEST_INFO,  # Spécifique
        "Demande de Démonstration": PAGE_ID_GUEST_DEMO,  # Spécifique
    },
    "default": {
        "Tableau de Bord": PAGE_ID_SHARED_DEFAULT_DASHBOARD,
    },
}

# ------------------------------------------------------------------------------
# 3. FONCTIONS UTILITAIRES DE SESSION ET D'AUTHENTIFICATION
# ------------------------------------------------------------------------------


def get_greeting() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Bonjour"
    elif 12 <= hour < 17:
        return "Bon après-midi"
    else:
        return "Bonsoir"


def get_user_role():
    return st.session_state.get("user_role", "guest")


def get_current_form_map():
    role = st.session_state.get("user_role")
    return FORM_MAP.get(role, FORM_MAP.get("default", {}))


def get_default_page_key():
    role_map = get_current_form_map()
    # Retourne la première ID de page (ex: DASHBOARD_MIDWIFE)
    if role_map:
        return list(role_map.values())[0]
    return PAGE_ID_SHARED_HOME


def initialize_session():
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False

    if "user_role" not in st.session_state:
        st.session_state.user_role = "guest"

    if "page" not in st.session_state:
        # Fixe la page par défaut selon le rôle initial (guest)
        st.session_state.page = get_default_page_key()

    if "login_time" not in st.session_state:
        st.session_state.login_time = None
    if "last_session_time" not in st.session_state:
        st.session_state.last_session_time = st.session_state.get(
            PERSISTENCE_KEY, "N/A"
        )
    if "logged_out_time" not in st.session_state:
        st.session_state.logged_out_time = "N/A"
    if "show_logout_confirm" not in st.session_state:
        st.session_state.show_logout_confirm = False
    if "user_info" not in st.session_state:
        st.session_state.user_info = {}
    if "username" not in st.session_state:
        st.session_state.username = None


def handle_logout_confirm():
    logout_time = datetime.now()
    st.session_state[PERSISTENCE_KEY] = logout_time.strftime("%d/%m/%Y à %H:%M:%S")

    st.session_state.logged_out_time = logout_time.strftime("%H:%M:%S")
    st.session_state.is_logged_in = False
    st.session_state.page = "LoggedOut"
    st.session_state.show_logout_confirm = False

    keys_to_delete = ["user_role", "user_info", "username", "page"]
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]

    st.toast("👋 Déconnexion réussie.", icon="✅")
    time.sleep(1)
    st.rerun()


def handle_logout_cancel():
    st.session_state.show_logout_confirm = False
    st.toast("✅ Session maintenue.", icon="🔒")


def apply_global_styles():
    st.markdown(
        """
        <style>
        /* CSS global pour l'apparence */
        div.stButton > button {
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.2s ease;
            color: #333;
            border: 1px solid #ddd;
        }
        div.stButton > button {
            border-radius: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            height: auto;
        }
        
        /* Styles spécifiques pour les boutons de déconnexion */
        button[key="btn_logout_styled"] {
            background-color: #e74c3c !important;
            color: white !important;
            border: none !important;
        }
        
        /* Layout */
        .main .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_top_strip(app_title: str):
    # Barre de titre en haut de la page
    strip_container = st.container()
    with strip_container:
        user_role = st.session_state.get("user_role", "guest")

        st.markdown(
            f"""
            <style>
            .top-strip {{
                padding: 10px 0px;
                background-color: #f0f2f6;
                border-bottom: 1px solid #e6e6e6;
                margin-bottom: 20px;
                width: 100%;
            }}
            .title-text {{
                font-size: 1.5em;
                font-weight: 600;
                color: #0c4c5e;
            }}
            </style>
            <div class="top-strip">
                <span class="title-text">{app_title}</span>
                <span style="float:right; font-size:0.9em; color:#555;">
                    {st.session_state.get('username', 'Visiteur')} | {user_role.capitalize()}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_role_switcher():
    # Outil de débogage pour changer de rôle
    st.sidebar.markdown("## ⚙️ Outil de Test de Rôle (DEBUG)")
    current_state = st.session_state.get("user_role", "guest")
    options = ["guest"] + ALL_ROLES

    try:
        default_index = options.index(current_state)
    except ValueError:
        default_index = 0

    selected_role = st.sidebar.selectbox(
        "Simuler le rôle de l'utilisateur:",
        options=options,
        index=default_index,
        key="role_switcher_select",
    )

    if st.sidebar.button("Appliquer le Rôle", width='stretch'):
        if selected_role == "guest":
            if st.session_state.get("is_logged_in"):
                handle_logout_confirm()
        else:
            if st.session_state.get("user_role") != selected_role:
                st.session_state["is_logged_in"] = True
                st.session_state["user_role"] = selected_role
                st.session_state["username"] = f"Test-{selected_role.capitalize()}"
                st.session_state["page"] = get_default_page_key()
                st.toast(f"Rôle simulé : **{selected_role.capitalize()}**.", icon="✅")

        time.sleep(0.1)
        st.rerun()


# Actions Rapides Partagées
SHARED_ACTIONS: Dict[str, Dict[str, Any]] = {
    "📅 Calendrier": {"icon": "🗓️", "id": PAGE_ID_SHARED_CALENDAR},
    "📈 Statistiques": {"icon": "📊", "id": PAGE_ID_SHARED_STATS},
    "📨 Messagerie": {"icon": "📧", "id": PAGE_ID_SHARED_MESSAGES},
    "👤 Mon Profil": {"icon": "👤", "id": PAGE_ID_SHARED_PROFILE},
    "🛠️ Paramètres": {"icon": "⚙️", "id": PAGE_ID_SHARED_SETTINGS},
    "🚪 Déconnexion": {"icon": "🚪", "id": "Logout"},
}


def render_sidebar_content():
    current_role = get_user_role()
    current_role_map = get_current_form_map()

    st.sidebar.title(f"{get_greeting()}!")
    st.sidebar.markdown(f"**Rôle Actuel :** `{current_role.capitalize()}`")

    # --- A. FORMULAIRES SPÉCIFIQUES (Navigation Principale - Selectbox) ---
    st.sidebar.subheader("Navigation (Modules Spécifiques)")

    # Déterminer la clé active (l'ID string)
    current_page_id = st.session_state.get("page", get_default_page_key())

    # Trouver le label correspondant à la page active pour le selectbox
    active_label = next(
        (
            label
            for label, page_id in current_role_map.items()
            if page_id == current_page_id
        ),
        list(current_role_map.keys())[0] if current_role_map else "Accueil",
    )

    if current_role_map:
        selected_label = st.sidebar.selectbox(
            "Sélectionnez un module :",
            options=list(current_role_map.keys()),
            index=list(current_role_map.keys()).index(active_label),
            key="main_navigation_select",
        )

        new_page_id = current_role_map.get(selected_label)

        if st.session_state.page != new_page_id:
            st.session_state.page = new_page_id
            st.toast(f"Navigation vers {selected_label}...", icon="🚀")
            st.rerun()
    else:
        st.sidebar.info("Aucun module principal disponible pour ce rôle.")

    # --- B. FORMULAIRES PARTAGÉS (Actions Rapides) ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Actions Rapides (Partagées)")

    for label, config in SHARED_ACTIONS.items():
        if label == "🚪 Déconnexion":
            continue

        # Utilisation du texte seul pour l'affichage du bouton
        text_label_only = label.split(" ", 1)[1] if " " in label else label

        if st.sidebar.button(
            f"{config['icon']} {text_label_only}",
            key=f"btn_{config['id']}",
            width='stretch',
        ):
            st.session_state.page = config["id"]
            st.rerun()

    # --- C. Informations de Session et Déconnexion ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Session")

    if st.session_state.login_time:
        login_time_str = st.session_state.login_time.strftime("%H:%M:%S")
        st.sidebar.markdown(f"**Connexion :** `{login_time_str}`")
    else:
        st.sidebar.markdown(f"**Connexion :** `N/A`")

    last_session_str = st.session_state.last_session_time
    st.sidebar.markdown(f"**Dernière session :** `{last_session_str}`")

    # Logique de confirmation de déconnexion
    if st.session_state.show_logout_confirm:
        st.sidebar.error("⚠️ Voulez-vous vous déconnecter?")
        col_yes, col_no = st.sidebar.columns(2)
        with col_yes:
            if st.button(
                "Oui, déconnecter",
                key="btn_logout_yes",
                width='stretch',
                type="primary",
            ):
                handle_logout_confirm()
        with col_no:
            if st.button(
                "Non, continuer", key="btn_logout_no", width='stretch'
            ):
                handle_logout_cancel()
    else:
        # Bouton Déconnexion stylisé
        logout_config = SHARED_ACTIONS["🚪 Déconnexion"]
        logout_label_only = list(SHARED_ACTIONS.keys())[-1].split(" ", 1)[1]

        if st.sidebar.button(
            f"{logout_config['icon']} {logout_label_only}",  # Utilisation de l'icône + label sans l'icône
            key="btn_logout_styled",
            width='stretch',
        ):
            st.session_state.show_logout_confirm = True
            st.rerun()

    st.sidebar.markdown(
        """
        <div style="text-align: center; color: #AAAAAA; font-size: 0.8em; margin-top: 50px;">
            MSA | Midwifery Services Application — Engagée pour des soins de qualité.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_app_content():
    """Affiche le contenu de l'application après la connexion, en fonction de l'ID de page."""

    role = st.session_state.get("user_role", "guest")
    user_name = st.session_state.get("username", "Utilisateur")

    st.header(f"{get_greeting()}, {user_name}!")
    st.subheader(f"Accès : **{role.capitalize()}**")
    st.markdown("---")

    current_page_id = st.session_state.get("page", get_default_page_key())

    # Tenter de trouver la fonction de rendu dans la carte de routage unifiée
    render_func = ROUTING_MAP.get(current_page_id)

    if render_func and callable(render_func):
        render_func()  # Exécute la fonction de rendu (dashboard, formulaire, ou placeholder)
    else:
        # Fallback si l'ID est dans l'état mais n'est pas mappé
        render_placeholder_page(f"Module inconnu (ID: {current_page_id})")
        st.error(
            "Erreur de routage : Impossible de trouver la fonction de rendu pour cet ID de page."
        )


def render_logged_out_page():
    # Page affichée après la déconnexion
    st.title("👋 Session Terminée")
    st.info(f"Vous avez été déconnecté à {st.session_state.logged_out_time}.")
    st.markdown(
        f"Votre dernière session s'est terminée le **{st.session_state.last_session_time}**."
    )

    if st.button("Reconnecter", key="btn_reconnect", type="primary"):
        st.session_state.clear()
        initialize_session()
        st.rerun()


def main():
    st.set_page_config(layout="wide", page_title="MSA - Midwifery Services Application")
    apply_global_styles()
    initialize_session()
    render_top_strip("MSA - Midwifery Services Application")
    render_role_switcher()

    if st.session_state.is_logged_in:
        # La barre latérale et le contenu principal sont rendus si l'utilisateur est connecté
        render_sidebar_content()
        render_app_content()

    elif st.session_state.page == "LoggedOut":
        render_logged_out_page()
    else:
        # Page de connexion par défaut
        st.title("Bienvenue dans MSA !")
        st.markdown(
            "Veuillez vous connecter pour accéder aux tableaux de bord et aux formulaires."
        )
        st.markdown("---")
        st.subheader("Authentification (Simulée)")
        username_input = st.text_input(
            "Nom d'utilisateur (ex: midwife)", key="auth_username"
        )
        password_input = st.text_input("Mot de passe", type="password")

        if st.button("Se connecter", type="primary"):
            if username_input and password_input:
                role = username_input.lower()
                if role in ALL_ROLES:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = role
                    st.session_state.username = role.capitalize()
                    st.session_state.login_time = datetime.now()
                    st.session_state.page = get_default_page_key()
                    st.toast("Connexion réussie!", icon="🎉")
                    time.sleep(0.1)
                    st.rerun()
                else:
                    st.error("Rôle ou identifiant inconnu. Veuillez réessayer.")


if __name__ == "__main__":
    main()
