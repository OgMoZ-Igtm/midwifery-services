import streamlit as st
import importlib.util
from typing import Dict
from modules.backend.supabase_client import supabase

# --- Variables de Configuration ---
ALLOWED_ROLES = [
    "admin",
    "doctor",
    "midwife",
    "nurse",
    "intern",
    "doctoral",
    "student",
    "guest",
    "patient",
]

# --- Dictionnaire de Mappage des Formulaires (Traduit et avec Icônes) ---
# La clé du dictionnaire est le LABEL affiché dans la selectbox.
# La valeur est le CHEMIN du module Python à charger (simulé ici par des
# st.write)
FORM_MAP: Dict[str, Dict[str, str]] = {
    "admin": {
        "📊 Tableau de bord Administrateur": "modules.forms.forms_admin.form_admin_dashboard",
        "🔍 Tableau de bord d'Audit": "modules.forms.forms_admin.form_admin_audit_dashboard",
        "👥 Gestion des Utilisateurs": "modules.forms.forms_admin.form_user_management",
        "🌐 Gestion Utilisateurs (Supabase)": "modules.forms.forms_admin.form_user_management_supabase",
        "🧑‍💻 Gestion des Rôles": "modules.forms.forms_admin.form_admin_roles",
        "🤝 Gestion des Groupes": "modules.forms.forms_admin.form_group_management",
        "⚙️ Gestionnaire de Modules": "modules.forms.forms_admin.form_admin_module_manager",
        "🧩 Tableau de bord des Modules": "modules.forms.forms_admin.form_admin_dashboard_modules",
        "🛠️ Configuration Système": "modules.forms.forms_admin.form_config_system",
        "🔑 Hachage & Sécurité": "modules.forms.forms_admin.form_admin_hashing",
        "🔒 Outil de Hachage": "modules.forms.forms_admin.form_hashing",
        "📜 Journaux d'activité (Logs)": "modules.forms.forms_admin.form_admin_logs",
        "🗑️ Suppression des Logs": "modules.forms.forms_admin.form_log_deleter",
        "💾 Gestion des Données": "modules.forms.forms_admin.form_admin_data",
        "📈 Tableau de bord de Rapports": "modules.forms.forms_admin.form_report_dashboard",
        "✅ Tableau de bord du Validateur": "modules.forms.forms_admin.form_validator_dashboard",
        "📄 Exporter en PDF": "modules.forms.forms_admin.form_export_pdf",
        "📦 Organisation des Packs": "modules.forms.forms_admin.form_pack_organisation",
        "⬆️ Mise à Jour Système": "modules.forms.forms_admin.form_update",
        "✏️ Éditeur Administrateur": "modules.forms.forms_admin.form_editor_admin",
        "📝 Voir les Notes": "modules.forms.forms_admin.form_view_notes",
    },
    "doctor": {
        "👨‍⚕️ Tableau de bord Docteur": "modules.forms.forms_doctor.form_doctor_dashboard",
        "🧠 Diagnostic Médical": "modules.forms.forms_doctor.form_diagnostic",
        "💊 Ordonnance/Prescription": "modules.forms.forms_doctor.form_prescription",
        "📁 Historique Patient": "modules.forms.forms_doctor.form_patient_history",
        "📞 Demandes de Consultation": "modules.forms.forms_doctor.form_consultation_requests",
        "🗒️ Notes Médicales": "modules.forms.forms_doctor.form_medical_notes",
        "📦 Gestion des Stocks": "modules.forms.forms_doctor.form_supply",
        "💬 Messages Docteur": "modules.forms.forms_doctor.form_messages",
        "👤 Mon Profil Docteur": "modules.forms.forms_doctor.form_profile",
        "📄 Page Générique": "modules.forms.forms_doctor.form_page",
    },
    "midwife": {
        "🤱 Tableau de bord Sage-Femme": "modules.forms.forms_midwife.form_midwife_dashboard",
        "💖 Soins Prénataux": "modules.forms.forms_midwife.form_prenatal_care",
        "⏱️ Soins Intrapartum": "modules.forms.forms_midwife.form_intrapartum_care",
        "🧸 Soins Postnatals": "modules.forms.forms_midwife.form_postnatal_care",
        "🏃 Suivi Post-Partum": "modules.forms.forms_midwife.form_follow_up",
        "🤰 Accouchement": "modules.forms.forms_midwife.form_childbirth",
        "🗂️ Registre des Accouchements": "modules.forms.forms_midwife.form_delivery_log",
        "📝 Plan de Naissance": "modules.forms.forms_midwife.form_birth_plan",
        "📈 Suivi de Grossesse": "modules.forms.forms_midwife.form_pregnancy_tracking",
        "👩‍⚕️ Consultation S-F": "modules.forms.forms_midwife.form_consultation_midwife",
        "🔄 Soins Complets de S-F": "modules.forms.forms_midwife.form_throughout_midwifery_care",
        "🍎 Suivi Nutritionnel": "modules.forms.forms_midwife.form_nutrition",
        "💡 Éducation & Prévention": "modules.forms.forms_midwife.form_education_prevention",
        "🧘 Bien-être Émotionnel": "modules.forms.forms_midwife.form_emotional_well_being",
        "🛠️ Ateliers & Formations": "modules.forms.forms_midwife.form_workshops",
        "📋 Données Patient": "modules.forms.forms_midwife.form_patient_data",
        "🌍 Données Démographiques": "modules.forms.forms_midwife.form_demographics",
        "🚨 Alertes Patients": "modules.forms.forms_midwife.form_patients_alerts",
        "🗓️ Agenda Médical": "modules.forms.forms_midwife.form_medical_agenda",
        "📞 Informations de Contact": "modules.forms.forms_midwife.form_contact_info",
        "💬 Messages Sage-Femme": "modules.forms.forms_midwife.form_messages",
        "👤 Mon Profil Sage-Femme": "modules.forms.forms_midwife.form_profile",
    },
    "nurse": {
        "👩‍⚕️ Tableau de bord Infirmier(ère)": "modules.forms.forms_nurse.form_nurse_dashboard",
        "🩸 Signes Vitaux": "modules.forms.forms_nurse.form_vital_signs",
        "❤️ Surveillance Patient": "modules.forms.forms_nurse.form_patient_monitoring",
        "💉 Gestion des Médicaments": "modules.forms.forms_nurse.form_medication_management",
        "📋 Notes Infirmières": "modules.forms.forms_nurse.form_nursing_notes",
        "🛍️ Demande de Fournitures": "modules.forms.forms_nurse.form_supply_request",
        "📅 Horaire / Planning": "modules.forms.forms_nurse.form_schedule_nurse",
        "💬 Messages Infirmier(ère)": "modules.forms.forms_nurse.form_messages",
        "👤 Mon Profil Infirmier(ère)": "modules.forms.forms_nurse.form_profile",
    },
    "intern": {
        "🧑‍🎓 Tableau de bord Stagiaire": "modules.forms.forms_intern.form_intern_dashboard",
        "✅ Tâches Quotidiennes": "modules.forms.forms_intern.form_daily_tasks",
        "📚 Journal de Bord": "modules.forms.forms_intern.form_intern_logbook",
        "🔗 Ressources": "modules.forms.forms_intern.form_resources",
        "📢 Commentaires & Retour": "modules.forms.forms_intern.form_feedback",
        "💬 Messages Stagiaire": "modules.forms.forms_intern.form_messages",
        "👤 Mon Profil Stagiaire": "modules.forms.forms_intern.form_profile",
    },
    "doctoral": {
        "🎓 Tableau de bord Doctorant": "modules.forms.forms_doctoral.form_doctoral_dashboard",
        "🔬 Projet de Recherche": "modules.forms.forms_doctoral.form_research_project",
        "📑 Suivi de Thèse": "modules.forms.forms_doctoral.form_thesis_tracking",
        "📰 Publications": "modules.forms.forms_doctoral.form_publications",
        "🧑‍🏫 Supervision & Encadrement": "modules.forms.forms_doctoral.form_supervision",
        "💬 Messages Doctorant": "modules.forms.forms_doctoral.form_messages",
        "👤 Mon Profil Doctorant": "modules.forms.forms_doctoral.form_profile",
    },
    "student": {
        "🧑‍💻 Tableau de bord Étudiant": "modules.forms.forms_student.form_student_dashboard",
        "📈 Suivi Académique": "modules.forms.forms_student.form_academic_tracking",
        "📖 Cours & Matières": "modules.forms.forms_student.form_courses",
        "⭐ Évaluations": "modules.forms.forms_student.form_evaluations",
        "📧 Demande de Stage": "modules.forms.forms_student.form_internship_request",
        "💬 Messages Étudiant": "modules.forms.forms_student.form_messages",
        "👤 Mon Profil Étudiant": "modules.forms.forms_student.form_profile",
    },
    "patient": {
        "🧑 Tableau de bord Patient": "modules.forms.forms_patient.form_patient_dashboard",
        "🗓️ Prendre Rendez-vous": "modules.forms.forms_patient.form_book_appointment",
        "✍️ Auto-Déclaration": "modules.forms.forms_patient.form_self_report",
        "📂 Voir Dossier Médical": "modules.forms.forms_patient.form_view_records",
        "🕰️ Historique des Visites": "modules.forms.forms_patient.form_visit_history",
        "👨‍⚕️ Contacter un Docteur": "modules.forms.forms_patient.form_contact_doctor",
        "📄 Exporter Dossier PDF": "modules.forms.forms_patient.form_export_pdf",
        "💬 Messages Patient": "modules.forms.forms_patient.form_messages",
        "👤 Mon Profil Patient": "modules.forms.forms_patient.form_profile",
    },
    "guest": {
        "🚪 Tableau de bord Invité": "modules.forms.forms_guest.form_guest_dashboard",
        "❓ Qui Sommes-Nous ?": "modules.forms.forms_guest.form_qui_sommes_nous",
    },
}

# --- Formulaires partagés (cliquables via boutons) ---
SHARED_FORMS: Dict[str, str] = {
    # AJOUTÉ : Le formulaire d'accueil par défaut demandé
    "🏠 Accueil": "modules.forms.shared.form_home",
    "📅 Calendrier": "modules.forms.shared.form_calendar",
    "🛠️ Paramètres": "modules.forms.shared.form_settings",
    "📈 Statistiques": "modules.forms.shared.form_stats",
    "📨 Messagerie Générique": "modules.forms.shared.form_messages",
    "👤 Mon Profil Générique": "modules.forms.shared.form_profile",
    "🚪 Déconnexion": "modules.auth.logout",
}

# --- Constante pour la clé du formulaire d'accueil ---
ACCUEIL_KEY = "🏠 home"
ACCUEIL_PATH = SHARED_FORMS[ACCUEIL_KEY]


# --- Fonctions Utilitaires ---


def load_form(form_key: str, module_path: str):
    """
    Simule le chargement du contenu du formulaire.
    """
    # Scenario 2: Gestion de la Déconnexion (Réinitialise pour le prochain
    # login)
    if module_path == "modules.auth.logout":
        # Logique de déconnexion gérée directement dans le routeur pour la
        # simplicité
        if "role" in st.session_state:
            del st.session_state.role
        if "username" in st.session_state:
            del st.session_state.username

        # S'assurer que le prochain login chargera l'Accueil (Scenario 1)
        st.session_state.current_form_key = ACCUEIL_KEY

        st.session_state.page = "login"
        st.success("🚪 Vous êtes déconnecté(e). Redirection...")
        st.rerun()

    st.markdown(f"## {form_key}")
    st.markdown("---")
    st.info(f"Rendu du contenu du module: **{module_path}**")

    # Afficher le chemin pour la démo
    st.code(
        f"def run():\n    st.title('{form_key}')\n    st.write('Contenu spécifique au rôle: {
            st.session_state.get(
                'role',
                'none')}')",
        language="python",
    )


def get_default_form_key(role: str) -> str:
    """Détermine la clé (label) du dashboard par défaut pour un rôle."""
    role_forms = FORM_MAP.get(role, {})

    default_map = {
        "admin": "📊 Tableau de bord Administrateur",
        "doctor": "👨‍⚕️ Tableau de bord Docteur",
        "midwife": "🤱 Tableau de bord Sage-Femme",
        "nurse": "👩‍⚕️ Tableau de bord Infirmier(ère)",
        "intern": "🧑‍🎓 Tableau de bord Stagiaire",
        "doctoral": "🎓 Tableau de bord Doctorant",
        "student": "🧑‍💻 Tableau de bord Étudiant",
        "patient": "🧑 Tableau de bord Patient",
        "guest": "🚪 Tableau de bord Invité",
    }

    key = default_map.get(role)
    if key and key in role_forms:
        return key

    # Si aucun tableau de bord spécifique n'est trouvé, ou s'il n'y a pas de formulaires,
    # on retourne l'Accueil s'il est disponible.
    return (
        ACCUEIL_KEY
        if ACCUEIL_KEY in SHARED_FORMS
        else (list(role_forms.keys())[0] if role_forms else None)
    )


# --- Fonction principale de Routage et Rendu ---
def route_dashboard():
    # 🔐 Rôle actif (s'assure que le rôle existe, sinon utilise 'guest')
    role = st.session_state.get("role", "guest").lower()

    # --- 1. Gestion de l'état non autorisé et non authentifié (Scénario 3) ---
    if role not in ALLOWED_ROLES:
        # Charger la vue d'accueil (accueil_view.py) pour le cas non autorisé
        load_form(ACCUEIL_KEY, ACCUEIL_PATH)

        st.session_state.page = "login"
        st.error(
            "⛔ Rôle non autorisé ou session expirée. Redirection vers la page de connexion."
        )
        return  # Empêche le reste du routeur de s'exécuter

    # --- 2. Initialisation de la sélection du formulaire (Scénario 1: Connexion) ---

    # Si 'current_form_key' n'est pas défini, le premier formulaire chargé après
    # une connexion réussie est l'Accueil.
    if "current_form_key" not in st.session_state:
        st.session_state.current_form_key = ACCUEIL_KEY

    # Si la clé de formulaire sélectionnée n'est pas valide pour le rôle actuel
    # et n'est pas un formulaire partagé, on revient à l'Accueil.
    if (
        st.session_state.current_form_key not in FORM_MAP.get(role, {})
        and st.session_state.current_form_key not in SHARED_FORMS
    ):
        st.session_state.current_form_key = ACCUEIL_KEY

    # --- Préparation de la Barre Latérale ---
    st.sidebar.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-color: #f0f4f8;
            padding: 20px;
        }}
        .sidebar-title {{
            font-size: 24px;
            font-weight: 700;
            color: #1a56db;
            margin-bottom: 20px;
            padding-bottom: 5px;
            border-bottom: 2px solid #ccc;
        }}
        .sidebar-section {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-top: 15px;
            margin-bottom: 8px;
        }}
        /* Style pour les boutons partagés */
        div.stButton > button {{
            width: 100%;
            margin-top: 5px;
            background-color: #ffffff;
            border-radius: 8px;
            border: 1px solid #c4c9d1;
            transition: all 0.2s;
            text-align: left;
            padding: 8px 12px;
        }}
        div.stButton > button:hover {{
            background-color: #e6e9f0;
            border-color: #1a56db;
        }}
        </style>
        <div class='sidebar-title'>App Santé - Rôle: {role.capitalize()}</div>
    """,
        unsafe_allow_html=True,
    )

    # 3. 🎛️ Barre latérale : formulaires spécifiques (Selectbox)
    role_forms = FORM_MAP.get(role, {})

    st.sidebar.markdown(
        "<div class='sidebar-section'>📂 Tâches Spécifiques</div>",
        unsafe_allow_html=True,
    )
    if role_forms:
        try:
            current_key_for_selectbox = st.session_state.current_form_key
            if current_key_for_selectbox in role_forms:
                default_index = list(role_forms.keys()).index(current_key_for_selectbox)
            else:
                # Si le formulaire actif est l'Accueil ou un autre partagé,
                # la selectbox par défaut est le premier item spécifique du
                # rôle.
                default_index = 0

        except ValueError:
            default_index = 0

        selected_key = st.sidebar.selectbox(
            "Sélectionner un formulaire",
            list(role_forms.keys()),
            key="sidebar_selectbox",
            index=default_index,
            label_visibility="collapsed",
            on_change=lambda: st.session_state.__setitem__(
                "current_form_key", st.session_state.sidebar_selectbox
            ),
        )

        # Mise à jour de la clé si la selectbox a été utilisée
        if (
            selected_key != st.session_state.current_form_key
            and selected_key in role_forms
        ):
            st.session_state.current_form_key = selected_key

    # 4. 🎛️ Barre latérale : formulaires partagés (Boutons)
    st.sidebar.markdown(
        "<div class='sidebar-section'>🤝 Fonctions Transverses</div>",
        unsafe_allow_html=True,
    )

    # Créer les boutons
    for label, module_path in SHARED_FORMS.items():
        if st.sidebar.button(label, key=f"btn_{label}"):
            st.session_state.current_form_key = label
            st.rerun()

    # 5. 🚀 Chargement dynamique du module sélectionné
    current_key = st.session_state.current_form_key

    if current_key in role_forms:
        module_path = role_forms[current_key]
        load_form(current_key, module_path)
    elif current_key in SHARED_FORMS:
        module_path = SHARED_FORMS[current_key]
        load_form(current_key, module_path)
    else:
        # En cas d'erreur de routage non prévue, charge l'Accueil par sécurité
        st.error("Erreur de routage. Chargement de la page d'Accueil par défaut.")
        st.session_state.current_form_key = ACCUEIL_KEY
        st.rerun()
