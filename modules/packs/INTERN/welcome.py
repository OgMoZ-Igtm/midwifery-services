# BANNER_INJECTED
import streamlit as st
import requests
import os
import time
from PIL import Image
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import base64
from datetime import datetime

# =========================================================
# 🏠 VARIABLES ET RESSOURCES GLOBALES
# =========================================================

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Tempo en secondes pour l'auto-défilement
TEMPO = 5

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
        "image": os.path.join(
            script_dir, "..", "..", "static", "Grand_mere_et_enfant.png"
        ),
        "description": "👵 Les aînées partagent leur sagesse à travers les récits et les gestes.",
        "citation": "« Ce que tu apprends avec ton cœur, tu ne l’oublies jamais. »",
    },
    "Accueil sur le territoire": {
        "titre": "Accueil sur le territoire",
        "image": os.path.join(
            script_dir, "..", "..", "static", "Accueil_territoire.png"
        ),
        "description": "🌿 Le lien sacré avec la terre, les ancêtres et les esprits protecteurs.",
        "citation": "« Chaque pas sur cette terre est une prière. »",
    },
    "Maternité et continuité": {
        "titre": "Maternité et continuité",
        "image": os.path.join(script_dir, "..", "..", "static", "Mere_crie.png"),
        "description": "👩‍👧 La force des mères cries, gardiennes de la vie et de l’avenir.",
        "citation": "« Porter un enfant, c’est porter l’histoire de notre peuple. »",
    },
    "Le retour attendu": {
        "titre": "Le souffle de l'avenir",
        "image": os.path.join(
            script_dir, "..", "..", "static", "Le_retour_attendu.png"
        ),
        "description": "Deux jeunes mères partageant un moment de quiétude avec leurs nouveau-nés.",
        "citation": "« La vie que nous tenons dans nos bras est l'héritage de nos ancêtres et le futur de notre peuple. »",
    },
    "La transmission du savoir ancestral": {
        "titre": "La transmission du savoir ancestral",
        "image": os.path.join(
            script_dir, "..", "..", "static", "Tissage_et_transmission.png"
        ),
        "description": "Gestes et traditions qui relient la maternité à l'esprit de la terre.",
        "citation": "« Dans chaque pli de la peau d'une aînée se cachent les histoires qui protégeront le nouveau-né. »",
    },
    "Le berceau de la nature": {
        "titre": "Le berceau de la nature",
        "image": os.path.join(script_dir, "..", "..", "static", "Berceau_nature.png"),
        "description": "Dès leurs premiers instants, la nature est intégrée dans le soin des tout-petits.",
        "citation": "« Comme une graine dans la terre, notre bébé trouvera sa force dans le territoire. »",
    },
}

# Dictionnaire de mots de passe pour la démo
USER_PASSWORDS = {
    "MIDWIFE": "midwife",
    "ADMIN": "admin",
    "NURSE": "nurse",
    "DOCTOR": "doctor",
    "INTERN": "intern",
    "STUDENT": "student",
    "PATIENT": "patient",
    "DOCTORAL": "doctoral",
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


def render_page(role):
    # 🌟 Présentation du projet
    st.markdown("---")
    st.title("🏡 Bienvenue sur Midwifery-Data-COOL-Collection!")
    st.info(
        """
        Ce projet est une plateforme interactive pour aider les futures mamans, 
        les nouvelles mères et les professionnels de la santé à mieux gérer la grossesse 
        et les premiers mois de la vie de bébé. Naviguez à travers les menus pour accéder 
        à des ressources, des outils de suivi et des informations pertinentes.
        """
    )
    st.progress(100)  # Barre pleine instantanée

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
        temp = weather["temp"]
        wind = weather["wind"]
        icon = WEATHER_ICONS.get(code, "❔")
        cri = CREE_CONDITIONS.get(code, "Inconnu")

        # Le rôle est passé ici par la fonction de rendu
        if role == "INTERN":
            st.info(
                f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n🌾 À {communaute}, prévoyez vos déplacements pour les accouchements."
            )
        elif role == "PATIENT":
            st.info(
                f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n💖 À {communaute}, une météo douce pour une promenade avec bébé !"
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
    if role in ["MIDWIFE", "ADMIN", "DOCTOR", "NURSE"]:
        st.info("Statistiques professionnelles:")
        col1.metric("💉 Vaccination", "78%", "↑ 5%")
        col2.metric("🍼 Allaitement", "65%", "↔ Stable")
        col3.metric("⚠️ Complications", "12%", "↓ 2%")
    elif role == "PATIENT":
        st.info("Statistiques de suivi personnel:")
        col1.metric("❤️ Poids de bébé", "5,2 kg", "↑ 0,3 kg")
        col2.metric("💤 Heures de sommeil", "8h", "↔ Stable")
        col3.metric("🍏 Suivi nutritif", "Excellent", "↑")
    elif role in ["STUDENT", "INTERN", "DOCTORAL"]:
        st.info("Statistiques de recherche:")
        col1.metric("📄 Articles", "124", "↑ 20")
        col2.metric("📚 Études lues", "65", "↔ Stable")
        col3.metric("🔍 Thèmes explorés", "12", "↓ 2")
    else:
        st.info("Aucune statistique disponible pour ce rôle.")

    # ======================================================
    # 🔔 Notifications
    # ======================================================
    st.markdown("---")
    st.subheader("🔔 Notifications")
    if role in ["INTERN"]:
        st.warning("📨 Vous avez 2 messages non lus.")
        st.info("📅 Rappel : réunion avec l’équipe demain à 9h.")
    elif role == "PATIENT":
        st.warning("🔔 Le suivi de votre bébé est prêt.")
        st.info("💡 Nouveaux articles de blog sur l'allaitement.")
    else:
        st.info("Aucune notification pour ce rôle.")

    # ======================================================
    # 🎥 Vidéo explicative
    # ======================================================
    st.markdown("---")
    st.subheader("🎥 Vidéo explicative")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")


def lecteur_audio():
    audio_path = os.path.join(script_dir, "..", "..", "static", "bebe_pleure.mp3")
    if os.path.exists(audio_path):
        audio_base64 = image_to_base64(audio_path)
        st.markdown(
            f"""
            <audio id="bebeAudio" controls style="width:100%;">
                <source src="{audio_base64}" type="audio/mpeg">
                Votre navigateur ne supporte pas l'audio.
            </audio>
            <script>
                const audio = document.getElementById('bebeAudio');
                function toggleAudio() {{
                    if (audio.paused) {{
                        audio.play();
                    }} else {{
                        audio.pause();
                    }}
                }}
            </script>
            <div style='text-align:center; margin-top:10px;'>
                <button onclick="toggleAudio()" style='padding:8px 16px; font-size:16px;'>🔊 Activer / Désactiver le son</button>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Fichier audio 'bebe_pleure.mp3' introuvable.")


# =========================================================
# 🚀 POINT D'ENTRÉE DE L'APPLICATION
# =========================================================
st.set_page_config(page_title="🌾 Accueil INTERN", page_icon="🌾", layout="wide")

# Initialisation robuste de l'état de la session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = "INTERN"
if "user_name" not in st.session_state:
    st.session_state.user_name = "Intern"

if not st.session_state.authenticated:
    st.subheader("Connexion")
    with st.form(key="login_form"):
        user_name = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submit_button = st.form_submit_button(label="Se connecter")

        if submit_button:
            # Vérification du mot de passe
            valid_login = False
            lower_password = password.lower()
            for role, pw in USER_PASSWORDS.items():
                if lower_password == pw:
                    st.session_state.authenticated = True
                    st.session_state.user_role = role
                    st.session_state.user_name = user_name
                    valid_login = True
                    break

            if valid_login:
                st.success(
                    f"Connexion réussie en tant que **{st.session_state.user_role}** !"
                )
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")
else:
    # Affichage du contenu de la page si l'utilisateur est authentifié
    now = datetime.now()
    heure = now.hour
    date_connexion = now.strftime("%A %d %B %Y")
    heure_connexion = now.strftime("%H:%M")

    if heure < 12:
        salutation = "Bonjour"
    elif heure < 18:
        salutation = "Bon après-midi"
    else:
        salutation = "Bonsoir"

    st.markdown(
        f"""
    ### 👋 {salutation}, {st.session_state.user_name}
    Vous êtes connecté en tant que **{st.session_state.user_role}**
    🕒 Heure de connexion : **{heure_connexion}**
    📅 Date : **{date_connexion}**
    🗂️ Dernière connexion : *non enregistrée*
    """
    )

    # Afficher la page
    render_page(st.session_state.user_role)

    # Bouton de déconnexion
    if st.button("Se déconnecter"):
        st.session_state.authenticated = False
        st.session_state.user_role = "INTERN"
        st.session_state.user_name = "Intern"
        st.success("Déconnexion réussie.")
        st.rerun()

    # Afficher le lecteur audio
    try:
        lecteur_audio()
    except Exception as e:
        st.error(f"Une erreur est survenue lors du chargement du lecteur audio: {e}")
