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

# 📦 Modules internes
from modules.public.form_registry import form_registry
from modules.shared.form_carrousel_soins import render_carrousel_soins_form
from modules.public.forms_registry import PUBLIC_FORMS_REGISTRY
from modules.public.form_registry import get_all_forms
from modules.public.form_registry import get_shared_forms
from modules.shared.form_carrousel_soins import render_bebe_pleure

# Dans la section Workshops ou Accueil
render_bebe_pleure()


# from modules.forms_admin.admin_dashboard import form_dashboard_admin
# from modules.forms.forms_guest.dashboard_guest import form_dashboard_guest
# Dashboards par rôle
# =========================================================================
# 📦 IMPORTS DES FORMULAIRES PAR RÔLE
# =========================================================================

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


# Formulaires partagés
from modules.shared.form_shared_agenda import form_shared_agenda
from modules.shared.form_shared_calendar import form_shared_calendar
from modules.shared.form_shared_profile import form_shared_profile
from modules.shared.form_shared_settings import form_shared_settings
from modules.shared.form_shared_signup import form_shared_signup
from modules.shared.form_shared_stats import form_shared_stats
from modules.shared.form_shared_inbox import form_shared_inbox

# 🌿 Filtrage des formulaires publics
public_forms = {
    name: entry for name, entry in form_registry.items() if entry["role"] == "PUBLIC"
}


def render_accueil():
    st.title("🏠 Accueil")
    st.markdown("Bienvenue dans l'application Midwifery Services.")


# =========================================================================
# 📦 IMPORTS DES DASHBOARDS PAR RÔLE
# =========================================================================
from modules.dashboard.dashboard_guest import form_dashboard_guest
from modules.dashboard.dashboard_admin import form_dashboard_admin
from modules.dashboard.dashboard_midwife import form_dashboard_midwife
from modules.dashboard.dashboard_doctor import form_dashboard_doctor
from modules.dashboard.dashboard_nurse import form_dashboard_nurse
from modules.dashboard.dashboard_patient import form_dashboard_patient
from modules.dashboard.dashboard_student import form_dashboard_student
from modules.dashboard.dashboard_intern import form_dashboard_intern
from modules.dashboard.dashboard_doctoral import form_dashboard_doctoral


# =========================================================================
# 🚀 ROUTEUR DE DASHBOARDS
# =========================================================================
def render_dashboard():
    role = st.session_state.get("role", "GUEST")
    st.title(f"📊 Tableau de bord : {role}")

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
        st.warning("⚠️ Aucun tableau de bord trouvé pour ce rôle.")


def render_formulaires_specifiques():
    st.title("🧾 Formulaires spécifiques")
    st.markdown("Formulaires liés aux rôles...")


def render_formulaires_partages():
    st.title("🤝 Formulaires partagés")
    sub_choice = st.radio(
        "Choisir un formulaire",
        [
            "Agenda",
            "Calendrier",
            "Messages",
            "Profile",
            "Settings",
            "Signup",
            "Stats",
            "Inbox",
        ],
        key="shared_forms_navigation",
    )
    if sub_choice == "Agenda":
        form_shared_agenda()
    elif sub_choice == "Calendrier":
        form_shared_calendar()
    # elif sub_choice == "Messages":
    #     form_shared_messages()
    elif sub_choice == "Profile":
        form_shared_profile()
    elif sub_choice == "Settings":
        form_shared_settings()
    elif sub_choice == "Signup":
        form_shared_signup()
    elif sub_choice == "Stats":
        form_shared_stats()
    elif sub_choice == "Inbox":
        form_shared_inbox()


def render_workshops():
    st.title("🎠 Workshops")
    form_carrousel_soins()


# 🧩 SECTION 1 : Imports et initialisation :
# Ces fonctions invoquent les modules selon leur chemin.

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

# 🧩 SECTION 2 : Fonctions utilitaires
# 🔮 1. Chargement dynamique des tableaux de bord et formulaires


def load_dashboard(role):
    """Charge dynamiquement le tableau de bord selon le rôle."""
    try:
        module = importlib.import_module(f"modules.dashboard.dashboard_{role.lower()}")
        module.render_dashboard()
    except ModuleNotFoundError:
        st.warning(f"Aucun tableau de bord trouvé pour le rôle {role}")


def load_form(path):
    """Charge dynamiquement un formulaire selon son chemin."""
    try:
        module_path = path.replace("/", ".")
        module = importlib.import_module(module_path)
        module.render_form()
    except ModuleNotFoundError:
        st.error(f"Formulaire introuvable : {path}")


# Section II : 🌤️ 2. Météo en direct via Open-Meteo


# 🌤️ 2. Météo en direct via Open-Meteo :
# Cette fonction interroge les cieux pour Mistissini, Waskaganish et Chisasibi :


@st.cache_data
def get_current_weather(lat, lon):
    """Récupère et met en cache les données météo actuelles d'Open-Meteo."""
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


# 🎠 3. Carrousel culturel dynamique :
# Cette fonction génère le HTML du carrousel, avec une image toutes les 6 secondes, défilant de droite à gauche :


def image_to_base64(image_path):
    """Convertit une image en chaîne base64."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = os.path.splitext(image_path)[1][1:]
            return f"data:image/{ext};base64,{encoded}"
    else:
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


# 🧩 SECTION 3 : Barre latérale sacrée et navigation:
# Elle permet à l’utilisateur de choisir son chemin — Accueil, Tableau de bord, Formulaires, ou Ateliers — tout en affichant les détails de session avec soin.

# --- Initialisation de session ---
if "main_section_auth" not in st.session_state:
    st.session_state["main_section_auth"] = "Accueil"

# --- Barre latérale sacrée ---
with st.sidebar:
    st.markdown("## 🌿 Navigation")
    st.markdown("#### Détails de Session")

    login_timestamp = st.session_state.get("login_time")
    if login_timestamp:
        login_dt = time.localtime(login_timestamp)
        st.markdown(
            f"**Connexion :** {time.strftime('%Y-%m-%d', login_dt)} à {time.strftime('%H:%M:%S', login_dt)}"
        )

# ==============================================================================
# 🧪 Fonction utilitaire
# ==============================================================================


def normalize_session(last_sess):
    """
    Normalise la session en dict avec clés 'start' et 'end'.
    """
    if isinstance(last_sess, dict):
        return {
            "start": last_sess.get("start"),
            "end": last_sess.get("end"),
            "role": last_sess.get("role", "inconnu"),
        }
    elif isinstance(last_sess, datetime.datetime):
        return {
            "start": last_sess,
            "end": None,
            "role": "inconnu",
        }
    else:
        return {
            "start": None,
            "end": None,
            "role": "inconnu",
        }


# ==============================================================================
# 🧪 Utilisation dans ton dashboard
# ==============================================================================
last_sess = normalize_session(st.session_state.get("last_session", {}))

if last_sess["start"] and last_sess["end"]:
    start_dt = time.localtime(last_sess["start"].timestamp())
    end_dt = time.localtime(last_sess["end"].timestamp())
    st.markdown("---")
    st.markdown(f"**Dernière Session ({last_sess['role'].capitalize()})**:")
    st.markdown(f"Déb. : {time.strftime('%Y-%m-%d %H:%M:%S', start_dt)}")
    st.markdown(f"Fin : {time.strftime('%Y-%m-%d %H:%M:%S', end_dt)}")

    st.markdown("---")


# Initialisation sécurisée
if "main_section_auth" not in st.session_state:
    st.session_state["main_section_auth"] = "Accueil"

# Navigation dans la barre latérale
st.session_state["main_section_auth"] = st.sidebar.radio(
    "🧭 Que souhaitez-vous afficher ?",
    [
        "Accueil",
        "Tableau de bord",
        "Formulaires spécifiques",
        "Fonction partagée",
        "Workshops",
    ],
    index=[
        "Accueil",
        "Tableau de bord",
        "Formulaires spécifiques",
        "Fonction partagée",
        "Workshops",
    ].index(st.session_state.get("main_section_auth", "Accueil")),
)

# Séparateur visuel
st.sidebar.markdown("---")

# Bouton de déconnexion dans la sidebar
if st.sidebar.button("🚪 Déconnexion"):
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None
    st.session_state["info_page"] = "Accueil"
    st.session_state["selected_form"] = None
    st.session_state["last_session"] = {
        "role": st.session_state.get("user_role", "INVITÉ"),
        "start": st.session_state.get("login_time"),
        "end": time.time(),
    }
    st.session_state["login_time"] = None
    st.rerun()


# 🧩 SECTION 4 : Corps principal — Accueil, Tableau de bord, Formulaires, Workshops :
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
    st_folium(m, width=700, height=450)


# 📊 TABLEAU DE BORD
elif section == "Tableau de bord":
    render_dashboard()

# 📂 FORMULAIRES SPÉCIFIQUES
elif section == "Formulaires spécifiques":
    st.title("📂 Formulaires spécifiques")
    for key, config in get_all_forms().items():
        if config["role"] == role or role in config.get("roles_allowed", []):
            label = config.get("title", key)
            if st.button(f"📄 {label}", key=key):
                load_form(config["module"])

# 🌐 FONCTIONS PARTAGÉES
elif section == "Fonction partagée":
    st.title("🌐 Fonctions partagées")
    for key, config in get_shared_forms().items():
        label = config.get("title", key)
        if st.button(f"🔗 {label}", key=key):
            load_form(config["module"])

# 🧵 WORKSHOPS
elif section == "Workshops":
    st.title("🧵 Ateliers & Carrousels")
    st.markdown("Voici le carrousel `render_generate_bebe-carrousel`")
    load_form("modules.shared.form_carrousel_soins")


# 🧩 SECTION 5 : Sécurité, validation et transitions animées :
# ✅ 1. Validation du rôle et des modules
# Vérification avant d’appeler un tableau de bord ou un formulaire :


def is_valid_module(path):
    """Vérifie si le module existe avant de le charger."""
    try:
        importlib.import_module(path.replace("/", "."))
        return True
    except ModuleNotFoundError:
        return False


# Utilisation dans load_dashboard ou load_form :

config = {
    "module": "form_utility_general_contact",  # ou le module que tu veux tester
    "page_id": "PAGE_ID_UTILITY_CONTACT_FORM",
}


if is_valid_module(config["module"]):
    load_form(config["module"])
else:
    st.warning("Ce module n’est pas encore disponible.")

# 🌈 2. Transitions animées (visuelles et émotionnelles)
# Ajout des animations CSS dans le carrousel, ou des effets visuels dans les boutons :

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

# 🧘 3. Sécurité de session
# Renforcement de la logique de session pour éviter les erreurs :

if "user_role" not in st.session_state:
    st.session_state["user_role"] = "GUEST"

if "login_time" not in st.session_state:
    st.session_state["login_time"] = time.time()

# 🧩 4. Nettoyage à la déconnexion
# Déjà présent dans ta barre latérale, mais on peut ajouter :

# st.toast("🌿 Vous avez quitté votre espace avec succès !", icon="🕊️")
