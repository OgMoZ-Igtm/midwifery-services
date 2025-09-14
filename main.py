import streamlit as st
import requests
import os
import json
import time
from PIL import Image
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import base64
from datetime import datetime
import importlib.util
from utils.security import get_packs_for_role, est_autorise, log_audit_event


st.set_page_config(page_title="Accueil", page_icon="🏠", layout="centered")
st.title("🏠 Portail de consultation")

st.markdown("Bienvenue sur la plateforme de gestion des consultations.")

col1, col2 = st.columns(2)
with col1:
    st.header("👩‍⚕️ Médecin")

    # 🔐 Lien vers l'espace admin (visible uniquement pour les admins)
    if st.session_state.get("role") == "ADMIN":
        st.page_link(
            "modules/interface_admin.py", label="🛠️ Espace administrateur", icon="🧑‍💼"
        )

    # 🔐 Lien vers l'espace médecin (visible uniquement pour les professionnels de santé)
    if st.session_state.get("role") in ["DOCTOR", "MIDWIFE", "NURSE"]:
        st.page_link(
            "modules/interface_medecin.py",
            label="Accéder à l'espace médecin",
            icon="🩺",
        )
    else:
        st.info("🔒 Espace réservé aux professionnels de santé.")

with col2:
    st.header("🧑‍🤝‍🧑 Patient")
    st.page_link(
        "modules/interface_patient.py", label="Soumettre une demande", icon="📝"
    )

# =========================================================
# 📁 PATHS AND RESOURCES
# =========================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(script_dir, "utils")
data_dir = os.path.join(script_dir, "data")
static_dir = os.path.join(script_dir, "static")

for directory in [data_dir, os.path.join(script_dir, "modules", "packs")]:
    if not os.path.exists(directory):
        os.makedirs(directory)

try:
    menu_mapping_path = os.path.join(utils_dir, "menu_mapping.json")
    with open(menu_mapping_path, "r", encoding="utf-8") as f:
        MENU_MAPPING = json.load(f)
        st.session_state["MENU_MAPPING"] = MENU_MAPPING
except FileNotFoundError:
    st.error(f"❌ The menu configuration file '{menu_mapping_path}' was not found.")
    st.stop()
except json.JSONDecodeError:
    st.error("❌ Format error in the menu_mapping.json file. Check the syntax.")
    st.stop()

# =========================================================
# 🔐 PERMANENT ACCESS CONTROL
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "role" not in st.session_state:
    st.session_state["role"] = "GUEST"
if "unread_messages" not in st.session_state:
    st.session_state["unread_messages"] = 0
if "last_login" not in st.session_state:
    st.session_state["last_login"] = "not recorded"
if "username" not in st.session_state:
    st.session_state["username"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"
if "form_mode" not in st.session_state:
    st.session_state["form_mode"] = "login"


def set_form_mode(mode):
    st.session_state.form_mode = mode


# =========================================================
# 📝 REGISTRATION FUNCTION
# =========================================================
def registration_form():
    """Form for creating a new user account."""
    st.title("➕ Create a new account")
    with st.form("registration_form"):
        st.markdown("Please enter your information.")
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        full_name = st.text_input("Full name")
        role = st.selectbox(
            "Role",
            options=[
                "ADMIN",
                "DOCTOR",
                "MIDWIFE",
                "NURSE",
                "PATIENT",
                "STUDENT",
                "DOCTORAL",
                "INTERN",
            ],
        )
        register_button = st.form_submit_button("Register")

    if register_button:
        if not email or not password or not full_name:
            st.error("❌ Please fill in all fields.")
            return
        st.success("✅ Account successfully created! You can now log in. (Simulated)")
        st.session_state.form_mode = "login"
        st.rerun()


# =========================================================
# 🔐 UPDATED AUTHENTICATION FUNCTION
# =========================================================
def authentifier():
    """User authentication function."""
    st.title("🔐 Secure Connection")

    # Dictionnaire pour mapper les rôles aux pages d'accueil par défaut
    home_pages = {
        "ADMIN": "packs/home_admin.py",
        "DOCTOR": "packs/home_doctor.py",
        "NURSE": "packs/home_nurse.py",
        "MIDWIFE": "packs/home_midwife.py",
        "PATIENT": "packs/home_patient.py",
        "STUDENT": "packs/home_student.py",
        "DOCTORAL": "packs/home_doctoral.py",
        "INTERN": "packs/home_intern.py",
    }

    with st.form("login_form"):
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Log in")

    if login_button:
        # Données d'authentification simulées
        auth_data = {
            "admin@test.com": {"full_name": "Admin User", "role": "ADMIN"},
            "midwife@test.com": {"full_name": "Jane Midwife", "role": "MIDWIFE"},
            "patient@test.com": {"full_name": "Sarah Patient", "role": "PATIENT"},
        }


if password == "test" and email in auth_data:
    user_info = auth_data[email]
    st.session_state["logged_in"] = True
    st.session_state["user_info"] = user_info
    st.session_state["role"] = user_info["role"]
    st.session_state["full_name"] = user_info["full_name"]
    st.session_state["last_login"] = datetime.now().strftime("%A %d %B %Y at %H:%M")

    log_audit_event(user_info["full_name"], "Login Success", f"User {email} logged in.")

    # Redirection selon le rôle
    if user_info["role"] in ["DOCTOR", "MIDWIFE", "NURSE"]:
        st.switch_page("modules/interface_medecin.py")
    elif user_info["role"] == "PATIENT":
        st.switch_page("modules/interface_patient.py")
    else:
        st.session_state["current_page"] = "home"
        st.rerun()
else:
    log_audit_event(email, "Login Failed", "Incorrect email or password.")
    st.error("❌ Incorrect credentials.")

# =========================================================
# 🛠️ UTILITY FUNCTIONS (pas de changement ici)
# =========================================================
COMMUNITIES = {
    "Mistissini": (50.426, -73.882),
    "Chisasibi": (53.666, -78.792),
    "Waskaganish": (51.733, -78.757),
}
CREE_CONDITIONS = {
    0: "Wāwīpān",
    1: "Mīna wāwīpān",
    2: "Mīna wāwīpān",
    3: "Yūtin",
    45: "Wāpiskāw mīna yūtin",
    48: "Wāpiskāw mīna yūtin",
    51: "Nipīhūn",
    61: "Nipīhūn",
    71: "Wāpiskāw",
    80: "Nipīhūn mīna yūtin",
    95: "Nipīhūn mīhūtin",
}
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
fiches = {
    "Transmission of Knowledge": {
        "titre": "Transmission of Knowledge",
        "image": os.path.join(static_dir, "Grand_mere_et_enfant.png"),
        "description": "👵 The elders share their wisdom through stories and gestures.",
        "citation": "« What you learn with your heart, you never forget. »",
    },
    "Welcome to the Territory": {
        "titre": "Welcome to the Territory",
        "image": os.path.join(static_dir, "Accueil_territoire.png"),
        "description": "🌿 The sacred bond with the land, ancestors, and protective spirits.",
        "citation": "« Every step on this land is a prayer. »",
    },
    "Maternity and Continuity": {
        "titre": "Maternity and Continuity",
        "image": os.path.join(static_dir, "Mere_crie.png"),
        "description": "👩‍👧 The strength of Cree mothers, guardians of life and the future.",
        "citation": "« Carrying a child is carrying the history of our people. »",
    },
    "The Awaited Return": {
        "titre": "The Breath of the Future",
        "image": os.path.join(static_dir, "Le_retour_attendu.png"),
        "description": "Two young mothers sharing a quiet moment with their newborns.",
        "citation": "« The life we hold in our arms is the legacy of our ancestors and the future of our people. »",
    },
    "The Transmission of Ancestral Knowledge": {
        "titre": "The Transmission of Ancestral Knowledge",
        "image": os.path.join(static_dir, "Tissage_et_transmission.png"),
        "description": "Gestures and traditions that connect maternity to the spirit of the land.",
        "citation": "« In every fold of an elder's skin, stories are hidden that will protect the newborn. »",
    },
    "Nature's Cradle": {
        "titre": "Nature's Cradle",
        "image": os.path.join(static_dir, "Berceau_nature.png"),
        "description": "From their first moments, nature is integrated into the care of toddlers.",
        "citation": "« Like a seed in the earth, our baby will find its strength in the territory. »",
    },
}


def image_to_base64(image_path):
    # ... (le code reste le même)
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = os.path.splitext(image_path)[1][1:]
            return f"data:image/{ext};base64,{encoded}"
    else:
        st.error(f"Image not found: {image_path}")
        return None


@st.cache_data
def get_current_weather(lat, lon):
    # ... (le code reste le même)
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


def generate_carousel_html(fiches):
    # ... (le code reste le même)
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
                <p>⚠️ Image not found</p>
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
        .progress-bar {{
            height: 4px;
            background: #ddd;
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
        }}
        .progress-bar-inner {{
            height: 100%;
            background: #007bff;
            transition: width 0.1s linear;
        }}
    </style>
    <div class="swiper">
        <div class="swiper-wrapper">
            {slides}
        </div>
        <div class="progress-bar">
            <div class="progress-bar-inner"></div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.js"></script>
    <script>
        const progressBar = document.querySelector('.progress-bar-inner');
        const swiper = new Swiper('.swiper', {{
            loop: true,
            autoplay: {{
                delay: 6000,
                disableOnInteraction: false,
            }},
            on: {{
                autoplayTimeLeft(s, timeLeft, percentage) {{
                    progressBar.style.width = (1 - percentage) * 100 + '%';
                }}
            }}
        }});
    </script>
    """
    return html_code


# def play_audio(file_path):
#     # ... (le code reste le même)
#     try:
#         if os.path.exists(file_path):
#             with open(file_path, "rb") as audio_file:
#                 audio_bytes = audio_file.read()
#             st.audio(audio_bytes, format="audio/mpeg", start_time=0)
#         else:
#             st.error(f"Audio file not found: {file_path}")
#     except Exception as e:
#         st.error(f"An error occurred while playing the audio: {e}")


# # Audio Player Interface (le code reste le même)
# AUDIO_PATH = os.path.join(utils_dir, "assets", "bebe_pleure.mp3")
# if "mute" not in st.session_state:
#     st.session_state.mute = False
# col1, col2 = st.columns([3, 1])
# with col2:
#     if st.button("🔇 Mute" if not st.session_state.mute else "🔊 Unmute"):
#         st.session_state.mute = not st.session_state.mute
#         st.rerun()
# if not st.session_state.mute:
#     play_audio(AUDIO_PATH)


def load_last_login():
    login_data_path = os.path.join(data_dir, "last_login.json")
    if os.path.exists(login_data_path):
        with open(login_data_path, "r") as f:
            return json.load(f)
    return {}


def save_last_login(data):
    login_data_path = os.path.join(data_dir, "last_login.json")
    with open(login_data_path, "w") as f:
        json.dump(data, f, indent=4)


def afficher_menu(role):
    # ... (le code reste le même)
    user_name = st.session_state.get("full_name", "Inconnu")
    choix = None
    st.sidebar.header("🧭 Navigation")
    st.sidebar.markdown(f"👤 Utilisateur : **{user_name}**")
    st.sidebar.markdown(f"🎭 Rôle : **{role}**")
    st.sidebar.markdown("---")
    st.sidebar.info(
        f"Dernière connexion : {st.session_state.get('last_login', 'Non enregistrée')}"
    )
    st.sidebar.progress(80)
    st.sidebar.markdown(
        """
    <style>
        .unread-badge {
            display: inline-block;
            margin-left: 10px;
            padding: 2px 8px;
            border-radius: 12px;
            background-color: #17A2B8;
            color: white;
            font-size: 12px;
            font-weight: bold;
            line-height: 1;
            vertical-align: middle;
            text-align: center;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    visible_packs = get_packs_for_role(role)
    for pack in visible_packs:
        with st.sidebar.expander(f"📦 {pack}"):
            pages = sorted(
                st.session_state.get("MENU_MAPPING", {}).get(pack, []),
                key=lambda x: x["order"],
            )
            for page in pages:
                page_name = page.get("name")
                page_file = page.get("file")
                if not page_file:
                    st.warning(
                        f"La page '{page_name}' n'a pas de fichier associé et ne peut être chargée."
                    )
                    continue
                if page_name == "MESSAGES":
                    unread_count = st.session_state.get("unread_messages", 0)
                    if unread_count > 0:
                        page_name += (
                            f' <span class="unread-badge">{unread_count}</span>'
                        )
                if est_autorise(role, pack, user_name):
                    if st.button(page_name, key=f"page_btn_{page['id']}"):
                        log_audit_event(
                            user_name,
                            "Menu Click",
                            f"User selected page '{page_name}' from pack '{pack}'",
                        )
                        choix = page_file
                        if "MESSAGES" in page_name:
                            st.session_state["unread_messages"] = 0
                        st.session_state["current_page"] = page_file
                        st.rerun()
                else:
                    log_audit_event(
                        user_name,
                        "Unauthorized Access Attempt",
                        f"User tried to access page '{page_name}' from pack '{pack}'",
                    )
    st.sidebar.markdown("---")
    if st.sidebar.button("🔓 Déconnexion", key="logout_button"):
        log_audit_event(user_name, "Logout", "User logged out successfully.")
        st.session_state.clear()
        st.rerun()
    return choix


def render(role):
    # ... (le code reste le même)
    role_messages = {
        "ADMIN": "Welcome, **Administrator**. Here, you can access all pages for user management, data, and configurations.",
        "DOCTOR": "Welcome, **Doctor**. You have access to patient files, diagnoses, and prescriptions.",
        "NURSE": "Welcome, **Nurse**. You can manage patient information and appointments.",
        "MIDWIFE": "Welcome, **Midwife**. This section is dedicated to prenatal and postnatal care.",
        "PATIENT": "Welcome, **Patient**. You will find information about your follow-up and useful resources here.",
        "STUDENT": "Welcome, **Student**. Access your courses, grades, and internship evaluations.",
        "INTERN": "Welcome, **Intern**. You can view your internship journal and evaluations.",
        "DOCTORAL": "Welcome, **Doctoral Student**. This section is for research, publications, and thesis tracking.",
        "GUEST": "Welcome to the platform! Log in to see your dashboard.",
    }
    st.title(f"Welcome to the {role} space")
    st.markdown("---")
    if role in ["ADMIN", "DOCTOR", "MIDWIFE", "NURSE"]:
        with st.expander("🔔 Clinical reminders"):
            st.warning(
                "⚠️ **Reminder**: Check the files of at-risk patients in the Patient folder."
            )
            st.info(
                "💡 Remember to schedule the postnatal consultation for patient Sarah M."
            )
    role_message = role_messages.get(
        role, "Welcome to the platform! Log in to see your dashboard."
    )
    st.info(role_message)
    if role in ["ADMIN", "DOCTOR", "MIDWIFE", "NURSE"]:
        st.markdown("---")
        st.subheader("⚠️ Vital clinical data")
        col_vital1, col_vital2 = st.columns(2)
        with col_vital1:
            st.warning("🔒 Restricted access: **Allergies and risks**")
            allergies = st.radio("Select patient:", ["Sarah", "Marie"])
            if allergies == "Sarah":
                with st.expander("Allergy file"):
                    st.error("**Allergies:** Penicillin, peanuts")
                    st.warning("**Risk:** Gestational hypertension")
            elif allergies == "Marie":
                with st.expander("Allergy file"):
                    st.info("**Allergies:** None known")
                    st.warning("**Risk:** Gestational diabetes")
        with col_vital2:
            st.success("🩸 **Emergency information**")
            if st.button("Display emergency info"):
                st.info(
                    f"""
                **Blood type:** A+
                **Conditions:** Anemia
                **Emergency contact:** John (Spouse) - 514-555-1234
                """
                )
                st.snow()
    st.markdown("---")
    st.subheader("🎒 Cultural Packs")
    st.markdown("Explore stories, songs, and knowledge passed down by the elders.")
    try:
        carousel_html = generate_carousel_html(fiches)
        components.html(carousel_html, height=450)
    except NameError:
        st.error("⚠️ Cultural data (cards) is not available.")
    except Exception as e:
        st.error(f"⚠️ An error occurred while loading the carousel: {e}")
    st.markdown(
        """
---
### *Here begins the breath of the world.*

Under blankets of moss and sky, 
a Cree mother embraces her child, 
and the territory listens.

The newborn's cries are not screams — 
they are ancient songs, 
calls to the wind, 
promises of roots.

Welcome to where life is born in the arms of knowledge, 
where every heartbeat is a memory, 
where the future is woven in the eyes of women.
---
"""
    )
    st.markdown("---")
    st.subheader("🌦️ Community Weather")
    cols = st.columns(len(COMMUNITIES))
    for col, (name, coords) in zip(cols, COMMUNITIES.items()):
        weather = get_current_weather(*coords)
        if weather:
            icon = WEATHER_ICONS.get(weather["weather_code"], "🌤️")
            cree_cond = CREE_CONDITIONS.get(weather["weather_code"], "")
            col.metric(
                label=name,
                value=f"{weather['temp']}°C {icon}",
                delta=cree_cond if cree_cond else None,
            )
        else:
            col.error(f"Weather unavailable for {name}")
    st.markdown("---")
    st.subheader("🗺️ Map of Communities")
    map = folium.Map(location=[51.5, -78.7], zoom_start=5)
    for name, coords in COMMUNITIES.items():
        weather = get_current_weather(*coords)
        if weather:
            icon = WEATHER_ICONS.get(weather["weather_code"], "❔")
            cree_cond = CREE_CONDITIONS.get(weather["weather_code"], "Unknown")
            popup_html = f"<b>{name}</b><br>{icon} {cree_cond}<br>{weather['temp']}°C"
        else:
            popup_html = f"<b>{name}</b><br>Weather unavailable"
        folium.Marker(
            location=coords,
            tooltip=name,
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="red", icon="fa-baby", prefix="fa"),
        ).add_to(map)
    st_folium(map, width=700, height=400)
    st.markdown("---")
    st.subheader("📅 Upcoming Appointments")
    st.info("No appointments scheduled for today.")
    st.markdown("---")
    st.subheader("🌤️ Local weather by community")
    communaute = st.selectbox("Choose your community:", list(COMMUNITIES.keys()))
    lat, lon = COMMUNITIES.get(communaute, (50.4184, -73.8693))
    weather = get_current_weather(lat, lon)
    if weather:
        code = weather["weather_code"]
        temp = weather["temp"]
        wind = weather["wind"]
        icon = WEATHER_ICONS.get(code, "❔")
        cri = CREE_CONDITIONS.get(code, "Unknown")
        if role == "ADMIN":
            st.info(
                f"{icon} **{cri}** — {temp}°C, wind {wind} km/h.\n🌾 In {communaute}, plan your trips for deliveries."
            )
        elif role == "PATIENT":
            st.info(
                f"{icon} **{cri}** — {temp}°C, wind {wind} km/h.\n💖 In {communaute}, a gentle weather for a walk with baby!"
            )
        else:
            st.warning(
                "❓ Unrecognized role — weather displayed without personalization."
            )
    else:
        st.error("Unable to retrieve weather.")
    st.markdown("---")
    st.subheader("📊 Quick Statistics")
    col1, col2, col3 = st.columns(3)
    if role in ["ADMIN"]:
        st.info("Professional statistics:")
        col1.metric("💉 Vaccination", "78%", "↑ 5%")
        col2.metric("🍼 Breastfeeding", "65%", "↔ Stable")
        col3.metric("⚠️ Complications", "12%", "↓ 2%")
    elif role == "PATIENT":
        st.info("Personal follow-up statistics:")
        col1.metric("❤️ Baby weight", "5.2 kg", "↑ 0.3 kg")
        col2.metric("💤 Sleep hours", "8h", "↔ Stable")
        col3.metric("🍏 Nutritional follow-up", "Excellent", "↑")
    elif role in ["STUDENT", "INTERN", "DOCTORAL"]:
        st.info("Research statistics:")
        col1.metric("📄 Articles", "124", "↑ 20")
        col2.metric("📚 Studies read", "65", "↔ Stable")
        col3.metric("🔍 Themes explored", "12", "↓ 2")
    else:
        st.info("No statistics available for this role.")
    st.markdown("---")
    st.subheader("🔔 Notifications")
    if role in ["MIDWIFE", "ADMIN", "DOCTOR", "NURSE", "INTERN", "STUDENT", "DOCTORAL"]:
        st.warning("📨 You have 2 unread messages.")
        st.info("📅 Reminder: team meeting tomorrow at 9 a.m.")
    elif role == "PATIENT":
        st.warning("🔔 Your baby's follow-up is ready.")
        st.info("💡 New blog articles on breastfeeding.")
    else:
        st.info("No notifications for this role.")
    st.markdown("---")
    st.subheader("🎥 Explanatory video")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")


def interface():
    """Fonction principale pour l'interface de l'utilisateur authentifié."""
    role = st.session_state["role"]
    choix_menu = afficher_menu(role)
    if choix_menu:
        st.session_state["current_page"] = choix_menu
        log_audit_event(
            st.session_state.get("full_name", "Inconnu"),
            "Page Change",
            f"User navigated to page: {choix_menu}",
        )
    current_page_file = st.session_state["current_page"]
    if current_page_file == "home":
        render(role)
    else:
        try:
            page_path = os.path.join(script_dir, "modules", current_page_file)
            if not os.path.exists(page_path):
                st.error(f"❌ Le fichier de page n'a pas été trouvé : {page_path}")
                st.stop()
            spec = importlib.util.spec_from_file_location(current_page_file, page_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.render()
        except FileNotFoundError:
            st.error("❌ Le fichier de page sélectionné n'a pas été trouvé.")
        except Exception as e:
            st.error(
                f"❌ Une erreur s'est produite lors du chargement de la page : {e}"
            )


# =========================================================
# 🚀 POINT D'ENTRÉE PRINCIPAL DE L'APPLICATION
# =========================================================
if __name__ == "__main__":
    if st.session_state.get("logged_in", False):
        interface()
    else:
        st.sidebar.title("Bienvenue !")
        st.sidebar.info("Veuillez vous connecter ou vous inscrire.")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Se connecter", key="btn_login"):
                st.session_state.form_mode = "login"
                st.rerun()
        with col2:
            if st.button("S'inscrire", key="btn_register"):
                st.session_state.form_mode = "register"
                st.rerun()
        if st.session_state.form_mode == "login":
            authentifier()
        else:
            registration_form()
