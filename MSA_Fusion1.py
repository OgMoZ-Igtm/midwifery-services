# =========================================================================
# 1. IMPORTS & INITIALISATION
# =========================================================================

# 🌿 Imports fondamentaux
import streamlit as st
import time
import os
import base64
import importlib
import requests
import folium
import datetime
from streamlit_folium import st_folium

# 📦 Modules internes et Registres
from modules.public.form_registry import form_registry, get_all_forms, get_shared_forms
from modules.shared.form_carrousel_soins import (
    render_carrousel_soins_form,
    render_bebe_pleure,
)

# from modules.public.forms_registry import PUBLIC_FORMS_REGISTRY # Utilisé pour la navigation publique, non nécessaire ici si form_registry est complet

# 📦 Imports des Dashboards par rôle
from modules.dashboard.dashboard_guest import form_dashboard_guest
from modules.dashboard.dashboard_admin import form_dashboard_admin
from modules.dashboard.dashboard_midwife import form_dashboard_midwife
from modules.dashboard.dashboard_doctor import form_dashboard_doctor
from modules.dashboard.dashboard_nurse import form_dashboard_nurse
from modules.dashboard.dashboard_patient import form_dashboard_patient
from modules.dashboard.dashboard_student import form_dashboard_student
from modules.dashboard.dashboard_intern import form_dashboard_intern
from modules.dashboard.dashboard_doctoral import form_dashboard_doctoral

# 📦 Imports des Formulaires partagés
from modules.shared.form_shared_agenda import form_shared_agenda
from modules.shared.form_shared_calendar import form_shared_calendar
from modules.shared.form_shared_profile import form_shared_profile
from modules.shared.form_shared_settings import form_shared_settings
from modules.shared.form_shared_signup import form_shared_signup
from modules.shared.form_shared_stats import form_shared_stats
from modules.shared.form_shared_inbox import form_shared_inbox

# 📦 Imports de tous les Formulaires spécifiques (pour que load_form puisse les trouver)
# NOTE: Ces imports sont nécessaires pour garantir que Python charge les modules
# et que la fonction `get_all_forms()` ait connaissance de tous les chemins.

# --- ADMIN ---
import modules.forms_admin.admin_access_audit_log_form
import modules.forms_admin.admin_model_configuration_form
import modules.forms_admin.admin_statistical_report_form
import modules.forms_admin.admin_user_role_management_form

# --- MIDWIFE ---
import modules.forms_midwife.midwife_prenatal_care_form
import modules.forms_midwife.midwife_postnatal_care_form
import modules.forms_midwife.midwife_intrapartum_care_form
import modules.forms_midwife.midwife_throughout_midwifery_care_form
import modules.forms_midwife.midwife_prenatal_consultation_form
import modules.forms_midwife.midwife_postpartum_follow_up_form
import modules.forms_midwife.midwife_partogram_form
import modules.forms_midwife.midwife_prenatal_follow_up_form
import modules.forms_midwife.midwife_birth_plan_consent_form
import modules.forms_midwife.midwife_childbirth_form
import modules.forms_midwife.midwife_contact_info_form
import modules.forms_midwife.midwife_daily_tasks_form
import modules.forms_midwife.midwife_demographics_form
import modules.forms_midwife.midwife_education_prevention_form
import modules.forms_midwife.midwife_emotional_well_being_form
import modules.forms_midwife.midwife_follow_up_form
import modules.forms_midwife.midwife_incident_report_form
import modules.forms_midwife.midwife_initial_anamnesis_form
import modules.forms_midwife.midwife_initial_routine_form
import modules.forms_midwife.midwife_messaging_form
import modules.forms_midwife.midwife_nutrition_form
import modules.forms_midwife.midwife_patient_file_form
import modules.forms_midwife.midwife_patient_management_form
import modules.forms_midwife.midwife_patients_alerts_form
import modules.forms_midwife.midwife_resume_data_recorded_form
import modules.forms_midwife.midwife_visit_history_form
import modules.forms_midwife.midwife_workshops_form

# --- DOCTOR ---
import modules.forms_doctor.doctor_birth_care_plan_form
import modules.forms_doctor.doctor_cesarean_operative_report_form
import modules.forms_doctor.doctor_fetal_anomaly_assessment_form
import modules.forms_doctor.doctor_final_discharge_prescriptions_form
import modules.forms_doctor.doctor_inter_specialities_consultation_request_form
import modules.forms_doctor.doctor_ultrasound_report_form
import modules.forms_doctor.doctor_supervision_form
import modules.forms_doctor.doctor_due_date_calculator_form

# --- NURSE ---
import modules.forms_nurse.nurse_administration_record_form
import modules.forms_nurse.nurse_admission_discharge_checklist_form
import modules.forms_nurse.nurse_patient_education_postpartum_form
import modules.forms_nurse.nurse_postpartum_care_record
import modules.forms_nurse.nurse_vital_signs_form
import modules.forms_nurse.nurse_evolution_notes_vitals_signs
import modules.forms_nurse.nurse_fetal_monotoring_pain_assessment_form

# --- PATIENT ---
import modules.forms_patient.patient_appointment_booking_form
import modules.forms_patient.patient_appointment_followup_form
import modules.forms_patient.patient_communication_prefs_form
import modules.forms_patient.patient_feedback_form
import modules.forms_patient.patient_messaging_form
import modules.forms_patient.patient_obstetric_informed_consent_form
import modules.forms_patient.patient_pre_consultation_questionnaire_form
import modules.forms_patient.patient_pregnancy_log_form
import modules.forms_patient.patient_prescription_request_form
import modules.forms_patient.patient_satisfaction_survey_form
import modules.forms_patient.patient_symptom_logs_form

# --- DOCTORAL ---
import modules.forms_doctoral.doctoral_data_extraction_form
import modules.forms_doctoral.doctoral_research_consent_form
import modules.forms_doctoral.doctoral_thesis_report_form

# --- INTERN ---
import modules.forms_intern.intern_clinical_observations_form
import modules.forms_intern.intern_delivery_exams_follow_up_ob_form
import modules.forms_intern.intern_internship_request_form
import modules.forms_intern.intern_skills_checklist_form

# --- STUDENT ---
import modules.forms_student.student_clinical_observations_ob_form
import modules.forms_student.student_ob_dashboard_form
import modules.forms_student.student_supervision_ob_form
import modules.forms_student.student_competency_evaluations_ob_form
import modules.forms_student.student_course_feedback_form
import modules.forms_student.student_case_study_form
import modules.forms_student.student_stage_request_form

# --- GUEST ---
import modules.forms_guest.guest_public_education_ressources_form
import modules.forms_guest.guest_utility_service_request_form
import modules.forms_guest.guest_workshop_registration_portal_form

# 🌿 Filtrage des formulaires publics (utilisé pour la navigation publique si nécessaire)
public_forms = {
    name: entry
    for name, entry in form_registry.items()
    if entry.get("role") == "PUBLIC"
}


# =========================================================================
# 2. CONFIGURATION ET DONNÉES STATIQUES
# =========================================================================

# 🌤️ Icônes météo
WEATHER_ICONS = {
    0: "☀️",
    1: "🌤️",
    2: "⛅",
    3: "☁️",
    45: "🌫️",
    48: "🌫️",
    51: "🌦️",
    61: "🌧️",
    71: "❄️",
    80: "🌧️",
    95: "⛈️",
}

# 📚 Fiches culturelles (carrousel)
# Les chemins d'accès aux images sont conservés tels quels (doivent exister localement)
script_dir = os.path.dirname(os.path.abspath(__file__))
fiches = {
    "Transmission des savoirs": {
        "titre": "Transmission des savoirs",
        "image": os.path.join(script_dir, "static", "Grand_mere_et_enfant.png"),
        "description": "👵 Les aînées partagent leur sagesse à travers les récits et les gestes.",
        "citation": "« Ce que tu apprends avec ton cœur, tu ne l’oublies jamais. »",
    },
    "Accueil sur le territoire": {
        "titre": "Accueil sur le territoire",
        "image": os.path.join(script_dir, "static", "Accueil_territoire.png"),
        "description": "🌿 Le lien sacré avec la terre, les ancêtres et les esprits protecteurs.",
        "citation": "« Chaque pas sur cette terre est une prière. »",
    },
    "Maternité et continuité": {
        "titre": "Maternité et continuité",
        "image": os.path.join(script_dir, "static", "Mere_crie.png"),
        "description": "👩‍👧 La force des mères cries, gardiennes de la vie et de l’avenir.",
        "citation": "« Porter un enfant, c’est porter l’histoire de notre peuple. »",
    },
    "Le retour attendu": {
        "titre": "Le souffle de l'avenir",
        "image": os.path.join(script_dir, "static", "Le_retour_attendu.png"),
        "description": "Deux jeunes mères partageant un moment de quiétude avec leurs nouveau-nés.",
        "citation": "« La vie que nous tenons dans nos bras est l'héritage de nos ancêtres et le futur de notre peuple. »",
    },
    "La transmission du savoir ancestral": {
        "titre": "La transmission du savoir ancestral",
        "image": os.path.join(script_dir, "static", "Tissage_et_transmission.png"),
        "description": "Gestes et traditions qui relient la maternité à l'esprit de la terre.",
        "citation": "« Dans chaque pli de la peau d'une aînée se cachent les histoires qui protégeront le nouveau-né. »",
    },
    "Le berceau de la nature": {
        "titre": "Le berceau de la nature",
        "image": os.path.join(script_dir, "static", "Berceau_nature.png"),
        "description": "Dès leurs premiers instants, la nature est intégrée dans le soin des tout-petits.",
        "citation": "« Comme une graine dans la terre, notre bébé trouvera sa force dans le territoire. »",
    },
}


# =========================================================================
# 3. FONCTIONS UTILITAIRES
# =========================================================================


def image_to_base64(image_path):
    """Convertit une image en chaîne base64."""
    # Cette fonction est conservée pour le carrousel culturel
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = os.path.splitext(image_path)[1][1:]
            return f"data:image/{ext};base64,{encoded}"
    else:
        # En production, cela pourrait être un placeholder générique ou un log
        st.error(f"Image introuvable: {image_path}")
        return None


def generate_carousel_html(fiches):
    """Génère le HTML du carrousel culturel."""
    slides = ""
    for fiche in fiches.values():
        img_data = image_to_base64(fiche["image"])
        if img_data:
            slides += f"""
            <div class="swiper-slide">
                <h3>{fiche['titre']}</h3>
                <img src="{img_data}" style="width:45%; height:260px; object-fit:cover; border-radius:10px; margin:auto; display:block;" />
                <p>{fiche['description']}</p>
                <blockquote><em>{fiche['citation']}</em></blockquote>
            </div>
            """
        else:
            slides += f"""
            <div class="swiper-slide">
                <h3>{fiche['titre']}</h3>
                <p>⚠️ Image introuvable</p>
                <p>{fiche['description']}</p>
                <blockquote><em>{fiche['citation']}</em></blockquote>
            </div>
            """

    html_code = f"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.css" />
    <style>
        .swiper {{
            width: 100%;
            height: 600px;
            direction: rtl;
        }}
        .swiper-slide {{
            text-align: center;
            font-size: 18px;
            background: #fff;
            padding: 20px;
        }}
        img {{
            max-height: 600px;
            object-fit: cover;
        }}
    </style>
    <div class="swiper">
        <div class="swiper-wrapper">
            {slides}
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.js"></script>
    <script>
        const swiper = new Swiper('.swiper', {{
            loop: true,
            autoplay: {{
                delay: 6000,
                disableOnInteraction: false,
            }},
            slidesPerView: 1,
            spaceBetween: 30,
            speed: 1000,
            reverseDirection: true,
        }});
    </script>
    """
    return html_code


@st.cache_data
def get_current_weather(lat, lon):
    """Récupère et met en cache les données météo actuelles d'Open-Meteo."""
    # Fonction conservée et utilisée dans la section Accueil
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,wind_speed_10m&timezone=auto"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["current"]
        return {
            "temp": data["temperature_2m"],
            "weather_code": data["weather_code"],
            "wind": data["wind_speed_10m"],
        }
    except requests.exceptions.RequestException:
        return None


def normalize_session(last_sess):
    """Normalise la session en dict avec clés 'start' et 'end'."""
    # Fonction conservée pour les détails de session
    if isinstance(last_sess, dict):
        return {
            "start": last_sess.get("start"),
            "end": last_sess.get("end"),
            "role": last_sess.get("role", "inconnu"),
        }
    elif isinstance(last_sess, datetime.datetime):
        # Conversion du datetime.datetime en timestamp pour la compatibilité avec time.localtime
        return {
            "start": last_sess.timestamp(),
            "end": None,
            "role": "inconnu",
        }
    else:
        return {
            "start": None,
            "end": None,
            "role": "inconnu",
        }


def is_valid_module(path):
    """Vérifie si le module existe avant de le charger."""
    # Fonction conservée pour la validation des modules
    try:
        importlib.import_module(path.replace("/", "."))
        return True
    except ModuleNotFoundError:
        return False


def load_form(path):
    """Charge dynamiquement un formulaire selon son chemin."""
    # Fonction conservée pour charger les formulaires
    try:
        module_path = path.replace("/", ".")
        module = importlib.import_module(module_path)
        # Assurez-vous que le module a la fonction render_form
        if hasattr(module, "render_form"):
            module.render_form()
        else:
            st.error(
                f"Module trouvé, mais la fonction 'render_form' est manquante dans: {path}"
            )
    except ModuleNotFoundError:
        st.error(f"Formulaire introuvable : {path}")


# =========================================================================
# 4. FONCTIONS DE RENDU (ROUTING)
# =========================================================================


def render_dashboard():
    """Routeur de Dashboards en fonction du rôle."""
    role = st.session_state.get("user_role", "GUEST")
    st.title(f"📊 Tableau de bord : {role.capitalize()}")

    # Utilisation des fonctions importées au début du script
    if role == "GUEST":
        form_dashboard_guest()
    elif role == "ADMIN":
        form_dashboard_admin()
    elif role == "MIDWIFE":
        form_dashboard_midwife()
    elif role == "DOCTOR":
        form_dashboard_doctor()
    elif role == "NURSE":
        form_dashboard_nurse()
    elif role == "PATIENT":
        form_dashboard_patient()
    elif role == "STUDENT":
        form_dashboard_student()
    elif role == "INTERN":
        form_dashboard_intern()
    elif role == "DOCTORAL":
        form_dashboard_doctoral()
    else:
        st.warning(
            "⚠️ Aucun tableau de bord trouvé pour ce rôle. Affichage du tableau de bord GUEST."
        )
        form_dashboard_guest()


def render_formulaires_specifiques():
    """Affiche les boutons des formulaires spécifiques à chaque rôle."""
    role = st.session_state.get("user_role", "GUEST")
    st.title("📂 Formulaires spécifiques")
    st.markdown(f"**Rôle actuel :** `{role}`")

    forms_to_display = []
    # Filtrer les formulaires pour le rôle actuel
    for key, config in get_all_forms().items():
        if config["role"] == role or role in config.get("roles_allowed", []):
            forms_to_display.append((key, config))

    if not forms_to_display:
        st.info("Aucun formulaire spécifique n'est disponible pour votre rôle.")
        return

    # Affichage des formulaires par colonne pour un meilleur agencement
    cols = st.columns(3)
    for i, (key, config) in enumerate(forms_to_display):
        col = cols[i % 3]
        with col:
            label = config.get("title", key)
            # Bouton stylisé avec une clé unique
            if st.button(f"📄 {label}", key=f"form_spec_{key}"):
                load_form(config["module"])


def render_formulaires_partages():
    """Affiche les boutons des fonctions partagées."""
    st.title("🌐 Fonctions partagées")

    shared_forms = get_shared_forms()

    # Liste ordonnée des clés pour l'affichage
    shared_keys = [
        "Agenda",
        "Calendrier",
        "Inbox",
        "Profile",
        "Settings",
        "Signup",
        "Stats",
    ]

    # Affichage des formulaires par colonne
    cols = st.columns(3)
    for i, key in enumerate(shared_keys):
        if key in shared_forms:
            config = shared_forms[key]
            col = cols[i % 3]
            with col:
                label = config.get("title", key)
                if st.button(f"🔗 {label}", key=f"shared_form_{key}"):
                    # Assurez-vous que le module est un chemin (string) pour load_form
                    module_path = config.get("module_path") or config.get("module")
                    if isinstance(module_path, str):
                        load_form(module_path)
                    else:
                        st.error(f"Chemin de module invalide pour {label}.")


def render_workshops():
    """Affiche le carrousel des soins et les ateliers."""
    st.title("🧵 Ateliers & Carrousels")
    st.markdown("Explorez les ressources d'ateliers et de soins culturels.")

    # Affichage de l'outil Bébé Pleure (maintenant dans une fonction de rendu)
    st.markdown("### 👶 Carrousel d'aide aux soins")
    render_carrousel_soins_form()

    # Affichage de l'outil Bébé Pleure (maintenant dans une fonction de rendu)
    st.markdown("### 🎧 Outil sonore : Le bébé pleure")
    render_bebe_pleure()


def handle_login_form(message_placeholder):
    """
    Affiche et gère le formulaire de connexion.
    Utilise une DIV stylisée pour encadrer les champs.
    """
    # CSS pour styliser le bloc de connexion
    st.markdown(
        """
        <style>
        .login-box {
            padding: 20px;
            border-radius: 15px;
            border: 3px solid #FFD1DC; /* Bordure rose douce */
            background-color: #FFF0F5; /* Fond rose très clair */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .login-box .stTextInput > div > div > input, .login-box .stButton > button {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("🏠 Bienvenue dans MSA !❤️")

        with st.form("msa_login_form", clear_on_submit=True):
            st.markdown(
                """
                <p style="font-size:1rem; color:#d63384; font-style:italic;">
                Veuillez utiliser votre rôle et votre mot de passe.
                </p>
                """,
                unsafe_allow_html=True,
            )

            username = st.text_input(
                "Identifiant (rôle)",
                placeholder="Ex: MIDWIFE, DOCTOR, ADMIN...",
            )
            password = st.text_input(
                "Mot de passe (pour démo: '1234')",
                type="password",
                placeholder="Entrez votre mot de passe",
            )
            submitted = st.form_submit_button("Se connecter 🔒")

            if submitted:
                # Logique de validation simple basée sur les rôles existants dans le script
                valid_roles = [
                    "ADMIN",
                    "MIDWIFE",
                    "DOCTOR",
                    "NURSE",
                    "PATIENT",
                    "DOCTORAL",
                    "INTERN",
                    "STUDENT",
                    "GUEST",
                ]

                # Validation pour la démo
                if username.upper() in valid_roles and password == "1234":
                    st.session_state["logged_in"] = True
                    st.session_state["user_role"] = username.upper()
                    st.session_state["login_time"] = time.time()
                    st.session_state["main_section_auth"] = (
                        "Tableau de bord"  # Redirection après connexion
                    )
                    message_placeholder.success(
                        "✅ Connexion réussie! Bienvenue " + username.upper()
                    )
                    st.rerun()
                elif username.upper() in valid_roles and password != "1234":
                    message_placeholder.error(
                        "❌ Mot de passe incorrect. Essayez '1234'."
                    )
                else:
                    message_placeholder.error("❌ Rôle invalide ou non reconnu.")

        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================================
# 5. LOGIQUE PRINCIPALE DE L'APPLICATION
# =========================================================================

# --- Configuration de la page ---
st.set_page_config(
    page_title="MSA Fusion Application", layout="wide", initial_sidebar_state="expanded"
)

# --- Initialisation de session sécurisée ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "GUEST"
if "main_section_auth" not in st.session_state:
    st.session_state["main_section_auth"] = "Accueil"
if "login_time" not in st.session_state:
    st.session_state["login_time"] = None  # Pas connecté au début

# --- Vérification de la connexion ---
if not st.session_state["logged_in"]:
    # Affiche l'image et le formulaire de connexion
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(
            "https://placehold.co/600x400/AEDFF7/333?text=Bienvenue+MSA",
            use_column_width="auto",
        )
    with col2:
        # Placeholder pour les messages de succès/erreur de login
        login_message_placeholder = st.empty()
        handle_login_form(login_message_placeholder)

    st.stop()  # Arrête le reste du script si l'utilisateur n'est pas connecté

# --- Logique de la barre latérale (après connexion) ---
with st.sidebar:
    st.markdown("## 🌿 Navigation")
    st.markdown("#### Détails de Session")

    st.markdown(
        f"**Rôle :** {st.session_state.get('user_role', 'INVITÉ').capitalize()}"
    )

    login_timestamp = st.session_state.get("login_time")
    if login_timestamp:
        login_dt = time.localtime(login_timestamp)
        st.markdown(
            f"**Connexion :** {time.strftime('%Y-%m-%d', login_dt)} à {time.strftime('%H:%M:%S', login_dt)}"
        )

    # Affichage de la dernière session si elle existe
    last_sess = normalize_session(st.session_state.get("last_session", {}))
    if last_sess["start"] and last_sess["end"]:
        # Les valeurs start et end sont des timestamps ici
        start_dt = time.localtime(last_sess["start"])
        end_dt = time.localtime(last_sess["end"])
        st.markdown("---")
        st.markdown(f"**Dernière Session ({last_sess['role'].capitalize()})**:")
        st.markdown(f"Déb. : {time.strftime('%Y-%m-%d %H:%M:%S', start_dt)}")
        st.markdown(f"Fin : {time.strftime('%Y-%m-%d %H:%M:%S', end_dt)}")

    st.markdown("---")

    # Navigation dans la barre latérale
    nav_options = [
        "Accueil",
        "Tableau de bord",
        "Formulaires spécifiques",
        "Fonction partagée",
        "Workshops",
    ]
    st.session_state["main_section_auth"] = st.radio(
        "🧭 Que souhaitez-vous afficher ?",
        nav_options,
        index=nav_options.index(st.session_state.get("main_section_auth", "Accueil")),
        key="sidebar_navigation",
    )

    st.markdown("---")

    # Bouton de déconnexion dans la sidebar
    if st.button("🚪 Déconnexion", key="logout_button"):
        st.session_state["last_session"] = {
            "role": st.session_state.get("user_role", "INVITÉ"),
            "start": st.session_state.get("login_time"),
            "end": time.time(),
        }
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = "GUEST"
        st.session_state["login_time"] = None
        st.session_state["main_section_auth"] = "Accueil"
        st.toast("🌿 Vous avez quitté votre espace avec succès !", icon="🕊️")
        st.rerun()

# --- Corps principal selon la section choisie ---
section = st.session_state["main_section_auth"]
role = st.session_state.get("user_role", "GUEST")

# 🏠 ACCUEIL
if section == "Accueil":
    st.title("🌸 Bienvenue dans MSA !")
    st.markdown("Un lieu de soin, de culture et de célébration partagée.")

    # 🎠 Carrousel culturel
    st.markdown("### 🎠 Fiches culturelles")
    carousel_html = generate_carousel_html(fiches)
    st.components.v1.html(carousel_html, height=650, scrolling=False)

    # 🌤️ Carte météo interactive
    st.markdown("### ☀️ Météo des communautés")
    communities = {
        "Mistissini": {"lat": 50.4184, "lon": -73.8755, "color": "blue"},
        "Waskaganish": {"lat": 51.4879, "lon": -78.7484, "color": "green"},
        "Chisasibi": {"lat": 53.8051, "lon": -78.9169, "color": "purple"},
    }
    m = folium.Map(location=[51.5, -76.5], zoom_start=5)
    for name, info in communities.items():
        weather = get_current_weather(info["lat"], info["lon"])
        if weather:
            icon = WEATHER_ICONS.get(weather["weather_code"], "❓")
            popup = (
                f"{name}<br>{icon} {weather['temp']}°C<br>Vent: {weather['wind']} km/h"
            )
            folium.Marker(
                location=[info["lat"], info["lon"]],
                popup=popup,
                icon=folium.Icon(color=info["color"], icon="cloud"),
            ).add_to(m)
        else:
            folium.Marker(
                location=[info["lat"], info["lon"]],
                popup=f"{name}<br>Données météo indisponibles.",
                icon=folium.Icon(color="gray", icon="question"),
            ).add_to(m)

    st_folium(m, width=700, height=450)


# 📊 TABLEAU DE BORD
elif section == "Tableau de bord":
    render_dashboard()

# 📂 FORMULAIRES SPÉCIFIQUES
elif section == "Formulaires spécifiques":
    render_formulaires_specifiques()

# 🌐 FONCTIONS PARTAGÉES
elif section == "Fonction partagée":
    render_formulaires_partages()

# 🧵 WORKSHOPS
elif section == "Workshops":
    render_workshops()

# --- Section pour les transitions CSS (conservée) ---
st.markdown(
    """
<style>
button {
    transition: all 0.3s ease-in-out;
}
button:hover {
    background-color: #A7D8DE !important;
    color: white !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# 🧘 Sécurité de session (Nettoyage à la déconnexion déjà fait dans le bouton)
# Nettoyage final du module de vérification (uniquement un exemple)
# La fonction is_valid_module est utilisée pour la robustesse.
# Exemple d'utilisation finale de is_valid_module (seulement comme trace, la logique n'est pas intégrée au flux principal ici)
# config = {"module": "form_utility_general_contact"}
# if is_valid_module(config["module"]):
#     pass
