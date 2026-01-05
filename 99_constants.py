import os
import streamlit as st
import pandas as pd

# =========================================================
# 🏠 VARIABLES ET RESSOURCES GLOBALES
# =========================================================

# 📁 Répertoire racine du projet
script_dir = os.path.dirname(os.path.abspath(__file__))

# 🕒 Tempo en secondes pour l’auto-défilement des fiches
TEMPO = 5

# 🌍 Communautés cries
COMMUNITIES = pd.DataFrame(
    [
        {
            "Nom": "Waskaganish",
            "lat": 51.4833,
            "lon": -78.75,
            "color": "#A7D8DE",
            "icon": "🌿",
            "legend": "Là où les rivières chantent les berceuses des ancêtres.",
            "legend_cr": "ᐊᐧᐋᐦᑖ ᓂᔭᐦᑖᐤ",
        },
        {
            "Nom": "Mistissini",
            "lat": 50.4183,
            "lon": -73.869,
            "color": "#FDE2B9",
            "icon": "🔥",
            "legend": "Le feu sacré veille sur les rêves des enfants.",
            "legend_cr": "ᐱᐦᑯᓯᒫᐦᑖ ᓂᔭᐦᑖᐤ",
        },
        {
            "Nom": "Chisasibi",
            "lat": 53.7833,
            "lon": -78.8958,
            "color": "#D3C0F9",
            "icon": "🌌",
            "legend": "Sous le ciel étoilé, les histoires prennent vie.",
            "legend_cr": "ᓂᐦᑖᐧᐃᓐ ᐋᐧᐱᐦᑖᐤ",
        },
    ]
)

# 🌦️ Coordonnées météo officielles
WEATHER_COORDS = {
    "Mistissini": (51.5275, -73.6789),
    "Waskaganish": (51.4833, -78.75),
    "Chisasibi": (53.8057, -78.9166),
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

# 🌦️ Légendes météo poétiques — Français
WEATHER_LEGENDS_FR = {
    0: "Le ciel clair est une bénédiction des ancêtres.",
    1: "La lumière filtre doucement, comme une caresse sur le territoire.",
    2: "Les nuages dansent, porteurs de récits anciens.",
    3: "Le ciel se voile, mais la terre reste attentive.",
    45: "Le brouillard murmure les secrets du territoire.",
    48: "Le givre suspend le temps, comme une mémoire figée.",
    51: "La bruine est une berceuse pour les esprits.",
    61: "La pluie légère nettoie les pensées et les chemins.",
    71: "La neige douce enveloppe les rêves des nouveau-nés.",
    80: "Les averses chantent la force du ciel.",
    95: "L’orage rappelle que la nature parle fort quand elle protège.",
}

# 🌦️ Légendes météo poétiques — Cri
WEATHER_LEGENDS_CR = {
    0: "Wāwīpān kāh-kīyānāw āpīchikēwin.",
    1: "Wāwīpān kāh-kīyānāw kāpīpīchikēwin.",
    2: "Yūtin kāh-kīyānāw kāpīpīchikēwin.",
    3: "Yūtin kāh-kīyānāw kākīwēw.",
    45: "Wāpiskāw kāh-kīyānāw kāpīchikēwin.",
    48: "Wāpiskāw kāh-kīyānāw kāpīchikēwin kāpīwēw.",
    51: "Nipīhūn kāh-kīyānāw kāpīchikēwin.",
    61: "Nipīhūn kāh-kīyānāw kāpīchikēwin.",
    71: "Wāpiskāw kāh-kīyānāw kāpīchikēwin.",
    80: "Nipīhūn mīna yūtin kāh-kīyānāw kāpīchikēwin.",
    95: "Nipīhūn mīna yūtin kāh-kīyānāw kāpīchikēwin kāpīwēw.",
}

# 🌦️ Légendes météo poétiques — Anglais
WEATHER_LEGENDS_EN = {
    0: "Clear skies are a blessing from the ancestors.",
    1: "Light filters gently, like a caress on the land.",
    2: "Clouds dance, carrying ancient stories.",
    3: "The sky veils itself, but the earth remains attentive.",
    45: "The fog whispers the secrets of the territory.",
    48: "Frost suspends time, like a frozen memory.",
    51: "The drizzle is a lullaby for the spirits.",
    61: "Light rain cleanses thoughts and paths.",
    71: "Soft snow wraps the dreams of newborns.",
    80: "Showers sing the strength of the sky.",
    95: "Thunder reminds us that nature speaks loudly when it protects.",
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


# 🧵 Fiches culturelles pour le carrousel
def get_cultural_cards():
    return [
        {
            "file": "Accueil_territoire.png",
            "title": "Accueil sur le territoire",
            "description": "Le lien sacré avec la terre, les ancêtres et les esprits protecteurs.",
            "citation": "« Chaque pas sur cette terre est une prière. »",
            "icon": "🪶",  # territoire et spiritualité
        },
        {
            "file": "Grand_mere_et_enfant.png",
            "title": "Transmission des savoirs",
            "description": "Les aînées partagent leur sagesse à travers les récits et les gestes.",
            "citation": "« Ce que tu apprends avec ton cœur, tu ne l’oublies jamais. »",
            "icon": "📚",  # transmission et apprentissage
        },
        {
            "file": "Berceau_nature.png",
            "title": "Le berceau de la nature",
            "description": "La terre comme première gardienne.",
            "citation": "« Là où pousse la mousse, naît la mémoire. »",
            "icon": "🌱",  # nature et naissance
        },
        {
            "file": "Mere_crie.png",
            "title": "Maternité et continuité",
            "description": "La force des mères cries, gardiennes de la vie et de l’avenir.",
            "citation": "« Porter la vie, c’est porter l’histoire. »",
            "icon": "🤱",  # maternité
        },
        {
            "file": "Le_retour_attendu.png",
            "title": "Le souffle de l'avenir",
            "description": "Deux jeunes mères partageant un moment de quiétude avec leurs nouveau-nés.",
            "citation": "« Le silence partagé est parfois le plus grand des chants. »",
            "icon": "👶",  # nouveau-nés et avenir
        },
        {
            "file": "Tissage_et_transmission.png",
            "title": "La transmission du savoir ancestral",
            "description": "Gestes et traditions qui relient la maternité à l'esprit de la terre.",
            "citation": "« Chaque fil tissé relie une génération à l’autre. »",
            "icon": "🧵",  # tissage et tradition
        },
    ]


def load_static_asset(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "static", filename)


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


if st.session_state.get("authenticated"):
    role = st.session_state["role"]

    # 🔊 Lecture automatique du son
    if st.session_state.get("audio_running", False):
        play_audio("bebe_pleure.mp3")

    # 🔊 Indicateur visuel
    st.markdown(f"""
        <div style="text-align:center; font-size:18px; margin-top:10px;">
            {"🔊 Le son est actif" if st.session_state.audio_running else "🔇 Le son est en pause"}
        </div>
    """, unsafe_allow_html=True)

    # 🎚️ Sélecteur de volume symbolique
    volume_icon = st.select_slider(
        "Niveau du son",
        options=["🔈", "🔉", "🔊"],
        value=st.session_state.get("audio_level", "🔊")
    )
    st.session_state.audio_level = volume_icon

    st.markdown(f"""
        <div style="text-align:center; font-size:22px; margin-top:10px;">
            Volume sélectionné : {volume_icon}
        </div>
    """, unsafe_allow_html=True)

    # 🎛️ Boutons de contrôle audio
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏸️ Couper le son"):
            st.session_state.audio_running = False
    with col2:
        if st.button(f"{volume_icon} Reprendre le son"):
            st.session_state.audio_running = True
