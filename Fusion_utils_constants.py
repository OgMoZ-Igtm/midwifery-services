import streamlit as st
import os
import time
import requests
import pandas as pd
import pydeck as pdk
import base64

# =========================================================
# 🏠 VARIABLES ET RESSOURCES GLOBALES (Consolidé de constants.py)
# =========================================================

# 📁 Répertoire racine du projet
script_dir = os.path.dirname(os.path.abspath(__file__))

# 🕒 Tempo en secondes pour l’auto-défilement des fiches (5 secondes)
TEMPO = 5

# 📍 Coordonnées géographiques des communautés cries
COMMUNITIES = {
    "Mistissini": (50.426, -73.882),
    "Chisasibi": (53.666, -78.792),
    "Waskaganish": (51.733, -78.757),
}

# 🌦️ Coordonnées météo (identiques ou légèrement ajustées)
WEATHER_COORDS = {
    "Mistissini": (50.4184, -73.8693),
    "Waskaganish": (51.4800, -78.7500),
    "Chisasibi": (53.8050, -78.9167),
}

# 🧠 Traduction cri des conditions météo (codes standardisés Open-Meteo)
CREE_CONDITIONS = {
    0: "Wāwīpān",  # Ciel clair
    1: "Mīna wāwīpān",  # Principalement clair
    2: "Mīna wāwīpān",  # Partiellement nuageux
    3: "Yūtin",  # Couvert
    45: "Wāpiskāw mīna yūtin",  # Brouillard
    48: "Wāpiskāw mīna yūtin",  # Brouillard givrant
    51: "Nipīhūn",  # Bruine légère
    61: "Nipīhūn",  # Pluie légère
    71: "Wāpiskāw",  # Neige légère
    80: "Nipīhūn mīna yūtin",  # Averses légères
    95: "Nipīhūn mīna yūtin",  # Orage (léger)
}

# 🌤️ Icônes météo associées aux codes
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


# 🧵 Fiches culturelles pour le carrousel d’accueil
CULTURAL_CARDS = {
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

# 🔐 Mots de passe pour les rôles (à sécuriser en production)
USER_PASSWORDS = {
    "MIDWIFE": "Test!1234@",
    "ADMIN": "Test!1234@",
    "NURSE": "Test!1234@",
    "DOCTOR": "Test!1234@",
    "INTERN": "Test!1234@",
    "STUDENT": "Test!1234@",
    "PATIENT": "Test!1234@",
    "DOCTORAL": "Test!1234@",
}


# =========================================================
# 📦 Fonctions utilitaires
# =========================================================


def load_static_asset(filename: str) -> str:
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    return os.path.join(static_dir, filename)


def play_audio(filename: str):
    path = load_static_asset(filename)
    try:
        with open(path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
    except FileNotFoundError:
        st.error(f"Fichier audio introuvable : {filename}")


def init_carrousel_state():
    if "carrousel_running" not in st.session_state:
        st.session_state.carrousel_running = True
    if "carrousel_index" not in st.session_state:
        st.session_state.carrousel_index = 0
    if "carrousel_last_run" in st.session_state:
        del st.session_state.carrousel_last_run


def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    return response.json().get("current_weather", {})


st.markdown(
    """
    <style>
    .fiche-card {
        background-color: #f8f8f8;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        animation: fadeSlide 1s ease-in-out;
    }
    @keyframes fadeSlide {
        0% { opacity: 0; transform: translateX(40px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    </style>
""",
    unsafe_allow_html=True,
)


def get_current_card():
    """Retourne la fiche culturelle actuelle selon l’index du carrousel."""
    if "carrousel_index" not in st.session_state:
        st.session_state.carrousel_index = 0
    # Utilise la constante CULTURAL_CARDS désormais globale
    cards = list(CULTURAL_CARDS.values())
    return cards[st.session_state.carrousel_index]


def render_carrousel_card():
    """Affiche la fiche culturelle actuelle avec animation visuelle."""
    current = get_current_card()

    st.markdown(
        """
        <style>
        .fiche-card {
            background-color: #f8f8f8;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            animation: fadeSlide 1s ease-in-out;
        }
        @keyframes fadeSlide {
            0% { opacity: 0; transform: translateX(40px); }
            100% { opacity: 1; transform: translateX(0); }
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='fiche-card'>", unsafe_allow_html=True)
    st.image(current["image"], use_column_width=True)
    st.markdown(f"### {current['titre']}")
    st.markdown(
        f"<p style='color:gray'>{current['description']}</p>", unsafe_allow_html=True
    )
    st.markdown(f"<p><i>{current['citation']}</i></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def get_fiches():
    """
    Conserve la signature de la fonction originale (contrainte de ne pas supprimer)
    et retourne les fiches culturelles définies dans la constante CULTURAL_CARDS.
    """
    # L'implémentation originale est remplacée pour utiliser la constante globale CULTURAL_CARDS
    # qui contient les données centralisées et les chemins d'accès corrects.
    return list(CULTURAL_CARDS.values())


# =========================================================
# 🎨 Couleurs météo par code
# =========================================================

WEATHER_COLORS = {
    0: "#fff9c4",  # ciel clair
    1: "#dcedc8",  # principalement clair
    2: "#c8e6c9",  # partiellement nuageux
    3: "#b2dfdb",  # nuageux
    45: "#b3e5fc",  # brouillard
    48: "#b3e5fc",  # brouillard givrant
    51: "#e1f5fe",  # bruine légère
    61: "#bbdefb",  # pluie légère
    71: "#e3f2fd",  # neige légère
    80: "#90caf9",  # averses
    95: "#f8bbd0",  # orage
}

# =========================================================
# 🧭 Barre publique
# =========================================================


def show_public_header():
    st.markdown(
        """
        <style>
        .public-header {
            background-color: #f0f4f8;
            padding: 12px 0;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            position: relative;
            z-index: 999;
        }
        .public-header a {
            margin: 0 15px;
            font-weight: 500;
            font-size: 16px;
            text-decoration: none;
            color: #333;
        }
        .public-header a:hover {
            color: #0077cc;
        }
        </style>
        <div class='public-header'>
            <a href='#' onclick="window.location.reload();">Notre mission</a>
            <a href='#' onclick="window.location.reload();">Notre vision</a>
            <a href='#' onclick="window.location.reload();">Qui sommes-nous</a>
            <a href='#' onclick="window.location.reload();">Les Papotines</a>
            <a href='#' onclick="window.location.reload();">Organisation</a>
            <a href='#' onclick="window.location.reload();">Liens utiles</a>
            <a href='#' onclick="window.location.reload();">Pour nous joindre</a>
            <a href='#' onclick="window.location.reload();">Infos</a>
            <a href='#' onclick="window.location.reload();">FAQ</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    menu_items = {
        "Notre mission": "🎯",
        "Notre vision": "🌈",
        "Qui sommes-nous": "🧑‍🤝‍🧑",
        "Les Papotines": "🧵",
        "Organisation": "🏢",
        "Liens utiles": "🔗",
        "Pour nous joindre": "📞",
        "Infos": "ℹ️",
        "FAQ": "❓",
    }

    cols = st.columns(len(menu_items))
    for i, (label, icon) in enumerate(menu_items.items()):
        with cols[i]:
            # Correction : Ajout de l'argument 'key' pour rendre chaque bouton unique.
            # Nous utilisons le 'label' comme clé unique.
            if st.button(f"{icon} {label}", key=label):
                st.session_state.info_page = label


# =========================================================
# 📄 Section dynamique selon info_page
# =========================================================


def render_info_section():
    section = st.session_state.get("info_page", None)
    if not section:
        return

    section_styles = {
        "Notre mission": {"icon": "🎯", "color": "#0077cc"},
        "Notre vision": {"icon": "🌈", "color": "#8e44ad"},
        "Qui sommes-nous": {"icon": "🧑‍🤝‍🧑", "color": "#2c3e50"},
        "Les Papotines": {"icon": "🧵", "color": "#d35400"},
        "Organisation": {"icon": "🏢", "color": "#16a085"},
        "Liens utiles": {"icon": "🔗", "color": "#2980b9"},
        "Pour nous joindre": {"icon": "📞", "color": "#c0392b"},
        "Infos": {"icon": "ℹ️", "color": "#34495e"},
        "FAQ": {"icon": "❓", "color": "#7f8c8d"},
    }

    content = {
        "Notre mission": "Nous accompagnons les familles cries avec respect, soin et transmission des savoirs.",
        "Notre vision": "Créer un espace de confiance où la maternité est honorée dans toutes ses dimensions.",
        "Qui sommes-nous": "Une équipe de sages-femmes, soignantes et membres de la communauté engagées pour le bien-être.",
        "Les Papotines": "Un mur d’expression libre pour les femmes : récits, poèmes, dessins, confidences.",
        "Organisation": "Notre structure repose sur la collaboration entre rôles, la transparence et la bienveillance.",
        "Liens utiles": "Accès rapide aux ressources locales, formulaires, guides et contacts essentiels.",
        "Pour nous joindre": "📞 Téléphone : 819-555-1234\n📧 Courriel : contact@msa.cri\n📍 Adresse : 12 rue du Partage, Mistissini",
        "Infos": "Informations pratiques sur les services, horaires, accompagnement et confidentialité.",
        "FAQ": "Réponses aux questions fréquentes sur l’accueil, les rôles, les droits et les suivis.",
    }

    # style = section_styles.get(section, {"icon": "📌", "color": "#555"})
    # icon = style["icon"]
    # color = style["color"]

    st.markdown("---")
    st.markdown(
        f"<h2 style='color:{color};'>{icon} {section}</h2>", unsafe_allow_html=True
    )
    # st.markdown(
    #     f"<p style='font-size: 1.1rem;'>{content.get(section, 'Contenu à venir…')}</p>",
    #     unsafe_allow_html=True,
    # )


# =========================================================
# 🏠 Page d’accueil publique
# =========================================================


def render_home_page():
    if "carrousel_last_run" in st.session_state:
        del st.session_state.carrousel_last_run

    show_public_header()

    if st.session_state.get("audio_running", True):
        # NOTE: L'audio 'bebe_pleure.mp3' est supposé exister dans le répertoire 'static'.
        # Si vous ne voulez pas que l'audio joue en boucle, vous pouvez le commenter
        # play_audio("bebe_pleure.mp3")
        pass

    render_info_section()

    st.markdown(
        """
        <style>
        .weather-card {
            background-color: #f9f9f9;
            padding: 10px 16px;
            margin-bottom: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            animation: fadeInWeather 1s ease-in-out;
        }
        @keyframes fadeInWeather {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### ☀️ Météo dans les communautés")
    # Utilise WEATHER_COORDS pour l'itération (Mistissini, Waskaganish, Chisasibi)
    for name, (lat, lon) in WEATHER_COORDS.items():
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url)
            weather = response.json().get("current_weather", {})
            if weather:
                code = weather.get("weathercode", 0)
                icon = WEATHER_ICONS.get(code, "")
                cri = CREE_CONDITIONS.get(code, "—")
                temp = weather.get("temperature", "?")
                wind = weather.get("windspeed", "?")
                bg = WEATHER_COLORS.get(code, "#f0f0f0")
                st.markdown(
                    f"""<div class='weather-card' style='background-color:{bg};'>
                        <b>{name}</b> {icon} {cri} — {temp}°C, vent {wind} km/h
                    </div>""",
                    unsafe_allow_html=True,
                )
        except Exception:
            # st.warning(f"Impossible de récupérer la météo pour {name}")
            # Silencier l'erreur pour une meilleure expérience utilisateur si l'API est lente
            pass

    st.markdown("### 🗺️ Carte des communautés")
    # Utilise COMMUNITIES pour la carte
    df = pd.DataFrame(
        [{"Nom": k, "lat": v[0], "lon": v[1]} for k, v in COMMUNITIES.items()]
    )
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(latitude=52.0, longitude=-76.0, zoom=4),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position="[lon, lat]",
                    get_color="[255, 0, 0, 160]",
                    get_radius=50000,
                ),
                pdk.Layer(
                    "TextLayer",
                    data=df,
                    get_position="[lon, lat]",
                    get_text="Nom",
                    get_size=16,
                    get_color=[255, 0, 0],
                ),
            ],
        )
    )
