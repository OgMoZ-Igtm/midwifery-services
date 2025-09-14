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
import sqlite3
from utils.logger import log_info, log_error, log_user_action

log_info("Application démarrée")
try:
    log_user_action("admin@example.com", "admin", "modification du menu")
except Exception as e:
    st.error(f"Erreur lors de la journalisation : {e}")
log_error("Erreur de connexion à la base de données")
print("Signature de log_user_action :", log_user_action.__code__.co_varnames)
st.title("Bienvenue dans Midwifery Services")
st.write("L'application est bien lancée.")

# Importation manquante pour la sécurité
import bcrypt

# Assurez-vous que cette fonction existe dans votre projet
try:
    from utils.permissions import get_role_display
except ImportError:

    def get_role_display(role):
        """Fonction de remplacement si utils.permissions n'existe pas."""
        return "❓", "#CCCCCC"


# =========================================================
# 📁 CHEMINS ET RESSOURCES
# =========================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
menu_path = os.path.join(script_dir, "data", "menu_mapping.json")
login_data_path = os.path.join(script_dir, "data", "last_login.json")
users_data_path = os.path.join(
    script_dir, "data", "users.json"
)  # Ajouté pour gestion des utilisateurs


# Assure que le dossier 'data' existe
if not os.path.exists(os.path.join(script_dir, "data")):
    os.makedirs(os.path.join(script_dir, "data"))

# 📦 Chargement du menu
if os.path.exists(menu_path):
    with open(menu_path, "r", encoding="utf-8") as f:
        menu_mapping = json.load(f)
else:
    st.error(f"Le fichier de configuration du menu est introuvable : {menu_path}")
    menu_mapping = {}


# 👥 Gestion des utilisateurs pour la démo
def load_users():
    if os.path.exists(users_data_path):
        with open(users_data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


USERS = load_users()


def save_users(users):
    """Sauvegarde les données des utilisateurs dans un fichier JSON."""
    with open(users_data_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def hash_password(password):
    """Hashe un mot de passe en utilisant bcrypt."""
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode("utf-8")


def check_password(password, hashed_password):
    """Vérifie un mot de passe haché."""
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


# =========================================================
# 🛡️ SÉCURITÉ : GESTION DES PERMISSIONS ET DES SESSIONS
# =========================================================
# Définition des permissions par rôle
ROLE_PERMISSIONS = {
    "ADMIN": ["dashboard_access", "patient_write", "patient_read", "user_management"],
    "DOCTOR": ["dashboard_access", "patient_write", "patient_read"],
    "NURSE": ["dashboard_access", "patient_write", "patient_read"],
    "MIDWIFE": ["dashboard_access", "patient_write", "patient_read"],
    "PATIENT": ["dashboard_access", "patient_read_own"],
    "STUDENT": ["dashboard_access", "patient_read_limited"],
    "INTERN": ["dashboard_access", "patient_read_limited"],
    "DOCTORAL": ["dashboard_access", "patient_read_limited"],
    "GUEST": ["dashboard_access"],
}


def check_permission(permission):
    """Vérifie si le rôle de l'utilisateur a la permission demandée."""
    user_role = st.session_state.get("role", "GUEST")
    return permission in ROLE_PERMISSIONS.get(user_role, []) or user_role == "ADMIN"


def check_session_timeout(timeout_minutes=15):
    """Déconnecte l'utilisateur après une période d'inactivité."""
    last_activity = st.session_state.get("last_activity", datetime.now())
    inactivity_duration = (datetime.now() - last_activity).total_seconds() / 60
    if inactivity_duration > timeout_minutes:
        st.session_state.clear()
        st.session_state["page_state"] = "login"
        st.warning("Votre session a expiré en raison d'une inactivité prolongée.")
        st.rerun()
    else:
        st.session_state["last_activity"] = datetime.now()


def alerter_admin(message):
    # Exemple simple : afficher dans Streamlit
    import streamlit as st

    st.error(f"🚨 ALERTE ADMIN : {message}")


# =========================================================
# 🏠 VARIABLES ET RESSOURCES GLOBALES
# =========================================================
COMMUNITIES = {
    "Mistissini": (50.4184, -73.8693),
    "Chisasibi": (53.8050, -78.9167),
    "Waskaganish": (51.4800, -78.7500),
}
METEO_TRADUCTIONS = {
    "Clear": {"fr": "Clair", "en": "Clear", "cr": "Wâpikîw", "code": 0},
    "Mainly clear": {
        "fr": "Principalement clair",
        "en": "Mainly clear",
        "cr": "Wâpikîw",
        "code": 1,
    },
    "Partly cloudy": {
        "fr": "Partiellement nuageux",
        "en": "Partly cloudy",
        "cr": "Wâsêw",
        "code": 2,
    },
    "Overcast": {"fr": "Couvert", "en": "Overcast", "cr": "Wâsêw-wâsêw", "code": 3},
    "Fog and depositing rime fog": {
        "fr": "Brouillard",
        "en": "Fog",
        "cr": "Wâsêw-nipî",
        "code": 45,
    },
    "Drizzle": {"fr": "Bruine", "en": "Drizzle", "cr": "Kîmôw-sîpîs", "code": 51},
    "Rain": {"fr": "Pluie", "en": "Rain", "cr": "Kîmôw", "code": 61},
    "Snow": {"fr": "Neige", "en": "Snow", "cr": "Kôna", "code": 71},
    "Rain showers": {
        "fr": "Averses de pluie",
        "en": "Rain showers",
        "cr": "Kîmôw",
        "code": 80,
    },
    "Thunderstorm": {"fr": "Orages", "en": "Thunderstorm", "cr": "Pîmiwan", "code": 95},
}
CREE_CONDITIONS = {v["code"]: v["cr"] for v in METEO_TRADUCTIONS.values()}
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


# =========================================================
# 🛠️ FONCTIONS UTILITAIRES
# =========================================================
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


@st.cache_data(ttl=3600)
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


def generate_carousel_html(fiches):
    """Génère le code HTML pour le carrousel Swiper."""
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
        .swiper {{ width: 100%; height: 600px; }}
        .swiper-slide {{ text-align: center; font-size: 18px; background: #fff; padding: 20px; }}
        img {{ max-height: 600px; object-fit: cover; }}
        .progress-bar {{ height: 4px; background: #ddd; position: absolute; bottom: 0; left: 0; width: 100%; }}
        .progress-bar-inner {{ height: 100%; background: #007bff; transition: width 0.1s linear; }}
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


def load_last_login():
    """Charge les données de dernière connexion depuis le fichier JSON."""
    if os.path.exists(login_data_path):
        with open(login_data_path, "r") as f:
            return json.load(f)
    return {}


def save_last_login(data):
    """Sauvegarde les données de dernière connexion dans un fichier JSON."""
    with open(login_data_path, "w") as f:
        json.dump(data, f, indent=4)


def afficher_meteo_communautaire():
    st.subheader("🌤️ Météo des communautés")
    for communauté in ["Mistissini", "Waskaganish", "Chisasibi"]:
        try:
            coords = COMMUNITIES.get(communauté, None)
            if coords:
                meteo = get_current_weather(*coords)
                condition_code = meteo["weather_code"]
                temperature = meteo["temp"]

                # Trouver la traduction en utilisant le code météo
                condition_info = next(
                    (
                        v
                        for v in METEO_TRADUCTIONS.values()
                        if v.get("code") == condition_code
                    ),
                    {"fr": "Inconnu", "en": "Unknown", "cr": "Inconnu"},
                )

                st.markdown(
                    f"""
                    **📍 {communauté}**
                    - 🌡️ {temperature}°C
                    - 🇫🇷 {condition_info['fr']}
                    - 🇬🇧 {condition_info['en']}
                    - 🪶 {condition_info['cr']}
                    """
                )
        except Exception:
            st.warning(f"⚠️ Impossible de récupérer la météo pour {communauté}.")


# =========================================================
# 🔐 GESTION AUTHENTIFICATION, INSCRIPTION & MOT DE PASSE OUBLIÉ
# =========================================================
def login_form():
    """Formulaire d'authentification des utilisateurs."""
    st.title("🔐 Connexion sécurisée")
    username = st.text_input("Nom d'utilisateur (email)")
    password = st.text_input("Mot de passe", type="password")

    # Correction : Utilisation d'un dictionnaire pour les rôles au lieu de la BD
    role_options = sorted(list(set(user["role"] for user in USERS.values())))

    if role_options:
        default_role = st.session_state.get("role", "GUEST")
        index = role_options.index(default_role) if default_role in role_options else 0
        role_choice = st.selectbox("Sélectionnez votre rôle", role_options, index=index)
    else:
        st.warning("⚠️ Aucun rôle disponible. Vérifiez le fichier utilisateurs.")
        role_choice = None

    if st.button("Se connecter", key="login_button"):
        user = USERS.get(username)
        if user:
            if (
                check_password(password, user["password"].encode("utf-8"))
                and user["role"] == role_choice
            ):
                st.session_state["temp_user"] = username
                st.session_state["temp_role"] = user["role"]
                st.session_state["temp_full_name"] = user["full_name"]
                st.session_state.page_state = "mfa"
                st.rerun()
            else:
                st.error("Identifiants ou rôle incorrects.")
        else:
            st.error("Utilisateur non trouvé.")


def mfa_form():
    """Formulaire d'authentification multifacteur."""
    st.title("🛡️ Authentification Multifacteur")
    st.info("Un code de vérification a été envoyé à votre e-mail (simulé : `123456`).")
    mfa_code = st.text_input("Veuillez entrer le code de vérification", max_chars=6)

    if st.button("Vérifier"):
        if mfa_code == "123456":  # Code statique pour la démo
            username = st.session_state["temp_user"]
            login_data = load_last_login()
            last_login = login_data.get(username, "non enregistrée")

            st.session_state["user_info"] = {
                "username": username,
                "role": st.session_state["temp_role"],
                "full_name": st.session_state["temp_full_name"],
            }
            st.session_state["authentifie"] = True
            st.session_state["last_login"] = last_login
            st.session_state["page_state"] = "dashboard"
            st.session_state["last_activity"] = datetime.now()

            login_data[username] = datetime.now().strftime("%A %d %B %Y à %H:%M")
            save_last_login(login_data)

            # Initialisation de la variable après la connexion
            if "unread_messages" not in st.session_state:
                st.session_state["unread_messages"] = 0

            st.success("Connexion réussie ! Redirection vers le tableau de bord...")
            st.rerun()
        else:
            st.error("Code de vérification incorrect.")


def create_account_form():
    """Formulaire d'inscription avec politique de mot de passe."""
    st.title("➕ Créer un compte")
    new_username = st.text_input("Choisissez un nom d'utilisateur (email)")
    new_password = st.text_input("Choisissez un mot de passe", type="password")
    confirm_password = st.text_input("Confirmez le mot de passe", type="password")

    # Rôles disponibles pour l'inscription
    available_roles = ["PATIENT", "STUDENT", "INTERN", "DOCTORAL"]
    assigned_role = st.selectbox("Rôle assigné par l'administrateur", available_roles)

    new_full_name = st.text_input("Votre nom complet (optionnel)")

    if st.button("S'inscrire"):
        if new_username in USERS:
            st.error("Ce nom d'utilisateur existe déjà.")
        elif new_password != confirm_password:
            st.error("Les mots de passe ne correspondent pas.")
        elif len(new_password) < 8:
            st.error("Le mot de passe doit contenir au moins 8 caractères.")
        elif not any(char.isdigit() for char in new_password):
            st.error("Le mot de passe doit contenir au moins un chiffre.")
        elif not any(char.isupper() for char in new_password):
            st.error("Le mot de passe doit contenir au moins une majuscule.")
        else:
            hashed_pw = hash_password(new_password)
            USERS[new_username] = {
                "password": hashed_pw,
                "role": assigned_role,
                "full_name": new_full_name if new_full_name else new_username,
            }
            save_users(USERS)
            st.success(
                "Compte créé avec succès ! Vous pouvez maintenant vous connecter."
            )
            st.session_state.page_state = "login"
            st.rerun()


def forgot_password_form():
    """Fonctionnalité de mot de passe oublié."""
    st.title("❓ Mot de passe oublié")
    username_reset = st.text_input("Nom d'utilisateur")
    if st.button("Réinitialiser le mot de passe"):
        if username_reset in USERS:
            st.success(
                "Un lien de réinitialisation a été envoyé à votre adresse e-mail."
            )
            st.info(
                "Cette fonctionnalité est simulée pour des raisons de démonstration."
            )
            st.session_state.page_state = "login"
        else:
            st.error("Nom d'utilisateur introuvable.")


# =========================================================
# 🧭 GESTION DU MENU ET DES PAGES
# =========================================================
def get_visible_packs(role):
    """Retourne la liste des packs de menu visibles selon le rôle."""
    packs_visibles = []

    # Packs de base visibles pour tous les utilisateurs, sauf l'admin
    if role != "ADMIN":
        packs_visibles.extend(["PROFILE", "MESSAGES"])

    # Packs spécifiques à chaque rôle
    if role == "ADMIN":
        packs_visibles.extend(list(menu_mapping.keys()))
    elif role == "MIDWIFE":
        packs_visibles.append("MIDWIFE")
    elif role == "NURSE":
        packs_visibles.append("NURSE")
    elif role == "PATIENT":
        packs_visibles.append("PATIENT")
    elif role == "STUDENT":
        packs_visibles.append("STUDENT")
    elif role == "INTERN":
        packs_visibles.append("INTERN")
    elif role == "DOCTOR":
        packs_visibles.append("DOCTOR")
    elif role == "DOCTORAL":
        packs_visibles.append("DOCTORAL")

    # Éliminer les doublons pour l'ADMIN et l'ALL
    return list(set(packs_visibles))


def afficher_menu(role):
    """Affiche le menu latéral dynamique."""
    visible_packs = get_visible_packs(role)

    st.sidebar.header("🧭 Menu")
    st.sidebar.markdown(
        f"👤 Utilisateur : **{st.session_state.get('full_name', 'inconnu')}**"
    )
    st.sidebar.markdown(f"🎭 Rôle : **{role}**")
    st.sidebar.markdown("---")
    st.sidebar.progress(80)

    # 💅 Style du badge
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

    for pack in visible_packs:
        # Correction pour éviter le TypeError
        pages = menu_mapping.get(pack, [])
        if not isinstance(pages, list):
            # Si le pack n'est pas une liste (par ex., une chaîne de caractères),
            # on passe au suivant.
            continue

        pages_valides = [
            p for p in pages if isinstance(p, dict) and "order" in p and "roles" in p
        ]
        pages_triees = sorted(pages_valides, key=lambda x: x["order"])

        with st.sidebar.expander(f"📦 {pack}"):
            for page in pages_triees:
                if role not in page["roles"]:
                    continue

                page_name = page["name"]
                page_id = page["id"]
                page_file = page["file"]

                # 📨 Gestion des messages non lus
                if page_name.upper() == "MESSAGES":
                    unread_count = st.session_state.get("unread_messages", 0)
                    if unread_count > 0:
                        page_name_with_badge = f"{page_name} <span class='unread-badge'>{unread_count}</span>"
                        if st.button(
                            page_name_with_badge,
                            key=f"page_btn_{page_id}",
                            unsafe_allow_html=True,
                        ):
                            st.session_state["unread_messages"] = 0
                            st.session_state["choix"] = page_file
                            st.rerun()
                            return
                    else:
                        if st.button(page_name, key=f"page_btn_{page_id}"):
                            st.session_state["choix"] = page_file
                            st.rerun()
                            return
                else:
                    if st.button(page_name, key=f"page_btn_{page_id}"):
                        st.session_state["choix"] = page_file
                        st.rerun()
                        return


def afficher_dashboard():
    """Affiche le contenu du tableau de bord pour l'utilisateur authentifié."""
    role = st.session_state.get("user_info", {}).get("role", "GUEST")
    full_name = st.session_state.get("user_info", {}).get("full_name", "utilisateur")
    last_login = st.session_state.get("last_login", "non enregistrée")

    st.title(f"👋 Bienvenue, {full_name}")
    st.markdown(f"**🎓 Rôle :** `{role}`")
    st.markdown(f"**🕒 Dernière connexion :** {last_login}")

    if check_permission("user_management"):
        st.info(
            "🔒 Vous avez les droits d'administration pour la gestion des utilisateurs."
        )

    st.markdown("---")

    st.subheader("🌟 Présentation du projet")
    role_messages = {
        "ADMIN": "Bienvenue, **Administrateur**. Ici, vous pouvez accéder à toutes les pages pour la gestion des utilisateurs, des données et des configurations.",
        "DOCTOR": "Bienvenue, **Docteur**. Vous avez accès aux dossiers des patients, aux diagnostics et aux prescriptions.",
        "NURSE": "Bienvenue, **Infirmier/Infirmière**. Vous pouvez gérer les informations des patients et les rendez-vous.",
        "MIDWIFE": "Bienvenue, **Sage-femme**. Cette section est dédiée aux soins prénatals et postnatals.",
        "PATIENT": "Bienvenue, **Patient(e)**. Vous trouverez ici des informations sur votre suivi et des ressources utiles.",
        "STUDENT": "Bienvenue, **Étudiant(e)**. Accédez à vos cours, vos notes et vos évaluations de stage.",
        "INTERN": "Bienvenue, **Interne**. Vous pouvez consulter votre journal de stage et vos évaluations.",
        "DOCTORAL": "Bienvenue, **Doctorant(e)**. Cette section est pour la recherche, les publications et le suivi de votre thèse.",
        "GUEST": "Bienvenue sur la plateforme! Connectez-vous pour voir votre tableau de bord.",
    }
    st.info(role_messages.get(role, "Bienvenue sur la plateforme!"))

    st.markdown("---")
    st.subheader("🎒 Packs culturels")
    try:
        carousel_html = generate_carousel_html(fiches)
        components.html(carousel_html, height=450)
    except Exception as e:
        st.error(f"⚠️ Une erreur est survenue lors du chargement du carrousel : {e}")

    st.markdown("---")
    st.subheader("🌦️ Météo des communautés")
    cols = st.columns(len(COMMUNITIES))
    for col, (name, coords) in zip(cols, COMMUNITIES.items()):
        weather = get_current_weather(*coords)
        if weather:
            icon = WEATHER_ICONS.get(weather["weather_code"], "❓")
            cree_cond = CREE_CONDITIONS.get(weather["weather_code"], "Inconnu")
            col.metric(label=name, value=f"{weather['temp']}°C {icon}", delta=cree_cond)
        else:
            col.error(f"Météo indisponible pour {name}")

    st.markdown("---")
    st.subheader("🗺️ Carte des communautés")
    map = folium.Map(location=[51.5, -78.7], zoom_start=5)
    for name, coords in COMMUNITIES.items():
        weather = get_current_weather(*coords)
        if weather:
            icon = WEATHER_ICONS.get(weather["weather_code"], "❔")
            cree_cond = CREE_CONDITIONS.get(weather["weather_code"], "Inconnu")
            popup_html = f"<b>{name}</b><br>{icon} {cree_cond}<br>{weather['temp']}°C"
        else:
            popup_html = f"<b>{name}</b><br>Météo indisponible"
        folium.Marker(
            location=coords,
            tooltip=name,
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="red", icon="fa-baby", prefix="fa"),
        ).add_to(map)
    st_folium(map, width=700, height=400)


def interface():
    """Fonction principale pour l'interface utilisateur authentifiée."""
    check_session_timeout()

    # Correction : Utilisation de user_info
    role = st.session_state.get("user_info", {}).get("role", "GUEST")

    # Correction : Utilisation d'une variable locale
    st.sidebar.markdown(
        f"👤 Utilisateur : **{st.session_state.get('user_info', {}).get('full_name', 'inconnu')}**"
    )
    st.sidebar.markdown(f"🎭 Rôle : **{role}**")

    # Appel de la fonction pour afficher le menu
    visible_packs = get_visible_packs(role)
    afficher_menu_corrigee(role, visible_packs, menu_mapping)

    # Déplacement du bouton de déconnexion dans l'interface
    st.sidebar.markdown("---")
    if st.sidebar.button("🔓 Déconnexion", key="logout_button"):
        st.session_state.clear()
        st.session_state["page_state"] = "login"
        st.rerun()

    choix = st.session_state.get("choix", "dashboard")

    if choix == "dashboard":
        afficher_dashboard()
    else:
        page_info = None
        for pack_pages in menu_mapping.values():
            if not isinstance(pack_pages, list):
                continue
            for page in pack_pages:
                if isinstance(page, dict) and page.get("file") == choix:
                    page_info = page
                    break
            if page_info:
                break

        if not page_info:
            st.error(
                "Page introuvable dans le fichier de menu. Veuillez vérifier 'menu_mapping.json'."
            )
            st.session_state["choix"] = "dashboard"
            st.rerun()
            return

        st.markdown(f"### 📄 Page sélectionnée : `{page_info['name']}`")
        is_readonly = role in page_info.get("readonly", [])
        if is_readonly:
            st.warning("🔒 Vous êtes en mode lecture seule pour cette page.")

        try:
            chemin_complet = os.path.join(script_dir, choix)
            if os.path.exists(chemin_complet):
                with open(chemin_complet, "r", encoding="utf-8") as f:
                    code = f.read()
                exec(code, globals())
            else:
                st.info(
                    f"Le contenu de la page '{page_info['name']}' n'est pas encore implémenté. Fichier manquant: `{choix}`"
                )

        except Exception as e:
            st.error(f"Erreur lors du chargement de la page : {e}")


# Cette fonction est une copie temporaire pour la démo, car la version originale est dupliquée.
# La version corrigée ci-dessus est la seule qui sera utilisée.
def afficher_menu_corrigee(role_utilisateur, visible_packs, menu_mapping):
    st.sidebar.header("🧭 Menu")
    st.sidebar.markdown(
        f"👤 Utilisateur : **{st.session_state.get('full_name', 'inconnu')}**"
    )
    st.sidebar.markdown(f"🎭 Rôle : **{role_utilisateur}**")
    st.sidebar.markdown("---")
    st.sidebar.progress(80)
