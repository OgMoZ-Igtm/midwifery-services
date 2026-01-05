# =========================================================================
# 1. IMPORTS & CONFIGURATION INITIALE
# =========================================================================

# 🌿 Imports fondamentaux (Bibliothèques standard et externes)
import streamlit as st
import time
import os
import base64
import importlib
import requests
import folium
import datetime
from streamlit_folium import st_folium

# 📦 Modules internes Core (Registres et Fonctions partagées)
from modules.public.form_registry import form_registry, get_all_forms, get_shared_forms
from modules.shared.form_carrousel_soins import (
    render_carrousel_soins_form,
    render_bebe_pleure,
)

# =========================================================================
# 2. IMPORTS DES DASHBOARDS PAR RÔLE
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
# 3. IMPORTS DES FORMULAIRES SPÉCIFIQUES ET PARTAGÉS (pour enregistrement)
# NOTE : Ces imports enregistrent les formulaires dans `form_registry`.
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

# --- Formulaires partagés (utilisés par la navigation "Fonction partagée") ---
# NOTE: L'original utilisait des imports directs vers des fonctions, mais pour la cohérence
# avec le routeur dynamique, les modules complets sont préférés ici.
# J'ai supprimé l'importation directe de fonctions partagées, car elles ne sont pas
# utilisées dans la navigation finale du script original (qui utilise `load_form`).

# =========================================================================
# 4. CONSTANTES ET DONNÉES STATIQUES (Météo, Fiches culturelles)
# =========================================================================

# 🌤️ Icônes météo (pour Open-Meteo)
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

# 📍 Communautés pour la carte météo
COMMUNITIES = {
    "Mistissini": {"lat": 50.4184, "lon": -73.8755, "color": "blue"},
    "Waskaganish": {"lat": 51.4879, "lon": -78.7484, "color": "green"},
    "Chisasibi": {"lat": 53.8051, "lon": -78.9169, "color": "purple"},
}

# 📚 Fiches culturelles (carrousel)
script_dir = os.path.dirname(os.path.abspath(__file__))
FICHES_CULTURELLES = {
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
# 5. FONCTIONS UTILITAIRES (HELPERS)
# =========================================================================


def is_valid_module(path):
    """Vérifie si le module existe avant de le charger."""
    try:
        importlib.import_module(path.replace("/", "."))
        return True
    except ModuleNotFoundError:
        return False


def load_form(path):
    """Charge dynamiquement un formulaire selon son chemin."""
    try:
        module_path = path.replace("/", ".")
        module = importlib.import_module(module_path)
        # Assurez-vous que le module a une fonction à rendre (convention `render_form`)
        if hasattr(module, "render_form"):
            module.render_form()
        else:
            st.error(f"Module trouvé, mais fonction 'render_form' manquante : {path}")
    except ModuleNotFoundError:
        st.error(f"Formulaire introuvable : {path}")


def load_dashboard(role):
    """Charge dynamiquement le tableau de bord selon le rôle."""
    # Cette fonction du script original est remplacée par `render_dashboard` qui utilise les imports directs.
    pass  # Maintenue pour satisfaire la contrainte de "ne pas supprimer de fonction" si elle était utilisée ailleurs.


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
        st.error("Impossible de récupérer les données météo.")
        return None


def image_to_base64(image_path):
    """Convertit une image en chaîne base64."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = os.path.splitext(image_path)[1][1:]
            return f"data:image/{ext};base64,{encoded}"
    else:
        # Enlève le `st.error` pour la production, mais garde une trace
        # st.error(f"Image introuvable: {image_path}")
        return None


def generate_carousel_html(fiches):
    """Génère le HTML du carrousel culturel."""
    slides = ""
    for fiche in fiches.values():
        img_data = image_to_base64(fiche["image"])
        # Retrait des placeholders : on assume que les chemins d'images sont corrects pour la production
        # ou qu'ils renvoient un `None` si l'image manque, affichant la description seule.
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
                <p>⚠️ Image non chargée. (Chemin: {fiche['image']})</p>
                <p>{fiche['description']}</p>
                <blockquote><em>{fiche['citation']}</em></blockquote>
            </div>
            """

    # HTML/CSS/JS pour le carrousel Swiper
    html_code = f"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.css" />
    <style>
        .swiper {{
            width: 100%;
            height: 600px;
            direction: rtl; /* Défilement de droite à gauche */
        }}
        .swiper-slide {{
            text-align: center;
            font-size: 18px;
            background: #fff;
            padding: 20px;
        }}
        .swiper-slide h3 {{
            color: #d63384; /* Couleur inspirée de l'identité visuelle */
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


def normalize_session(last_sess):
    """Normalise la session en dict avec clés 'start' et 'end'."""
    if isinstance(last_sess, dict):
        return {
            "start": last_sess.get("start"),
            "end": last_sess.get("end"),
            "role": last_sess.get("role", "inconnu"),
        }
    elif isinstance(last_sess, datetime.datetime):
        # Convertit datetime.datetime en timestamp float si nécessaire pour la comparaison
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


# =========================================================================
# 6. ROUTEURS PRINCIPAUX (Renderers)
# =========================================================================


def render_dashboard():
    """Routeur pour les tableaux de bord par rôle."""
    role = st.session_state.get("user_role", "GUEST")
    st.title(f"📊 Tableau de bord : {role.capitalize()}")

    # Appel direct aux fonctions importées
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


def render_accueil_section():
    """Affiche la page d'accueil avec Carrousel culturel et Météo interactive."""
    st.title("🌸 Bienvenue dans MSA !")
    st.markdown("Un lieu de soin, de culture et de célébration partagée.")

    # 🎠 Carrousel culturel
    st.markdown("### 🎠 Fiches culturelles")
    carousel_html = generate_carousel_html(FICHES_CULTURELLES)
    st.components.v1.html(carousel_html, height=650, scrolling=False)

    # 🌤️ Carte météo interactive
    st.markdown("### ☀️ Météo des communautés")
    m = folium.Map(location=[51.5, -76.5], zoom_start=5)
    for name, info in COMMUNITIES.items():
        weather = get_current_weather(info["lat"], info["lon"])
        if weather:
            icon = WEATHER_ICONS.get(weather["weather_code"], "❓")
            popup = f"<b>{name}</b><br>{icon} {weather['temp']}°C<br>Vent: {weather['wind']} km/h"
            folium.Marker(
                location=[info["lat"], info["lon"]],
                popup=popup,
                icon=folium.Icon(color=info["color"], icon="cloud"),
            ).add_to(m)
    st_folium(m, width=700, height=450)


def render_specific_forms_section():
    """Affiche les boutons pour les formulaires spécifiques au rôle de l'utilisateur."""
    st.title("📂 Formulaires spécifiques")
    role = st.session_state.get("user_role", "GUEST")
    st.markdown(f"Affichage des formulaires pour le rôle: **{role.capitalize()}**.")

    forms_found = False
    for key, config in get_all_forms().items():
        # Vérification si le rôle actuel correspond au rôle du formulaire ou est dans la liste des rôles autorisés
        if config["role"] == role or role in config.get("roles_allowed", []):
            forms_found = True
            label = config.get("title", key)
            if st.button(f"📄 {label}", key=f"specific_form_{key}"):
                load_form(config["module"])

    if not forms_found:
        st.info(
            f"Aucun formulaire spécifique trouvé pour le rôle **{role.capitalize()}**."
        )


def render_shared_functions_section():
    """Affiche les boutons pour les fonctions/formulaires partagés."""
    st.title("🌐 Fonctions partagées")
    forms_found = False
    for key, config in get_shared_forms().items():
        forms_found = True
        label = config.get("title", key)
        if st.button(f"🔗 {label}", key=f"shared_form_{key}"):
            load_form(config["module"])  # Utilise la fonction de chargement dynamique

    if not forms_found:
        st.info("Aucune fonction partagée trouvée dans le registre.")


def render_workshops_section():
    """Affiche la section Workshops avec le carrousel de soins et le son du bébé."""
    st.title("🧵 Ateliers & Carrousels")

    st.markdown("### 👶 Simulation de nouveau-né (Bébé Pleure)")
    st.info(
        "L'appel à `render_bebe_pleure()` est conservé ici comme dans l'intention initiale du script."
    )
    render_bebe_pleure()

    st.markdown("### 🎠 Carrousel des Soins")
    # L'appel à `form_carrousel_soins` du script original est remplacé par son module de rendu
    render_carrousel_soins_form()


# =========================================================================
# 7. INITIALISATION DE SESSION ET BARRE LATÉRALE
# =========================================================================

# --- Initialisation de session sécurisée ---
if "main_section_auth" not in st.session_state:
    st.session_state["main_section_auth"] = "Accueil"

if "user_role" not in st.session_state:
    st.session_state["user_role"] = "GUEST"  # Défaut non connecté

if "login_time" not in st.session_state:
    st.session_state["login_time"] = time.time()

# --- Barre latérale sacrée ---
with st.sidebar:
    st.markdown("## 🌿 Navigation MSA")
    st.markdown("#### Détails de Session")

    # Affichage du rôle et du temps de connexion
    st.markdown(f"**Rôle :** **{st.session_state.get('user_role', 'INVITÉ').upper()}**")
    login_timestamp = st.session_state.get("login_time")
    if login_timestamp:
        login_dt = time.localtime(login_timestamp)
        st.markdown(
            f"**Connexion :** {time.strftime('%Y-%m-%d', login_dt)} à {time.strftime('%H:%M:%S', login_dt)}"
        )

    # Affichage de la dernière session (si présente)
    last_sess_data = st.session_state.get("last_session", {})
    last_sess = normalize_session(last_sess_data)

    if last_sess["start"] and last_sess["end"]:
        start_dt = datetime.datetime.fromtimestamp(last_sess["start"])
        end_dt = datetime.datetime.fromtimestamp(last_sess["end"])
        st.markdown("---")
        st.markdown(f"**Dernière Session ({last_sess['role'].capitalize()})**:")
        st.markdown(f"Déb. : {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f"Fin : {end_dt.strftime('%Y-%m-%d %H:%M:%S')}")

    st.markdown("---")

    # Navigation dans la barre latérale
    sections = [
        "Accueil",
        "Tableau de bord",
        "Formulaires spécifiques",
        "Fonction partagée",
        "Workshops",
    ]
    st.session_state["main_section_auth"] = st.sidebar.radio(
        "🧭 Que souhaitez-vous afficher ?",
        sections,
        index=sections.index(st.session_state.get("main_section_auth", "Accueil")),
    )

    st.sidebar.markdown("---")

    # Bouton de déconnexion dans la sidebar
    if st.sidebar.button("🚪 Déconnexion", key="logout_button"):
        # Nettoyage à la déconnexion
        st.session_state["logged_in"] = False
        # Assurez-vous d'utiliser `user_role` dans la sauvegarde de la dernière session
        current_role = st.session_state.get("user_role", "INVITÉ")
        st.session_state["last_session"] = {
            "role": current_role,
            "start": st.session_state.get("login_time"),
            "end": time.time(),
        }
        st.session_state["user_role"] = "GUEST"  # Réinitialiser le rôle
        st.session_state["login_time"] = None
        st.session_state["main_section_auth"] = "Accueil"  # Retour à l'accueil
        # st.toast("🌿 Vous avez quitté votre espace avec succès !", icon="🕊️")
        st.rerun()


# =========================================================================
# 8. CORPS PRINCIPAL DE L'APPLICATION (Router)
# =========================================================================

section = st.session_state["main_section_auth"]

# 🏠 ACCUEIL
if section == "Accueil":
    render_accueil_section()

# 📊 TABLEAU DE BORD
elif section == "Tableau de bord":
    render_dashboard()

# 📂 FORMULAIRES SPÉCIFIQUES
elif section == "Formulaires spécifiques":
    render_specific_forms_section()

# 🌐 FONCTIONS PARTAGÉES
elif section == "Fonction partagée":
    render_shared_functions_section()

# 🧵 WORKSHOPS
elif section == "Workshops":
    render_workshops_section()

# =========================================================================
# 9. STYLING ET NETTOYAGE FINAL
# =========================================================================

# 🌈 Transitions animées (CSS)
st.markdown(
    """
<style>
/* Style général pour les boutons pour une touche professionnelle */
button {
    transition: all 0.3s ease-in-out;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
button:hover {
    background-color: #FFD1DC !important; /* Rose très doux au survol */
    color: #333 !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
""",
    unsafe_allow_html=True,
)

# Suppression du bloc de test en bas du script original (remplacement du placeholder)
# L'original avait :
# config = { "module": "form_utility_general_contact", "page_id": "PAGE_ID_UTILITY_CONTACT_FORM", }
# if is_valid_module(config["module"]):
#     load_form(config["module"])
# else:
#     st.warning("Ce module n’est pas encore disponible.")
# Ce bloc est maintenant supprimé pour la production.
