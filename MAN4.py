import streamlit as st
import requests
import os
import json
import time
import modules.Home
import modules.Login
from PIL import Image
import folium
from streamlit_folium import st_folium

m = folium.Map(location=[48.85, 2.35], zoom_start=12)
st_folium(m, use_container_width=True, height=600)
import streamlit.components.v1 as components
import base64
from datetime import datetime
import importlib.util
from utils.security import get_packs_for_role
from utils.permissions import afficher_tableau_des_permissions
from utils.permissions import get_accessible_sections, afficher_tableau_des_permissions

# Afficher le tableau des permissions
afficher_tableau_des_permissions()

# Récupérer les sections accessibles pour le rôle "DOCTOR"
sections = get_accessible_sections("DOCTOR", action="view")

# Afficher le résultat
print(sections)


# --- NOUVEAU : Import de la librairie Supabase et de la configuration ---
# from supabase import create_client, Client


# --- Initialisation de Supabase à l'aide des secrets de Streamlit ---
# @st.cache_resource
# def init_supabase() -> Client:
#     """Initialise le client Supabase avec les secrets de l'application."""
#     url = st.secrets["SUPABASE_URL"]
#     key = st.secrets["SUPABASE_KEY"]
#     return create_client(url, key)


# supabase = init_supabase()
# # On ajoute l'objet supabase dans la session pour qu'il soit accessible partout
# st.session_state["supabase"] = supabase


# --- Chargement dynamique du dictionnaire de menus depuis le fichier JSON ---
try:
    # Chemin absolu du dossier 'utils'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    utils_dir = os.path.join(script_dir, "utils")
    menu_mapping_path = os.path.join(utils_dir, "menu_mapping.json")

    with open(menu_mapping_path, "r", encoding="utf-8") as f:
        MENU_MAPPING = json.load(f)

except FileNotFoundError:
    st.error(
        f"❌ Le fichier de configuration des menus '{menu_mapping_path}' est introuvable."
    )
    st.stop()
except json.JSONDecodeError:
    st.error(
        "❌ Erreur de format dans le fichier menu_mapping.json. Vérifiez la syntaxe."
    )
    st.stop()


# =========================================================
# 🔐 CONTRÔLE D'ACCÈS PERMANENT
# =========================================================

# Chemin absolu du dossier 'modules'
script_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(script_dir, "modules")
login_path = os.path.join(modules_dir, "Login.py")


# Initialisation des variables de session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None
if "role" not in st.session_state:
    st.session_state["role"] = "GUEST"
if "unread_messages" not in st.session_state:
    st.session_state["unread_messages"] = 0
if "last_login" not in st.session_state:
    st.session_state["last_login"] = "non enregistrée"
if "username" not in st.session_state:
    st.session_state["username"] = None
# Ajout de la variable de session pour la navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"


# Si l'utilisateur n'est pas connecté, le rediriger vers la page d'accueil
if not st.session_state.get("logged_in", False):

    if os.path.exists(login_path):
        try:
            # Ajoute le dossier 'modules' au chemin de recherche Python pour l'import dynamique
            if modules_dir not in os.sys.path:
                os.sys.path.append(modules_dir)

            # Importe et exécute la page de connexion directement
            spec = importlib.util.spec_from_file_location("login", login_path)
            login_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(login_module)

            # --- CORRECTION: ARRÊT DE L'EXÉCUTION SI L'UTILISATEUR N'EST PAS CONNECTÉ ---
            if not st.session_state.get("logged_in", False):
                st.stop()

        except Exception as e:
            st.error(f"❌ Erreur lors du chargement de la page de connexion : {e}")
            st.stop()
    else:
        st.error(
            f"Le fichier 'Login_principal.py' est introuvable à l'emplacement suivant : `{login_path}`."
        )
        st.warning(
            "Veuillez vérifier que le fichier existe bien et que le nom du dossier est 'modules'."
        )
        st.stop()

# --- CORRECTION: LE RESTE DU CODE S'EXÉCUTE SEULEMENT SI L'UTILISATEUR EST CONNECTÉ ---

# Récupérer les informations de l'utilisateur à partir de la session
user_info = st.session_state.get("user_info", {})
full_name = user_info.get("prenom", "Utilisateur")
role = user_info.get("role", "GUEST")
last_login = st.session_state.get("last_login", "non enregistrée")


# Utiliser le rôle pour obtenir les packs autorisés
packs_autorises = get_packs_for_role(role)


# Le reste de votre code reste inchangé...

# 🪶 Message d’accueil trilingue
st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <h2>👋 Wāčiyā! / Bienvenue! / Welcome!</h2>
        <p style="font-size:16px;">
            Nous sommes ravis de vous accueillir dans cette application.<br>
            We're happy to have you here.<br>
            Mīna wāpamiyan — happy to see you.
        </p>
    </div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 📁 CHEMINS ET RESSOURCES
# =========================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
menu_path = os.path.join(script_dir, "data", "menu_mapping.json")
# Ajoute le chemin pour le fichier de dernière connexion
login_data_path = os.path.join(script_dir, "data", "last_login.json")

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


# =========================================================
# 🏠 VARIABLES ET RESSOURCES GLOBALES
# =========================================================

# 📍 Coordonnées des communautés
COMMUNITIES = {
    "Mistissini": (50.426, -73.882),
    "Chisasibi": (53.666, -78.792),
    "Waskaganish": (51.733, -78.757),
}

# 🧠 Traduction cri des conditions météo
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

# Fiches pour le carrousel
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


def generate_carousel_html(fiches):
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

    # Correction de l'indentation et ajout de la barre de progression
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


def play_audio(file_path):
    """
    Plays an audio file from a local path using Streamlit's native component.
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mpeg", start_time=0)
        else:
            st.error(f"Fichier audio introuvable: {file_path}")
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la lecture de l'audio: {e}")


# ---
# Audio Player Interface

# Chemin du son
AUDIO_PATH = "utils/assets/bebe_pleure.mp3"
if "mute" not in st.session_state:
    st.session_state.mute = False

col1, col2 = st.columns([3, 1])
with col2:
    if st.button(
        "🔇 Couper le son" if not st.session_state.mute else "🔊 Activer le son"
    ):
        st.session_state.mute = not st.session_state.mute
        # Re-run the app to apply the mute change
        st.rerun()


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


# =========================================================
# 🔐 GESTION AUTHENTIFICATION ET MENU
# =========================================================


# --- CORRECTION: LA FONCTION `afficher_menu` EST DÉSORMAIS APPELÉE APRÈS LA CONNEXION ---
def get_visible_packs(role):
    """Retourne la liste des packs de menu visibles selon le rôle."""
    if role == "admin":
        return list(MENU_MAPPING.keys())
    elif role == "midwife":
        return ["MIDWIFE", "MESSAGES"]
    elif role == "nurse":
        return ["NURSE", "PATIENT", "MESSAGES"]
    elif role in ["student", "intern", "doctoral"]:
        return [role, "MESSAGES"]
    else:
        return [role]


def afficher_menu(role):
    """Affiche le menu latéral dynamique."""
    visible_packs = get_visible_packs(role)
    st.sidebar.header("🧭 Menu")
    st.sidebar.markdown(f"👤 Utilisateur : **{full_name}**")
    st.sidebar.markdown(f"🎭 Rôle : **{role}**")
    st.sidebar.markdown("---")

    # 🔵 Ajout d'une barre de progression bleue
    st.sidebar.progress(80)

    # Ajout du style CSS pour la pastille de notification
    st.sidebar.markdown(
        """
    <style>
        .unread-badge {
            display: inline-block;
            margin-left: 10px;
            padding: 2px 8px;
            border-radius: 12px;
            background-color: #17A2B8; /* Bleu */
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

    # Ajout des menus dépliants
    for pack in visible_packs:
        with st.sidebar.expander(f"📦 {pack}"):
            for page in sorted(MENU_MAPPING.get(pack, []), key=lambda x: x["order"]):

                # Affiche l'indicateur de messages non lus pour le menu MESSAGES
                page_name = page["name"]
                if page_name == "MESSAGES":
                    unread_count = st.session_state.get("unread_messages", 0)
                    if unread_count > 0:
                        page_name += (
                            f' <span class="unread-badge">{unread_count}</span>'
                        )

                # Utilisation d'un callback pour mettre à jour la page actuelle
                if st.button(page_name, key=f"page_btn_{page['id']}"):
                    st.session_state["current_page"] = page["file"]
                    if page_name.startswith("MESSAGES"):
                        # Réinitialiser le compteur de messages non lus si on clique sur le bouton MESSAGES
                        st.session_state["unread_messages"] = 0
                    st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("🔓 Déconnexion", key="logout_button"):
        st.session_state.clear()
        # Redirection vers la page de connexion après déconnexion
        st.rerun()  # Le contrôle d'accès au début du script gérera la redirection


# =========================================================
# 🚀 RENDU DYNAMIQUE DES PAGES
# =========================================================


def render_home_page():
    """
    Rend la page d'accueil de l'application avec le contenu principal.
    """
    # Dictionnaire des messages par rôle
    role_messages = {
        "admin": "Bienvenue, **Administrateur**. Ici, vous pouvez accéder à toutes les pages pour la gestion des utilisateurs, des données et des configurations.",
        "doctor": "Bienvenue, **Docteur**. Vous avez accès aux dossiers des patients, aux diagnostics et aux prescriptions.",
        "nurse": "Bienvenue, **Infirmier/Infirmière**. Vous pouvez gérer les informations des patients et les rendez-vous.",
        "midwife": "Bienvenue, **Sage-femme**. Cette section est dédiée aux soins prénatals et postnatals.",
        "patient": "Bienvenue, **Patient(e)**. Vous trouverez ici des informations sur votre suivi et des ressources utiles.",
        "student": "Bienvenue, **Étudiant(e)**. Accédez à vos cours, vos notes et vos évaluations de stage.",
        "intern": "Bienvenue, **Interne**. Vous pouvez consulter votre journal de stage et vos évaluations.",
        "doctoral": "Bienvenue, **Doctorant(e)**. Cette section est pour la recherche, les publications et le suivi de votre thèse.",
        "GUEST": "Bienvenue sur la plateforme! Connectez-vous pour voir votre tableau de bord.",
    }

    # Titre personnalisé pour le rôle
    st.title(f"Bienvenue dans l'espace {role.upper()}")
    st.markdown("---")

    # Ajout d'un expander pour les rappels cliniques
    if role in ["admin", "doctor", "midwife", "nurse"]:
        with st.expander("🔔 Rappels cliniques"):
            st.warning(
                "⚠️ **Rappel** : Vérifiez les dossiers des patients à risque dans le dossier Patient."
            )
            st.info(
                "💡 Pensez à planifier la consultation postnatale pour la patiente Sarah M."
            )

    # Afficher le message dédié au rôle
    role_message = role_messages.get(
        role,
        "Bienvenue sur la plateforme! Connectez-vous pour voir votre tableau de bord.",
    )
    st.info(role_message)

    # ======================================================
    # 🏥 Informations de santé cruciales (Sécurisé par rôle)
    # ======================================================
    if role in ["admin", "doctor", "midwife", "nurse"]:
        st.markdown("---")
        st.subheader("⚠️ Données cliniques vitales")
        col_vital1, col_vital2 = st.columns(2)
        with col_vital1:
            st.warning("🔒 Accès restreint : **Allergies et risques**")
            allergies = st.radio("Sélectionner la patiente:", ["Sarah", "Marie"])
            if allergies == "Sarah":
                with st.expander("Dossier d'allergies"):
                    st.error("**Allergies :** Pénicilline, arachides")
                    st.warning("**Risque :** Hypertension gestationnelle")
            elif allergies == "Marie":
                with st.expander("Dossier d'allergies"):
                    st.info("**Allergies :** Aucune connue")
                    st.warning("**Risque :** Diabète gestationnel")

        with col_vital2:
            st.success("🩸 **Informations d'urgence**")
            if st.button("Afficher les infos d'urgence"):
                st.info(
                    f"""
                **Groupe sanguin :** A+
                **Conditions :** Anémie
                **Contact d'urgence :** John (Conjoint) - 514-555-1234
                """
                )
                st.snow()

    # Le reste du contenu de la page d'accueil...

    # 🎒 Packs culturels
    st.markdown("---")
    st.subheader("🎒 Packs culturels")
    st.markdown(
        "Explore les récits, les chants et les savoirs transmis par les aînées."
    )

    # 👉 Carrousel HTML
    try:
        carousel_html = generate_carousel_html(fiches)
        components.html(carousel_html, height=450)
    except NameError:
        st.error("⚠️ Les données culturelles (fiches) ne sont pas disponibles.")
    except Exception as e:
        st.error(f"⚠️ Une erreur est survenue lors du chargement du carrousel : {e}")

    # 🪶 Poème d’introduction
    st.markdown(
        """
---
### *Ici commence le souffle du monde.*

Sous les couvertures de mousse et de ciel,
une mère crie enlace son enfant,
et le territoire écoute.

Les pleurs du nouveau-né ne sont pas des cris —
ce sont des chants anciens,
des appels au vent,
des promesses de racines.

Bienvenue là où la vie naît dans les bras du savoir,
où chaque battement de cœur est une mémoire,
où l’avenir se tisse dans le regard des femmes.
---
"""
    )

    # ======================================================
    # 🌦️ Météo en temps réel et prévisions
    # ======================================================
    st.markdown("---")
    st.subheader("🌦️ Météo des communautés")
    communities = {
        "Mistissini": (50.426, -73.882),
        "Chisasibi": (53.666, -78.792),
        "Waskaganish": (51.733, -78.757),
    }
    cols = st.columns(len(communities))
    for col, (name, coords) in zip(cols, communities.items()):
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
            col.error(f"Météo indisponible pour {name}")

    # ======================================================
    # 🗺️ Carte interactive
    # ======================================================
    st.markdown("---")
    st.subheader("🗺️ Carte des communautés")
    map = folium.Map(location=[51.5, -78.7], zoom_start=5)

    # Ajoute les marqueurs avec des pop-ups pour afficher les infos météo
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

    # ======================================================
    # 📅 Prochains rendez-vous
    # ======================================================
    st.markdown("---")
    st.subheader("📅 Prochains rendez-vous")
    st.info("Aucun rendez-vous planifié pour aujourd'hui.")

    # 🌤️ Météo locale en cri par communauté
    st.markdown("---")
    st.subheader("🌤️ Météo locale par communauté")
    communaute = st.selectbox(
        "Choisissez votre communauté :", ["Mistissini", "Waskaganish", "Chisasibi"]
    )
    coordonnees = {
        "Mistissini": (50.4184, -73.8693),
        "Waskaganish": (51.4800, -78.7500),
        "Chisasibi": (53.8050, -78.9167),
    }
    lat, lon = coordonnees.get(communaute, (50.4184, -73.8693))
    weather = get_current_weather(lat, lon)
    if weather:
        code = weather["weather_code"]


# --- CORRECTION: GESTION DE LA NAVIGATION EN FONCTION DE LA SESSION D'ÉTAT ---
# Si l'utilisateur est connecté, on affiche le menu et la page correspondante
if st.session_state.get("logged_in", False):
    afficher_menu(st.session_state["role"])

    # Rendu dynamique de la page sélectionnée
    if st.session_state["current_page"] == "home":
        render_home_page()
    else:
        # Importe et exécute la page sélectionnée de manière dynamique
        page_path = os.path.join(modules_dir, st.session_state["current_page"])
        if os.path.exists(page_path):
            try:
                # --- NOUVEAU: Message de débogage pour confirmer le chargement de la page ---
                st.info(f"Page chargée : **{st.session_state['current_page']}**")

                spec = importlib.util.spec_from_file_location("dynamic_page", page_path)
                dynamic_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(dynamic_module)
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement de la page : {e}")
        else:
            st.error(
                f"Le fichier de page '{st.session_state['current_page']}' est introuvable."
            )
            st.session_state["current_page"] = "home"
            st.rerun()
