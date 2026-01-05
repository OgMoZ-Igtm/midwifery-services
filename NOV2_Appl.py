import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv
import os
import time
import importlib

# =========================================================
# ⚙️ CONFIGURATION ET CONSTANTES GLOBALES
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
    "GUEST": "guest2024",  # Ajout de GUEST pour la cohérence
}

# --- URL de Placeholder pour les assets statiques ---
STATIC_ASSET_URLS = {
    "img_1": "https://placehold.co/1200x400/94A3B8/FFFFFF?text=Bienvenue+sur+MSA+!",
    "img_2": "https://placehold.co/1200x400/3B82F6/FFFFFF?text=Soutien+aux+communaut%C3%A9s+cries",
    "img_3": "https://placehold.co/1200x400/10B981/FFFFFF?text=Soins+de+sage-femme+en+milieu+autochtone",
}

# --- Constantes: Chemins des Tableaux de Bord par rôle (NOUVEAU)
DASHBOARD_PATHS = {
    role: f"dashboard/dashboard_{role.lower()}" for role in USER_PASSWORDS.keys()
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

# --- Constantes: Fonctions partagées
SHARED_BUTTONS = {
    "Agenda": "📅",
    "Calendrier": "🗓️",
    "Messages": "✉️",
    "Chat": "💬",
    "Profil": "👤",
    "Settings": "⚙️",
    "Signup": "📝",
}

SHARED_FORMS = {
    "Agenda": "forms_shared/form_agenda",
    "Calendrier": "forms_shared/form_calendar",
    "Messages": "forms_shared/form_messages",
    "Chat": "forms_shared/form_chat",
    "Profil": "forms_shared/form_profile",
    "Settings": "forms_shared/form_settings",
    "Signup": "forms_shared/form_signup",
}


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
    # SHARED
    "forms_shared/form_agenda": "📅 Agenda",
    "forms_shared/form_calendar": "🗓️ Calendrier",
    "forms_shared/form_messages": "✉️ Messages",
    "forms_shared/form_chat": "💬 Chat",
    "forms_shared/form_profile": "👤 Profil",
    "forms_shared/form_settings": "⚙️ Paramètres",
    "forms_shared/form_signup": "📝 Inscription",
}

THEMATIC_GROUPS = {
    "Soins et suivi": [
        "forms_midwife/form_prenatal_care",
        "forms_midwife/form_postnatal_care",
        "forms_midwife/form_intrapartum_care",
        "forms_nurse/form_followup",
        "forms_nurse/form_vital_signs",
        "forms_doctor/form_medical_report",
    ],
    "Gestion et organisation": [
        "forms_midwife/form_patient_management",
        "forms_midwife/form_patient_file",
        "forms_nurse/form_schedule_nurse",
        "forms_doctor/form_doctor_schedule",
        "forms_admin/form_user_management",
        "forms_admin/form_global_settings",
    ],
    "Émotions et communication": [
        "forms_midwife/form_emotional_well_being",
        "forms_midwife/form_midwife_messages",
        "forms_patient/form_patient_feedback",
        "forms_shared/form_messages",
        "forms_shared/form_chat",
    ],
    "Demandes et formulaires utilitaires": [
        "forms_patient/form_request",
        "forms_guest/form_utility_service_request",
        "forms_patient/form_patient_prescription_request",
        "forms_shared/form_signup",
    ],
    "Formation et apprentissage": [
        "forms_student/form_observation",
        "forms_student/form_reflection",
        "forms_intern/form_training_log",
        "forms_doctoral/form_research_note",
    ],
}

THEME_COLORS = {
    "Soins": "#e3f2fd",
    "Gestion": "#f1f8e9",
    "Émotion": "#fce4ec",
}

ROLE_COLORS = {
    "MIDWIFE": "#f8bbd0",
    "NURSE": "#b2dfdb",
    "DOCTOR": "#c5cae9",
    "PATIENT": "#ffe0b2",
    "STUDENT": "#dcedc8",
    "GUEST": "#f0f4c3",
    "INTERN": "#e1bee7",
    "DOCTORAL": "#d7ccc8",
    "ADMIN": "#ffccbc",
}

# --- Constantes: Icônes des formulaires
FORM_ICONS = {
    "birth": "🧺",
    "prescription": "💊",
    "emergency": "🚨",
    "schedule": "📅",
    "notes": "📝",
    "feedback": "💬",
    "observation": "👀",
    "reflection": "🪞",
    "report": "📊",
    "appointment": "📆",
    "inventory": "📦",
    "incident": "⚠️",
    "research": "🔬",
    "settings": "⚙️",
    "default": "📄",
}


ROLE_ICONS = {
    "MIDWIFE": "🧺",
    "DOCTOR": "🩺",
    "NURSE": "💉",
    "PATIENT": "🫶",
    "STUDENT": "📚",
    "INTERN": "🧪",
    "DOCTORAL": "🎓",
    "ADMIN": "🛠️",
    "GUEST": "👤",
}


# =========================================================
# 🛠️ FONCTIONS UTILITAIRES
# =========================================================


def load_static_asset(asset_name):
    """Charge l'URL d'un asset statique simulé (usage pour URL/HTML)."""
    return STATIC_ASSET_URLS.get(asset_name, "")


def show_public_header():
    """Affiche l'en-tête public avec les liens d'information stylisés (Goal 1)."""
    # CSS pour styliser les boutons comme des liens de texte
    st.markdown(
        """
        <style>
        .public-header-row .stButton > button {
            background: none !important;
            border: none !important;
            color: #1e40af; /* Couleur de lien */
            padding: 5px 10px;
            text-decoration: none !important;
            box-shadow: none;
        }
        .public-header-row .stButton > button:hover {
            background-color: #eff6ff !important;
            text-decoration: none !important;
            color: #3b82f6 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("MSA - Services de sage-femme")
    st.caption(
        "Plateforme de soutien et de coordination dans les communautés de Waskaganish, Chisasibi et Mistissini"
    )

    cols = st.columns([1, 1, 1, 1, 1, 1, 1])
    links = {
        "Accueil": "🏠",
        "Mission": "🎯",
        "Communautés": "📍",
        "Contact": "📞",
        "FAQ": "❓",
        "Papotines": "👶",  # Goal 1: Ajout de Papotines
    }

    # Utilisation de st.button stylisé pour maintenir la gestion de l'état
    st.markdown("<div class='public-header-row'>", unsafe_allow_html=True)
    for col, (label, icon) in zip(cols, links.items()):
        with col:
            if st.button(f"{icon} {label}", key=f"info_{label}"):
                st.session_state["info_page"] = label
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)



def render_info_section():
    """Affiche les sections d'information spécifiques."""
    current_page = st.session_state.get("info_page", "Accueil")
    if current_page != "Accueil":
        st.title(f"ℹ️ {current_page}")
        st.info(f"Contenu détaillé pour la section **{current_page}**.")
        if st.button("Retour à l'accueil"):
            st.session_state["info_page"] = "Accueil"
            st.rerun()


def render_bebe_experience()
    render_home_page()  # Ajout du carrousel et de la présentation ici
    st.markdown("---")
    handle_login()  # Affiche le formulaire de connexion sur la page d'accueil



def render_home_page():
    """Affiche le carrousel (Goal 4) et le squelette de la page de présentation (Goal 5)."""
    # --- Carrousel Dynamique ---
    CAROUSEL_HTML = f"""
    <style>
        /* Styles pour un carrousel propre et réactif */
        .carousel-container {{
            overflow: hidden;
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }}
        .carousel-track {{
            display: flex;
            transition: transform 1s ease-in-out; 
            width: 300%; 
        }}
        .carousel-item {{
            min-width: 33.33%;
            box-sizing: border-box;
        }}
        .carousel-item img {{
            width: 100%;
            height: 400px;
            display: block;
            object-fit: cover;
            border-radius: 8px;
        }}
    </style>
    <div class="carousel-container">
        <div class="carousel-track" id="msa-carousel-track">
            <div class="carousel-item"><img src="{load_static_asset('img_1')}" alt="Image 1"></div>
            <div class="carousel-item"><img src="{load_static_asset('img_2')}" alt="Image 2"></div>
            <div class="carousel-item"><img src="{load_static_asset('img_3')}" alt="Image 3"></div>
        </div>
    </div>
    <script>
        const track = document.getElementById('msa-carousel-track');
        if (track && !window.msaCarouselInterval) {{
            let currentIdx = 0;
            const totalItems = 3;
            const intervalTime = 6000; 

            window.msaCarouselInterval = setInterval(() => {{
                currentIdx = (currentIdx + 1) % totalItems;
                const offset = -currentIdx * 100 / totalItems;
                
                // Correction de l'erreur 'offset': double accolade
                track.style.transform = `translateX(${{offset}}%)`; 
                
            }}, intervalTime);
        }}
    </script>
    """
    st.markdown(CAROUSEL_HTML, unsafe_allow_html=True)

    # --- Squelette de Page de Présentation (Goal 5) ---
    st.subheader("💡 À Propos de MSA.")
    st.markdown(
        """
    Le projet Midwifery Service Application, en abrégé "MSA", est une initiative visant à améliorer l'accès et la qualité des soins de sage-femme pour les mères et les familles des communautés cries de Waskaganish, Chisasibi et Mistissini (à venir), dans les Territoires-cries-de-la-Baie-James, au nord du Québec.

    Notre objectif principal est d'offrir un soutien médical et émotionnel complet, respectueux des cultures autochtones.

    ---
    ### Nos axes principaux :
    * **Soins de proximité :** Réduction des déplacements pour les mères en offrant des services directement dans les communautés.
    * **Intégration culturelle :** Collaboration étroite avec les Aînés et les leaders communautaires pour garantir des pratiques respectueuses des traditions.
    * **Formation et réseau :** Création d'un réseau sécurisé pour les professionnels de la santé afin de partager les informations et les meilleures pratiques.

    #### Partenariats clés 

    Certaines variables recueillies ici ont été spécifiquement demandées par Nishiyuu. D'autres ont été sélectionnées à la suite de diverses consultations avec les Services de sage-femme et s'inspirent de : 

    * The National Indigenous Association of Midwives 
    * I-CLSC, Care 4, CHB, RSFQ 
    * The Canadian Midwifery Minimum Database 
    * MSSS 

    📊 L’analyse des données est une démarche publique et sera communiquée chaque année aux communautés d’Eeyou Istchee par le biais du rapport annuel des Services de sage-femme et du Cree Health Board.

    ❤️ Merci à toutes et tous pour votre engagement à offrir des soins de sage-femme de haute qualité aux familles d’Eeyou Istchee.
    """
    )


def handle_login():
    """Gère le formulaire de connexion et la redirection."""
    st.subheader("🧡 Soyez les bienvenues !")
    message_placeholder = st.empty()

    with st.form("msa_login_form", clear_on_submit=True):
        username = st.text_input(
            "Identifiant (rôle)",
            placeholder="Ex: MIDWIFE, DOCTOR, PATIENT...",
        ).upper()
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter", type="primary")

    if submitted:
        role = username.upper()
        if role in USER_PASSWORDS and password == USER_PASSWORDS[role]:
            message_placeholder.success(
                f"✅ Connexion réussie en tant que **{role}**. Redirection..."
            )

            current_time = time.time()

            # Mise à jour de la dernière session si une session précédente a existé
            if st.session_state.get("login_time"):
                st.session_state["last_session"] = {
                    "role": st.session_state.get("user_role"),
                    "start": st.session_state["login_time"],
                    "end": current_time,
                }

            # Définition de la nouvelle session
            st.session_state["user_role"] = role
            st.session_state["logged_in"] = True
            st.session_state["info_page"] = "Accueil"
            # Les lignes audio ont été supprimées ici.
            st.session_state["login_time"] = (
                current_time  # Goal 6: Capture l'heure de connexion
            )
            # Initialisation de la section de navigation
            st.session_state["main_section_auth"] = "Accueil"
            st.session_state["selected_form"] = None

            time.sleep(0.5)
            st.rerun()
        else:
            message_placeholder.error("⛔ Identifiant ou mot de passe incorrect.")


def get_all_forms_for_role(role):
    specific = SPECIFIC_FORMS.get(role, [])
    shared = list(SHARED_FORMS.values())
    return specific + shared


def load_module_content(module_key):
    """
    Simule le chargement et l'affichage du contenu d'un module/dashboard.
    Utilise la structure de chemin demandée par l'utilisateur (dashboard/..., modules/...)
    """
    role = st.session_state.get("user_role", "GUEST").capitalize()

    # Détermination du chemin de fichier simulé pour l'affichage
    if module_key.startswith("dashboard/"):
        module_path = f"{module_key}.py"
        label = f"Tableau de Bord : {module_key.split('_')[-1].capitalize()}"
        type_content = "Dashboard"
        color = "#38bdf8"  # Blue for dashboard
    elif module_key in SHARED_FORMS.values():
        module_path = f"modules/shared/{module_key.split('/')[-1]}.py"
        label = FORM_LABELS.get(module_key, module_key.split("/")[-1])
        type_content = "Partagé"
        color = "#10b981"  # Green for shared
    else:  # Specific Forms (e.g., forms_midwife/form_birth_plan)
        # On simule le chemin comme modules/form_birth_plan.py
        form_name = module_key.split("/")[-1]
        module_path = f"modules/{form_name}.py"
        label = FORM_LABELS.get(module_key, form_name)
        type_content = "Spécifique"
        color = "#f97316"  # Orange for specific

    st.markdown(
        f"""
        <div style="background-color: {color}; color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <h3>{label}</h3>
            <p><strong>Fichier simulé :</strong> <code>{module_path}</code></p>
            <p>Contenu simulé chargé pour le rôle <strong>{role}</strong>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Corps de la simulation
    st.subheader(f"Détails du {type_content}")
    with st.expander("Voir le squelette du formulaire/dashboard", expanded=True):
        st.markdown(
            f"**Ceci est un placeholder pour le contenu dynamique du fichier {module_path}.**"
        )
        st.code(
            f"""
# Contenu du fichier {module_path}

import streamlit as st
# ... imports spécifiques ...

def render_{form_name.replace('-', '_')}():
    st.markdown("## {label}")
    st.write("Implémentation du formulaire ou des KPIs ici...")
    # ... logique métier ...

if __name__ == "__main__":
    render_{form_name.replace('-', '_')}()
        """,
            language="python",
        )

    if type_content != "Dashboard":
        with st.form(f"form_simulation_{module_key.replace('/', '_')}"):
            st.text_input("Champ de test 1", placeholder="Entrez une valeur")
            st.date_input("Champ de test 2 (Date)")
            st.form_submit_button("Simuler la Soumission", type="primary")


def render_authenticated_interface():
    """Affiche l'interface complète après connexion, y compris la sidebar améliorée."""
    # 🔐 Sécurité : définir le rôle dès le début
    role = st.session_state.get("user_role", "MIDWIFE")
    role_icon = ROLE_ICONS.get(role.upper(), "👤")
    color = ROLE_COLORS.get(role.upper(), "#eeeeee")

    # 🎛️ Affichage dans la barre latérale
    with st.sidebar:
        # --- Détermination de la salutation (Goal 6) ---
        current_hour = time.localtime().tm_hour
        if 5 <= current_hour < 12:
            greeting = "Bonjour"
        elif 12 <= current_hour < 18:
            greeting = "Bon après-midi"
        else:
            greeting = "Bonsoir"

        st.markdown(f"## {greeting} sur votre espace, {role.capitalize()}! 👋")

        # --- 4. Sélecteur de Rôle (Nouvelle fonctionnalité) ---
        new_role = st.selectbox(
            "🚀 Tester un autre rôle",
            options=list(USER_PASSWORDS.keys()),
            index=list(USER_PASSWORDS.keys()).index(role),
            key="role_switcher",
        )

        if new_role != role:
            # Met à jour le rôle et simule une nouvelle connexion/session
            current_time = time.time()
            st.session_state["last_session"] = {
                "role": role,
                "start": st.session_state["login_time"],
                "end": current_time,
            }
            st.session_state["user_role"] = new_role
            st.session_state["login_time"] = current_time
            st.session_state["main_section_auth"] = (
                "Tableau de bord"  # Redirection par défaut au changement de rôle
            )
            st.session_state["selected_form"] = None
            st.rerun()

        st.markdown("---")

        st.markdown(f"### 🎛️ Menu **{role.capitalize()}**")
        st.markdown(f"{role_icon} Rôle actif : **{role.capitalize()}**.")
        st.markdown("---")

        # Détails de Session (Goal 6)
        st.markdown("#### Détails de Session")

        login_timestamp = st.session_state.get("login_time")
        if login_timestamp:
            login_dt = time.localtime(login_timestamp)
            st.markdown(
                f"**Connexion :** {time.strftime('%Y-%m-%d', login_dt)} à {time.strftime('%H:%M:%S', login_dt)}"
            )

        last_sess = st.session_state.get("last_session", {})
        if last_sess and last_sess.get("start") and last_sess.get("end"):
            start_dt = time.localtime(last_sess["start"])
            end_dt = time.localtime(last_sess["end"])
            st.markdown("---")
            st.markdown(f"**Dernière Session ({last_sess['role'].capitalize()})**:")
            st.markdown(f"Déb. : {time.strftime('%Y-%m-%d %H:%M:%S', start_dt)}")
            st.markdown(f"Fin : {time.strftime('%Y-%m-%d %H:%M:%S', end_dt)}")

        st.markdown("---")  # Séparateur pour le menu de navigation

        main_section = st.radio(
            "🧭 Que souhaitez-vous afficher ?",
            [
                "Accueil",
                "Tableau de bord",
                "Formulaire spécifique",
                "Fonction partagée",
            ],
            key="main_section_auth",
            index=[
                "Accueil",
                "Tableau de bord",
                "Formulaire spécifique",
                "Fonction partagée",
            ].index(st.session_state.get("main_section_auth", "Accueil")),
        )

        selected_content_key = None
        if main_section == "Formulaire spécifique":
            form_options_specific = SPECIFIC_FORMS.get(role, [])
            # Map form paths to their display labels
            display_options_specific = {
                FORM_LABELS.get(p, p.split("/")[-1]): p for p in form_options_specific
            }

            if form_options_specific:
                selected_label = st.selectbox(
                    "📄 Choisissez un formulaire",
                    list(display_options_specific.keys()),
                    key="specific_form_select",
                )
                selected_content_key = display_options_specific.get(selected_label)
            else:
                st.info("Aucun formulaire spécifique pour ce rôle.")
        elif main_section == "Fonction partagée":
            selected_label = st.selectbox(
                "🌐 Fonction partagée",
                list(SHARED_BUTTONS.keys()),
                key="shared_func_select",
            )
            selected_content_key = SHARED_FORMS.get(selected_label)

        st.session_state["selected_form"] = selected_content_key

        # Bouton de déconnexion
        st.markdown("---")
        if st.button("🚪 Déconnexion", key="logout_button", type="primary"):
            st.session_state["logged_in"] = False
            st.session_state["user_role"] = None
            st.session_state["info_page"] = "Accueil"
            st.session_state["selected_form"] = None

            # Mettre à jour la dernière session au moment de la déconnexion
            st.session_state["last_session"] = {
                "role": role,
                "start": st.session_state["login_time"],
                "end": time.time(),
            }
            st.session_state["login_time"] = (
                None  # Réinitialiser l'heure de connexion actuelle
            )
            st.rerun()

    # --- Rendu du contenu principal après connexion ---
    # Récupération de l'état de la navigation après la sidebar
    main_section = st.session_state.get("main_section_auth", "Accueil")
    selected_content_key = st.session_state.get("selected_form")

    # 🌿 Affichage des formulaires par thème (reste dans le main body, mais est principalement décoratif)
    st.markdown(f"### {role_icon} Formulaires pour le rôle : **{role.capitalize()}**")

    for theme, paths in THEMATIC_GROUPS.items():
        filtered = [
            p
            for p in paths
            if p in SPECIFIC_FORMS.get(role, []) + list(SHARED_FORMS.values())
        ]
        if filtered:
            with st.expander(f"📂 {theme}", expanded=False):
                for form_path in filtered:
                    label = FORM_LABELS.get(form_path, form_path.split("/")[-1])

                    # Boutons d'action pour le contenu (simule la navigation dans la page principale)
                    if st.button(
                        f"{label}",
                        key=f"theme_button_{form_path.replace('/', '_')}",
                        help=f"Ouvrir le formulaire {label}",
                    ):
                        # Force la navigation vers la bonne section
                        if form_path in SPECIFIC_FORMS.get(role, []):
                            st.session_state["main_section_auth"] = (
                                "Formulaire spécifique"
                            )
                        elif form_path in SHARED_FORMS.values():
                            st.session_state["main_section_auth"] = "Fonction partagée"

                        st.session_state["selected_form"] = form_path
                        st.rerun()

    if main_section == "Accueil":
        st.subheader("Informations Clés Professionnelles")
        st.info(
            "Ceci est l'accueil personnalisé après connexion. Utilisez le menu de gauche pour accéder au Tableau de bord ou aux formulaires/fonctions. "
            "Le sélecteur de rôle en haut de la barre latérale vous permet de changer d'utilisateur sans vous déconnecter."
        )
    elif main_section == "Tableau de bord":
        dashboard_path = DASHBOARD_PATHS.get(role, "dashboard/dashboard_guest")
        load_module_content(dashboard_path)

    elif main_section == "Formulaire spécifique" and selected_content_key:
        load_module_content(selected_content_key)

    elif main_section == "Fonction partagée" and selected_content_key:
        load_module_content(selected_content_key)

    elif main_section == "Formulaire spécifique" or main_section == "Fonction partagée":
        st.warning("Veuillez choisir un module dans la barre latérale pour l'afficher.")


def main():
    """Fonction principale pour initialiser et rendre l'application Streamlit."""
    st.set_page_config(layout="wide")

    # 1. Initialisation de l'état
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["info_page"] = "Accueil"
        st.session_state["main_section_auth"] = "Accueil"
        st.session_state["last_session"] = {}
        st.session_state["login_time"] = None
        st.session_state["selected_form"] = None

    # 2. Rendu de l'interface
    if st.session_state["logged_in"]:
        render_authenticated_interface()
    else:
        show_public_header()
        render_info_section()

        if st.session_state.get("info_page", "Accueil") == "Accueil":
            st.markdown("---")
            col_login, col_home = st.columns([1, 2])
            with col_login:
                handle_login()  # Goal 2: Gère l'authentification
            with col_home:
                render_home_page()  # Goal 4 & 5: Gère l'affichage du carrousel et de l'info


if __name__ == "__main__":
    main()
