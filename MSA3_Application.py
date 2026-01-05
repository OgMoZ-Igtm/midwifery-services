# 🌿 Imports fondamentaux
import streamlit as st
import time
import os
import base64
import importlib
import requests
import folium
from streamlit_folium import st_folium

# 📦 Registres des formulaires
from modules.public.form_registry import (
    LINKED_FORMS_EXTENDED,
    SHARED_FORMS_REGISTRY,
    PUBLIC_FORMS_REGISTRY,
)

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

    last_sess = st.session_state.get("last_session", {})
    if last_sess.get("start") and last_sess.get("end"):
        start_dt = time.localtime(last_sess["start"])
        end_dt = time.localtime(last_sess["end"])
        st.markdown("---")
        st.markdown(f"**Dernière Session ({last_sess['role'].capitalize()})**:")
        st.markdown(f"Déb. : {time.strftime('%Y-%m-%d %H:%M:%S', start_dt)}")
        st.markdown(f"Fin : {time.strftime('%Y-%m-%d %H:%M:%S', end_dt)}")

    st.markdown("---")
    st.session_state["main_section_auth"] = st.radio(
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

    st.markdown("---")
    if st.button("🚪 Déconnexion"):
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
    st.title("🌸 Bienvenue dans l’espace de la maïeutique numérique")
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
    st.title(f"📊 Tableau de bord : {role}")
    load_dashboard(role)

# 📂 FORMULAIRES SPÉCIFIQUES
elif section == "Formulaires spécifiques":
    st.title("📂 Formulaires spécifiques")
    for key, config in LINKED_FORMS_EXTENDED.items():
        if config["role"] == role or role in config.get("roles_allowed", []):
            label = config.get("title", key)
            if st.button(f"📄 {label}", key=key):
                load_form(config["module"])

# 🌐 FONCTIONS PARTAGÉES
elif section == "Fonction partagée":
    st.title("🌐 Fonctions partagées")
    for key, config in SHARED_FORMS_REGISTRY.items():
        label = config.get("title", key)
        if st.button(f"🔗 {label}", key=key):
            load_form(config["module"])

# 🧵 WORKSHOPS
elif section == "Workshops":
    st.title("🧵 Ateliers & Carrousels")
    st.markdown("Voici le carrousel `render_generate_bebe-carrousel`")
    load_form("modules.shared.form_carrousel_bebe")

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

st.toast("🌿 Vous avez quitté votre espace avec succès !", icon="🕊️")
