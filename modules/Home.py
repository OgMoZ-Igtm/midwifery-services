# BANNER_INJECTED
import streamlit as st
from PIL import Image
import os
import requests
import time
from datetime import datetime
import pyttsx3  # À installer avec pip install pyttsx3

# from utils.logger import log_action, log_alert  # Imports commented out as files are not provided
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import base64


# =========================================================
# 🏠 VARIABLES ET RESSOURCES GLOBALES
# =========================================================

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Tempo en secondes pour l'auto-défilement
TEMPO = 5

# 📝 Dictionnaire de traduction (pour l'éditeur)
labels = {
    "fr": {
        "editor_title": "Éditeur de pages",
        "save_button": "Sauvegarder",
        "save_success": "Fichier sauvegardé avec succès !",
        "save_info": "Une sauvegarde a été créée",
        "save_error": "Erreur lors de la sauvegarde du fichier",
        "run_button": "Exécuter le code",
        "run_success": "Code exécuté avec succès !",
        "run_error": "Erreur lors de l'exécution du code",
        "file_not_found": "Le fichier menus.py est introuvable.",
    }
}
t = labels.get("fr")

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
    95: "Nipīhūn mīna yūtin",
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
        "image": os.path.join(script_dir, "..", "static", "Grand_mere_et_enfant.png"),
        "description": "👵 Les aînées partagent leur sagesse à travers les récits et les gestes.",
        "citation": "« Ce que tu apprends avec ton cœur, tu ne l’oublies jamais. »",
    },
    "Accueil sur le territoire": {
        "titre": "Accueil sur le territoire",
        "image": os.path.join(script_dir, "..", "static", "Accueil_territoire.png"),
        "description": "🌿 Le lien sacré avec la terre, les ancêtres et les esprits protecteurs.",
        "citation": "« Chaque pas sur cette terre est une prière. »",
    },
    "Maternité et continuité": {
        "titre": "Maternité et continuité",
        "image": os.path.join(script_dir, "..", "static", "Mere_crie.png"),
        "description": "👩‍👧 La force des mères cries, gardiennes de la vie et de l’avenir.",
        "citation": "« Porter un enfant, c’est porter l’histoire de notre peuple. »",
    },
    "Le retour attendu": {
        "titre": "Le souffle de l'avenir",
        "image": os.path.join(script_dir, "..", "static", "Le_retour_attendu.png"),
        "description": "Deux jeunes mères partageant un moment de quiétude avec leurs nouveau-nés.",
        "citation": "« La vie que nous tenons dans nos bras est l'héritage de nos ancêtres et le futur de notre peuple. »",
    },
    "La transmission du savoir ancestral": {
        "titre": "La transmission du savoir ancestral",
        "image": os.path.join(
            script_dir, "..", "static", "Tissage_et_transmission.png"
        ),
        "description": "Gestes et traditions qui relient la maternité à l'esprit de la terre. ",
        "citation": "« Dans chaque pli de la peau d'une aînée se cachent les histoires qui protégeront le nouveau-né. »",
    },
    "Le berceau de la nature": {
        "titre": "Le berceau de la nature",
        "image": os.path.join(script_dir, "..", "static", "Berceau_nature.png"),
        "description": "Dès leurs premiers instants, la nature est intégrée dans le soin des tout-petits.",
        "citation": "« Comme une graine dans la terre, notre bébé trouvera sa force dans le territoire. »",
    },
}

# =========================================================
# 🛠️ FONCTIONS UTILITAIRES
# =========================================================


def image_to_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = os.path.splitext(image_path)[1][1:]  # jpg, png, etc.
            return f"data:image/{ext};base64,{encoded}"
    else:
        st.error(f"Image introuvable: {image_path}")  # Added for debugging
        return None


def afficher_image_securisee(fiche):
    """Affiche une image si le chemin est valide, sinon affiche une alerte."""
    if "image" in fiche and os.path.exists(fiche["image"]):
        st.image(
            fiche["image"],
            caption=fiche.get("description", ""),
            use_container_width=True,
        )
    else:
        st.warning(f"⚠️ Image introuvable : {fiche.get('image', 'Non spécifié')}")


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


@st.cache_data
def get_forecast(lat, lon, days):
    """Récupère et met en cache les prévisions météo sur 3 jours."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days={days}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["daily"]
        forecasts = []
        for i in range(days):
            forecasts.append(
                {
                    "date": data["time"][i],
                    "weather_code": data["weather_code"][i],
                    "temp_max": data["temperature_2m_max"][i],
                    "temp_min": data["temperature_2m_min"][i],
                }
            )
        return forecasts
    except requests.exceptions.RequestException:
        return None


def login_form():
    """Affiche une interface de connexion simple."""
    st.title("Connexion")
    st.markdown("Veuillez entrer vos informations de connexion.")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")


if st.session_state.get("logged_in", False):
    st.title("Bienvenue, admin 👋")
    st.write("Vous êtes connecté.")
else:
    st.text_input("Nom d'utilisateur", key="username")
    st.text_input("Mot de passe", type="password", key="password")
    if st.button("Se connecter"):
        if (
            st.session_state.username == "admin"
            and st.session_state.password == "admin"
        ):
            st.session_state.logged_in = True
            st.success("Connexion réussie !")
            st.rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")


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
        }});
    </script>
    """
    return html_code


def render_audio_player():
    st.title("🔊 Lecteur audio interactif")
    st.write("Choisissez un son à écouter :")

    sons = {
        "👶 Bébé qui pleure": "utils/assets/bebe_pleure.mp3",
        "💓 Battement de cœur": "utils/assets/battement_coeur.mp3",
        "🗣️ Voix douce": "utils/assets/voix_douce.mp3",
    }

    choix = st.selectbox("Sélectionnez un son :", list(sons.keys()))

    # Correction : Utiliser st.audio() pour afficher le lecteur
    # Pas besoin de bouton, le widget st.audio() est interactif
    st.audio(sons[choix], format="audio/mp3")


# =========================================================
# 🖼️ PAGE D'APPLICATION PRINCIPALE
# =========================================================


def page_home():
    role = st.session_state.get("role", "GUEST").upper()
    st.title(f"🏠 Accueil {role}")

    if role == "MIDWIFE":
        st.success("👩‍⚕️ Suivi des patientes disponible.")

    elif role == "ADMIN":
        st.info("🔧 Accès complet à la configuration.")
        st.markdown(
            """
            Ce projet est une plateforme interactive pour aider les futures mamans,
            les nouvelles mères et les professionnels de la santé à mieux gérer la grossesse
            et les premiers mois de la vie de bébé.
            Naviguez à travers les menus pour accéder à des ressources, des outils de suivi
            et des informations pertinentes.
            """
        )

    else:
        st.warning(
            "🔒 Accès limité. Veuillez contacter l'administration pour plus d'autorisations."
        )

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
    folium.Marker([50.423, -73.857], tooltip="Mistissini").add_to(map)
    folium.Marker([53.8, -78.9], tooltip="Chisasibi").add_to(map)
    folium.Marker([51.5, -78.7], tooltip="Waskaganish").add_to(map)
    st_folium(map, width=700, height=400)

    # ======================================================
    # 📅 Prochains rendez-vous
    # ======================================================
    st.markdown("---")
    st.subheader("📅 Prochains rendez-vous")
    st.info("Aucun rendez-vous planifié pour aujourd'hui.")  # Placeholder

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
        temp = weather["temp"]
        wind = weather["wind"]
        icon = WEATHER_ICONS.get(code, "❔")
        cri = CREE_CONDITIONS.get(code, "Inconnu")
        role = st.session_state.get("role", "inconnu")

        if role == "Midwife":
            st.info(
                f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n🌾 À {communaute}, prévoyez vos déplacements pour les accouchements."
            )
        elif role == "Doctor":
            st.info(
                f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n🩺 À {communaute}, météo à surveiller pour les visites à domicile."
            )
        elif role == "Nurse":
            st.info(
                f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n💉 À {communaute}, la clinique mobile aura lieu sous {cri.lower()}."
            )
        elif role == "Patient":
            st.info(
                f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n🧑‍🍼 À {communaute}, météo prévue pour votre rendez-vous : {cri.lower()}."
            )
        else:
            st.warning("❓ Rôle non reconnu — météo affichée sans personnalisation.")
    else:
        st.error("Impossible de récupérer la météo.")

    # ======================================================
    # 📊 Statistiques rapides
    # ======================================================
    st.markdown("---")
    st.subheader("📊 Statistiques rapides")
    col1, col2, col3 = st.columns(3)
    col1.metric("💉 Vaccination", "78%", "↑ 5%")
    col2.metric("🍼 Allaitement", "65%", "↔ Stable")
    col3.metric("⚠️ Complications", "12%", "↓ 2%")

    # ======================================================
    # 🔔 Notifications
    # ======================================================
    st.markdown("---")
    st.subheader("🔔 Notifications")
    st.warning("📨 Vous avez 2 messages non lus.")
    st.info("📅 Rappel : réunion avec l’équipe demain à 9h.")

    # ======================================================
    # 🎥 Vidéo explicative
    # ======================================================
    st.markdown("---")
    st.subheader("🎥 Vidéo explicative")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")


# Logging
# ------------------------------------------------------
if st.session_state.get("authenticated", False):
    log_action(
        st.session_state.get("utilisateur", ["", "", ""])[2],
        st.session_state.get("role", "inconnu"),
        "Accès à la page Home",
    )


# =========================================================
# 🚀 POINT D'ENTRÉE DE L'APPLICATION
# =========================================================
if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Le code principal est maintenant dans des fonctions
    if st.session_state.logged_in:
        page_home()
    else:
        login_form()
