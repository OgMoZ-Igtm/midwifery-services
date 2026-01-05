# =========================================================
# 1. IMPORTS ET DÉPENDANCES
# =========================================================

# 1.1. Librairies Standard
import os
import time
import importlib

# 1.2. Librairies Tierces
import streamlit as st
import requests
import folium
from dotenv import load_dotenv
from streamlit_folium import st_folium

# 1.3. Modules Customisés (Assumant qu'ils existent)
from modules.utils.session import inject_session_keys
from modules.public import form_home
from modules.utils import (
    render_weather_card,
    render_cultural_carousel,
    # L'import de render_bebe_experience est laissé ici bien qu'une version locale soit définie plus bas
    render_bebe_experience,
)
from modules.public.form_registry import LINKED_FORMS_EXTENDED


# 1.4. Dashboards par rôle
from modules.dashboard import (
    dashboard_admin,
    dashboard_midwife,
    dashboard_doctor,
    dashboard_nurse,
    dashboard_patient,
    dashboard_student,
    dashboard_guest,
    dashboard_intern,
    dashboard_doctoral,
)

# =========================================================
# 2. CONFIGURATION ET CONSTANTES GLOBALES
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

# --- URL de Placeholder pour les assets statiques ---
STATIC_ASSET_URLS = {
    "img_1": "https://placehold.co/1200x400/94A3B8/FFFFFF?text=+MSA",
    "img_2": "https://placehold.co/1200x400/3B82F6/FFFFFF?text=Soutien+aux+communaut%C3%A9s+cries",
    "img_3": "https://placehold.co/1200x400/10B981/FFFFFF?text=Soins+de+sage-femme+en+milieu+autochtone",
}

# --- Constantes: Chemins des Tableaux de Bord par rôle
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
# 3. FONCTIONS UTILITAIRES (HELPERS)
# =========================================================


def load_static_asset(asset_name):
    """Charge l'URL d'un asset statique simulé (usage pour URL/HTML)."""
    return STATIC_ASSET_URLS.get(asset_name, "")


def render_bebe_experience():
    """Affiche l'animation du nouveau-né et le son (version locale)."""
    # Chemin d'accès simulé
    audio_path = "/home/ygd/projets-midwifery-Services/static/bebe_pleure.mp3"

    # 🌸 Animation typewriter
    st.markdown(
        """
        <div style="border: 2px solid #ffb6c1; border-radius: 12px; padding: 1rem; background-color: #fff0f5;">
            <h3 style="color:#d63384;">👶 Le souffle de la vie</h3>
            <div id="typewriter" style="font-size:1.1rem; font-family:monospace; color:#333;"></div>
        </div>
        <script>
        const text = "Un nouveau-né pleure doucement... et le monde s’éveille avec tendresse.";
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                document.getElementById("typewriter").innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        // Utilisation d'un drapeau pour éviter l'exécution multiple dans Streamlit
        if (!document.getElementById("typewriter").getAttribute("data-typed")) {
            typeWriter();
            document.getElementById("typewriter").setAttribute("data-typed", "true");
        }
        </script>
    """,
        unsafe_allow_html=True,
    )

    # 🔊 Audio synchronisé
    st.audio(audio_path, format="audio/mp3")


def render_home_page():
    """Affiche le carrousel et le squelette de la page de présentation."""
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
        // Utiliser une vérification de l'existence de l'intervalle dans window
        if (track && !window.msaCarouselInterval) {{
            let currentIdx = 0;
            const totalItems = 3;
            const intervalTime = 6000;

            window.msaCarouselInterval = setInterval(() => {{
                currentIdx = (currentIdx + 1) % totalItems;
                const offset = -currentIdx * 100 / totalItems;

                track.style.transform = `translateX(${{offset}}%)`;
            }}, intervalTime);
        }}
    </script>
    """
    st.markdown(CAROUSEL_HTML, unsafe_allow_html=True)

    # --- Squelette de Page de Présentation ---
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


def show_public_header():
    """Affiche l'en-tête public avec les liens d'information stylisés."""
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

    st.title("Midwifery Services Application")
    st.caption(
        "Plateforme de soutien et de coordination dans les communautés de Waskaganish, Chisasibi et Mistissini"
    )

    # --- Bande horizontale avec liens cliquables en bleu ---
    # La logique de navigation ici n'est pas Streamlit-native (ancre #)
    cols = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    labels = [
        "Accueil",
        "Mission",
        "Notre équipe",
        "Contact",
        "FAQ",
        "Les Papotines",
        "Pour nous joindre",
        "Liens utiles",
    ]

    st.markdown("<div style='margin-bottom:0.5rem;'>", unsafe_allow_html=True)
    for col, label in zip(cols, labels):
        with col:
            # Si le lien est cliqué, on met à jour la session state pour la navigation publique
            if st.button(label, key=f"nav_pub_{label}"):
                st.session_state["info_page"] = label
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Ligne de séparation douce
    st.markdown(
        "<hr style='margin-top:0.5rem;margin-bottom:1rem;border:1px solid #ccc;'>",
        unsafe_allow_html=True,
    )


def render_info_section():
    """
    Affiche les sections d'information spécifiques basées sur st.session_state["info_page"].
    Ce contenu est destiné à la partie publique.
    """
    current_page = st.session_state.get("info_page", "Accueil")

    if current_page == "Accueil":
        st.title("🏠 Bienvenue ❤️ !")
        st.write(
            "Veuillez vous connecter pour accéder à votre Tableau de bord personnel."
        )
        render_bebe_experience()
        render_home_page()  # Ajout du carrousel et de la présentation ici
        st.markdown("---")
        handle_login()  # Affiche le formulaire de connexion sur la page d'accueil

    elif current_page == "Mission":
        st.title("🎯 Notre mission")
        st.write(
            "Accompagner, soutenir, et honorer chaque naissance avec respect et amour."
        )
    elif current_page == "Notre équipe":
        st.title("📍 Notre équipe")
        st.write(
            "Découvrez les sages-femmes, infirmières et accompagnantes qui font vivre ce projet."
        )
        # Assumant que form_equipe.render() affiche la page d'équipe
        # form_equipe.render() # L'import form_equipe est fait mais le render n'est pas dans la fonction originale
    elif current_page == "Contact" or current_page == "Pour nous joindre":
        st.title("📞 Contact")
        st.write("Pour toute question, vous pouvez nous écrire ou nous appeler.")
    elif current_page == "FAQ":
        st.title("❓ Foire aux questions")
        st.write("Les réponses aux questions les plus fréquentes.")
    elif current_page == "Les Papotines":
        st.title("🎀 Les Papotines")
        st.write("Un espace de parole, de partage et de douceur entre femmes.")
    elif current_page == "Liens utiles":
        st.title("🔗 Liens utiles")
        st.write("Ressources, partenaires et documents à consulter.")
    # On vérifie si la page actuelle est un formulaire spécifique
    elif current_page in LINKED_FORMS:
        LINKED_FORMS[current_page].render()

    # Bouton de retour à l'accueil
    if current_page != "Accueil":
        st.markdown("---")
        if st.button("⬅️ Retour à l'accueil"):
            st.session_state["info_page"] = "Accueil"
            st.rerun()


def handle_login():
    """Gère le formulaire de connexion et la redirection."""

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

            # Mise à jour de la dernière session
            if st.session_state.get("login_time"):
                st.session_state["last_session"] = {
                    "role": st.session_state.get("user_role"),
                    "start": st.session_state["login_time"],
                    "end": current_time,
                }

            # Définition de la nouvelle session
            st.session_state["user_role"] = role
            st.session_state["logged_in"] = True
            st.session_state["login_time"] = current_time
            st.session_state["main_section_auth"] = (
                "Tableau de bord"  # Défaut pour l'auth
            )
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
    """
    role = st.session_state.get("user_role", "GUEST").capitalize()

    # Détermination du chemin de fichier simulé pour l'affichage
    if module_key.startswith("dashboard/"):
        form_name = module_key.split("_")[-1]
        module_path = f"{module_key}.py"
        label = f"Tableau de Bord : {form_name.capitalize()}"
        type_content = "Dashboard"
        color = "#38bdf8"  # Blue for dashboard
    elif module_key in SHARED_FORMS.values():
        form_name = module_key.split("/")[-1]
        module_path = f"modules/shared/{form_name}.py"
        label = FORM_LABELS.get(module_key, form_name)
        type_content = "Partagé"
        color = "#10b981"  # Green for shared
    else:  # Specific Forms (e.g., forms_midwife/form_birth_plan)
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


# =========================================================
# 4. LOGIQUE D'EXÉCUTION AUTHENTIFIÉE
# =========================================================


def render_startup_animation():
    """Affiche une animation simple pour le démarrage."""
    st.markdown(
        """
        <style>
        @keyframes plume {
            0%   {transform: translateY(-20px); opacity: 0;}
            50%  {transform: translateY(0px); opacity: 1;}
            100% {transform: translateY(10px); opacity: 0.8;}
        }

        .plume {
            font-size: 48px;
            animation: plume 2s ease-in-out infinite;
            text-align: center;
            margin-top: 2rem;
        }

        #typewriter_start {
            font-family: 'Courier New', monospace;
            font-size: 1.2rem;
            white-space: nowrap;
            overflow: hidden;
            border-right: 3px solid #ff69b4;
            width: 0;
            animation: typing 4s steps(60, end) forwards;
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        </style>

        <div class="plume">🪶</div>
        <div id="typewriter_start">Bienvenue dans l’espace sacré de la maïeutique numérique...</div>
    """,
        unsafe_allow_html=True,
    )


def redirect_to_dashboard():
    """Redirection vers le bon tableau de bord selon le rôle de la session."""
    role = st.session_state.get("user_role")

    if role == "ADMIN":
        dashboard_admin.render()
    elif role == "MIDWIFE":
        dashboard_midwife.render()
    elif role == "DOCTOR":
        dashboard_doctor.render()
    elif role == "NURSE":
        dashboard_nurse.render()
    elif role == "PATIENT":
        dashboard_patient.render()
    elif role == "STUDENT":
        dashboard_student.render()
    elif role == "INTERN":
        dashboard_intern.render()
    elif role == "DOCTORAL":
        dashboard_doctoral.render()
    elif role == "GUEST":
        dashboard_guest.render()
    else:
        st.warning("Rôle non reconnu. Veuillez contacter l’administratrice.")


def render_authenticated_interface():
    """Affiche l'interface complète après connexion, y compris la sidebar améliorée."""
    role = st.session_state.get("user_role", "MIDWIFE")
    role_icon = ROLE_ICONS.get(role.upper(), "👤")
    # color = ROLE_COLORS.get(role.upper(), "#eeeeee") # Non utilisé ici

    # 🎛️ Affichage dans la barre latérale
    with st.sidebar:
        # --- Détermination de la salutation ---
        current_hour = time.localtime().tm_hour
        if 5 <= current_hour < 12:
            greeting = "Bonjour"
        elif 12 <= current_hour < 18:
            greeting = "Bon après-midi"
        else:
            greeting = "Bonsoir"

        st.markdown(f"## {greeting} sur votre espace, {role.capitalize()}! 👋")

        # --- Sélecteur de Rôle ---
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
            st.session_state["main_section_auth"] = "Tableau de bord"
            st.session_state["selected_form"] = None
            st.rerun()

        st.markdown("---")

        st.markdown(f"### 🎛️ Menu **{role.capitalize()}**")
        st.markdown(f"{role_icon} Rôle actif : **{role.capitalize()}**.")
        st.markdown("---")

        # Détails de Session
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

        st.markdown("---")

        # --- Menu de navigation (Tableau de bord et Formulaires) ---
        if st.button("Tableau de bord", key="btn_dash"):
            st.session_state["main_section_auth"] = "Tableau de bord"
            st.session_state["selected_form"] = None
            st.rerun()

        st.markdown("#### Formulaires et outils")
        st.session_state["selected_form"] = st.selectbox(
            "Sélectionner un formulaire:",
            options=["-- Sélectionner --"] + get_all_forms_for_role(role),
            format_func=lambda x: FORM_LABELS.get(
                x, x.split("/")[-1].replace("_", " ").title()
            ),
            key="form_selector",
        )
        if st.session_state["selected_form"] != "-- Sélectionner --":
            st.session_state["main_section_auth"] = "Formulaire"
            st.rerun()

    # 🖥️ Affichage principal
    if st.session_state.get("main_section_auth") == "Tableau de bord":
        st.title(f"{role_icon} Tableau de bord {role.capitalize()}")
        redirect_to_dashboard()
    elif (
        st.session_state.get("selected_form")
        and st.session_state["selected_form"] != "-- Sélectionner --"
    ):
        load_module_content(st.session_state["selected_form"])
    else:
        # Page par défaut après connexion (peut-être un message d'accueil plus simple)
        st.title("Espace Authentifié")
        st.info(
            "Utilisez la barre latérale pour naviguer vers votre tableau de bord ou un formulaire spécifique."
        )
        # Affichage des infos du rôle
        st.markdown(f"### 🎯 Accès à votre espace")
        redirect_to_dashboard()


# =========================================================
# 5. POINT D'ENTRÉE PRINCIPAL DE L'APPLICATION
# =========================================================


@inject_session_keys
def main():
    """Fonction principale pour orchestrer l'application."""

    # 1. Vérification de l'état d'authentification
    if not st.session_state.get("logged_in"):
        # --- Logique publique (Non authentifiée) ---
        show_public_header()
        render_info_section()
        # Le formulaire de connexion est inclus dans render_info_section() pour "Accueil"

    else:
        # --- Logique privée (Authentifiée) ---
        render_authenticated_interface()


# =========================================================
# 6. EXÉCUTION
# =========================================================

if __name__ == "__main__":
    main()
