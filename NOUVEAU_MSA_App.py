import streamlit as st
import importlib
import requests
import pandas as pd
import pydeck as pdk
from dotenv import load_dotenv
import os

# Assurez-vous que utils.py et constants.py sont dans le même dossier ou accessible
# (Note: public_utils est supposé exister, sinon l'import échouera)
from modules.public.public_utils import (
    render_home_page,
    show_public_header,
    render_info_section,
    play_audio,
    load_static_asset,
)

# =========================================================
# ⚙️ CONSTANTES GLOBALES ET MOCKS
# =========================================================

# Charger les variables d'environnement (si utilisées)
load_dotenv()

# --- Simulation des mots de passe (à remplacer par une source sécurisée en production) ---
USER_PASSWORDS = {
    "MIDWIFE": "msa2024",
    "NURSE": "nurse2024",
    "DOCTOR": "doc2024",
    "PATIENT": "pat2024",
    "STUDENT": "stud2024",
    "INTERN": "intern2024",
    "DOCTORAL": "phd2024",
    "ADMIN": "admin2024",
    "GUEST": "guest2024",
}

# --- Constantes: Liste des formulaires spécifiques par rôle (Les clés sont des identifiants)
SPECIFIC_FORMS = {
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
    "ADMIN": [
        "forms_admin/form_user_management",
        "forms_admin/form_system_logs_viewer",
        "forms_admin/form_report_dashboard",
        "forms_admin/form_global_settings",
        "forms_admin/form_config_system",
    ],
}

# --- Constantes: Fonctions partagées (Nom convivial -> Chemin)
SHARED_FORMS = {
    "Agenda": "forms_shared/form_agenda",
    "Calendrier": "forms_shared/form_calendar",
    "Messages": "forms_shared/form_messages",
    "Chat": "forms_shared/form_chat",
    "Profil": "forms_shared/form_profile",
    "Settings": "forms_shared/form_settings",
    "Signup": "forms_shared/form_signup",
}

# --- Constantes: Étiquettes (Labels) conviviales pour les formulaires (Chemin -> Label affiché)
FORM_LABELS = {
    # MIDWIFE
    "forms_midwife/form_birth_plan": "🍼 Plan de naissance",
    "forms_midwife/form_postpartum": "🌸 Suivi post-partum",
    "forms_midwife/form_initial_routine": "🧾 Routine initiale",
    "forms_midwife/form_patient_file": "📁 Dossier patiente",
    "forms_midwife/form_patient_management": "🧭 Gestion de la patiente",
    "forms_midwife/form_midwife_messages": "✉️ Messages de la sage-femme",
    "forms_midwife/form_consultation_prenatale": "🤰 Consultation prénatale",
    "forms_midwife/form_emotional_well_being": "💖 Bien-être émotionnel",
    "forms_midwife/form_incident_report": "⚠️ Rapport d'incident",
    "forms_midwife/form_demographics": "📊 Données démographiques",
    "forms_midwife/form_prenatal_care": "🌿 Soins prénataux",
    "forms_midwife/form_postnatal_care": "🌼 Soins postnataux",
    "forms_midwife/form_intrapartum_care": "⏳ Soins intrapartum",
    # NURSE
    "forms_nurse/form_schedule_nurse": "📆 Horaire infirmier",
    "forms_nurse/form_consultation_notes": "📝 Notes de consultation",
    "forms_nurse/form_nurse_shift_report": "🌙 Rapport de quart",
    "forms_nurse/form_nursing_notes": "📒 Notes infirmières",
    "forms_nurse/form_nurse_inventory_management": "📦 Gestion des stocks",
    "forms_nurse/form_nurse_medicament_admin": "💊 Administration des médicaments",
    "forms_nurse/form_vital_signs": "❤️ Signes vitaux",
    "forms_nurse/form_followup": "🔄 Suivi infirmier",
    # DOCTOR
    "forms_doctor/form_doctor_emergency_assessment": "🚨 Évaluation d'urgence",
    "forms_doctor/form_medicament_prescription": "💊 Prescription",
    "forms_doctor/form_due_date_calculator": "📅 Calcul de la date prévue",
    "forms_doctor/form_doctor_schedule": "🩺 Horaire du médecin",
    "forms_doctor/form_medical_report": "📄 Rapport médical",
    "forms_doctor/form_prescription": "🖊️ Ordonnance",
    # PATIENT
    "forms_patient/form_patient_satisfaction_survey": "🗣️ Sondage de satisfaction",
    "forms_patient/form_patient_symptom": "🤒 Symptômes",
    "forms_patient/form_patient_appointment_booking": "📅 Prise de rendez-vous",
    "forms_patient/form_patient_communicatient_prefs": "📞 Préférences de communication",
    "forms_patient/form_patient_feedback": "💬 Retour d'expérience",
    "forms_patient/form_patient_prescription_request": "📝 Demande d'ordonnance",
    "forms_patient/form_feedback": "🗨️ Commentaires",
    "forms_patient/form_request": "📨 Demande générale",
    # STUDENT
    "forms_student/form_observation": "👀 Observation clinique",
    "forms_student/form_reflection": "🧠 Réflexion personnelle",
    # GUEST
    "forms_guest/form_utility_general_contact": "📬 Contact général",
    "forms_guest/form_utility_service_request": "🛠️ Demande de service",
    # INTERN
    "forms_intern/form_clinical_observation": "🔍 Observation clinique",
    "forms_intern/form_inter_case_study": "📚 Étude de cas",
    "forms_intern/form_intern_logbook": "📓 Journal de stage",
    "forms_intern/form_intern_skill_checklist": "✅ Liste de compétences",
    "forms_intern/form_training_log": "🗂️ Journal de formation",
    # DOCTORAL
    "forms_doctoral/form_research_note": "🧪 Note de recherche",
    "forms_doctoral/form_doctorant_ethics_submissions": "📑 Soumissions éthiques",
    # ADMIN
    "forms_admin/form_user_management": "👥 Gestion des utilisateurs",
    "forms_admin/form_system_logs_viewer": "🧾 Journaux système",
    "forms_admin/form_report_dashboard": "📊 Tableau de bord",
    "forms_admin/form_global_settings": "⚙️ Paramètres globaux",
    "forms_admin/form_config_system": "🛠️ Configuration système",
    # SHARED (Étiquettes complètes avec emoji pour l'affichage)
    "forms_shared/form_agenda": "📅 Agenda",
    "forms_shared/form_calendar": "🗓️ Calendrier",
    "forms_shared/form_messages": "✉️ Messages",
    "forms_shared/form_chat": "💬 Chat",
    "forms_shared/form_profile": "👤 Profil",
    "forms_shared/form_settings": "⚙️ Paramètres",
    "forms_shared/form_signup": "📝 Inscription",
}

# Mapping convivial pour l'affichage des boutons partagés (utilise l'emoji)
SHARED_DISPLAY_LABELS = {
    "Agenda": "📅 Agenda",
    "Calendrier": "🗓️ Calendrier",
    "Messages": "✉️ Messages",
    "Chat": "💬 Chat",
    "Profil": "👤 Profil",
    "Settings": "⚙️ Paramètres",
    "Signup": "📝 Inscription",
}


# =========================================================
# ⚙️ CONFIGURATION ET INITIALISATION
# =========================================================

# Configuration de la page Streamlit
st.set_page_config(
    page_title="MSA - Services de sage-femme en milieu autochtone",
    layout="centered",
)

# Initialisation de l'état si ce n'est pas déjà fait
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None
    st.session_state["info_page"] = "Accueil"
    st.session_state["audio_running"] = False
    st.session_state["audio_level"] = "🔊"
    if "carrousel_paused" not in st.session_state:
        st.session_state["carrousel_paused"] = False
# Ajout de la variable d'état pour la navigation
if "main_section_auth" not in st.session_state:
    st.session_state["main_section_auth"] = "Accueil"


# =========================================================
# 🔐 GESTION DE LA CONNEXION (Flux Principal)
# =========================================================

# Afficher l'en-tête public (supposé contenir des onglets de navigation publique)
show_public_header()

# Simuler le rendu des pages publiques (Mission, Équipe, etc.)
if st.session_state.get("onglet_selectionné") == "Accueil":
    render_info_section("🌸 Bienvenue dans votre espace privé.")
elif st.session_state.get("onglet_selectionné") == "Équipe":
    render_info_section("👩‍⚕️ Découvrez les membres de l’équipe et leurs rôles sacrés.")


if not st.session_state["logged_in"]:
    # LOGIQUE AVANT CONNEXION
    current_page = st.session_state.get("info_page", "Accueil")

    if current_page == "Accueil":
        # 1. Page d'accueil (carrousel, météo, carte)
        render_home_page()

        st.markdown("---")
        st.subheader("🧡 Connexion à la plateforme")

        # 2. Formulaire de connexion
        message_placeholder = st.empty()

        with st.form("msa_login_form", clear_on_submit=True):
            username = st.text_input(
                "Identifiant (rôle)",
                placeholder="Ex: MIDWIFE, DOCTOR, PATIENT...",
            )
            password = st.text_input("Mot de passe", type="password")
            submitted = st.form_submit_button("Se connecter")

        if submitted:
            role = username.upper()

            # Vérification de la connexion
            if role in USER_PASSWORDS and password == USER_PASSWORDS[role]:
                message_placeholder.success(
                    f"✅ Connexion réussie en tant que **{role}**. Redirection..."
                )

                # Mise à jour des variables de session
                st.session_state["user_role"] = role
                st.session_state["logged_in"] = True
                st.session_state["info_page"] = "Accueil"  # Réinitialise l'affichage
                st.session_state.audio_running = True  # <--- Démarrage de l'audio ici
                st.session_state.audio_level = "🔊"
                st.session_state["main_section_auth"] = (
                    "Tableau de bord"  # Sélectionne le dashboard au login
                )

                st.rerun()  # Force la redirection pour afficher l'interface connectée
            else:
                message_placeholder.error("⛔ Identifiant ou mot de passe incorrect.")


# =========================================================
# 🏠 Interface après connexion (Logique principale)
# =========================================================

if st.session_state.get("logged_in"):
    role = st.session_state["user_role"]
    main_section = st.session_state["main_section_auth"]  # Récupère la sélection

    st.subheader(f"Bienvenue sur votre espace, {role.capitalize()}!")

    # --- Barre latérale : navigation principale ---
    with st.sidebar:
        st.markdown(f"### 🎛️ Menu **{role.capitalize()}**")

        main_section = st.radio(
            "🧭 Que souhaitez-vous afficher ?",
            [
                "Accueil",
                "Tableau de bord",
                "Formulaire spécifique",
                "Fonction partagée",
            ],
            key="main_section_auth_radio",
            index=[
                "Accueil",
                "Tableau de bord",
                "Formulaire spécifique",
                "Fonction partagée",
            ].index(st.session_state.get("main_section_auth", "Accueil")),
        )
        # Met à jour la variable de session après le radio button
        st.session_state["main_section_auth"] = main_section

        selected_form_path = None
        if main_section == "Formulaire spécifique":
            # Utiliser la liste des chemins des formulaires spécifiques
            form_paths = SPECIFIC_FORMS.get(role, [])
            if form_paths:
                # Créer un mapping chemin -> label pour l'affichage
                form_display_options = {
                    FORM_LABELS.get(path, path): path for path in form_paths
                }

                selected_label = st.selectbox(
                    "📄 Choisissez un formulaire",
                    list(form_display_options.keys()),
                    key="specific_form_select",
                )
                selected_form_path = form_display_options.get(selected_label)
            else:
                st.info("Aucun formulaire spécifique pour ce rôle.")

        selected_shared_key = None
        if main_section == "Fonction partagée":
            # Utiliser les clés des formulaires partagés (ex: "Agenda")
            shared_keys = list(SHARED_FORMS.keys())

            selected_key = st.selectbox(
                "🌐 Fonction partagée",
                shared_keys,
                key="shared_func_select",
                format_func=lambda x: SHARED_DISPLAY_LABELS.get(
                    x, x
                ),  # Utilise l'emoji/label
            )
            selected_shared_key = selected_key
            # Si sélectionné, on récupère le chemin pour le rendu
            selected_form_path = SHARED_FORMS.get(selected_shared_key)

        st.markdown("---")

        if st.button("🚪 Déconnexion", key="logout_button", type="primary"):
            # Mise à jour de l'état de déconnexion et arrêt de l'audio
            st.session_state["logged_in"] = False
            st.session_state["user_role"] = None
            st.session_state["info_page"] = "Accueil"
            st.session_state["audio_running"] = False
            st.session_state["main_section_auth"] = "Accueil"

            # Optionnel: Arrêter l'audio via JS avant le rerun
            # st.markdown('<script>controlAudio("pause");</script>', unsafe_allow_html=True)
            st.rerun()

    # =========================================================
    # 🖼️ Rendu du contenu principal
    # =========================================================

    if main_section == "Accueil":
        st.title(f"Bienvenue, {role.capitalize()}!")
        st.info(
            "Cette section pourrait contenir des alertes ou des résumés spécifiques à votre rôle."
        )
        # L'audio est géré par la variable audio_running et play_audio
        render_home_page(hide_audio=False)

    elif main_section == "Tableau de bord":
        st.title(f"📊 Tableau de bord {role.capitalize()}")

        try:
            # Simulation de l'appel du module
            # dashboard_module = importlib.import_module(f"modules.dashboard.dashboard_{role.lower()}")
            # dashboard_module.render()
            st.info(
                f"Fonction d'affichage du dashboard pour **{role}** appelée. Module simulé: `modules.dashboard.dashboard_{role.lower()}`"
            )
        except Exception:
            st.info(
                f"🔒 Le Tableau de bord pour le rôle **{role}** n'est pas encore implémenté ou le module est manquant."
            )

    elif main_section == "Formulaire spécifique" and selected_form_path:
        # Afficher le label convivial
        display_label = FORM_LABELS.get(selected_form_path, selected_form_path)
        st.title(f"📄 Formulaire : {display_label}")

        try:
            # form_module = importlib.import_module(f"modules.{selected_form_path.replace('/', '.')}")
            # form_module.render()
            st.info(
                f"Fonction d'affichage du formulaire **{display_label}** pour **{role}** appelée. Chemin simulé: `{selected_form_path}`"
            )
        except Exception:
            st.info(
                f"🔒 Le formulaire **{display_label}** pour le rôle **{role}** n'est pas encore implémenté."
            )

    elif main_section == "Fonction partagée" and selected_shared_key:
        # Afficher le label convivial
        display_label = SHARED_DISPLAY_LABELS.get(
            selected_shared_key, selected_shared_key
        )
        form_path = SHARED_FORMS.get(selected_shared_key)
        st.title(f"{display_label}")

        try:
            # shared_module = importlib.import_module(f"modules.{form_path.replace('/', '.')}")
            # shared_module.render()
            st.info(
                f"Fonction d'affichage de la fonctionnalité **{display_label}** appelée. Chemin simulé: `{form_path}`"
            )
        except Exception:
            st.info(
                f"🌐 La fonction partagée **{display_label}** n'est pas encore implémentée."
            )
