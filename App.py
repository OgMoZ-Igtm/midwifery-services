# =========================================================
# 📦 FICHIER UNIQUE : MATERNITÉ CRIE APP - RÉORGANISÉ ET FIXÉ
# =========================================================

# ---------------------------------------------------------
# 1. CONFIGURATION, IMPORTS ET ENVIRONNEMENT
# ---------------------------------------------------------

import streamlit as st
import importlib
import requests
import pandas as pd
import pydeck as pdk
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from modules.backend.supabase_client import supabase

# Configuration de la page doit être la première commande Streamlit
st.set_page_config(page_title="Plateforme Maternité Crie", layout="wide")

# Chargement des variables d'environnement
load_dotenv()


# ---------------------------------------------------------
# 2. MOCKS & CONSTANTES SIMULÉES (DATA & PLACEHOLDERS)
# ---------------------------------------------------------

# --- MOCK: USER_PASSWORDS (Simule l'import de constants.py)
# FIX 3: Correction du nom de la variable
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
# Liste des rôles pour la selectbox de test
ALL_ROLES = list(USER_PASSWORDS.keys())


# --- MOCK: COMMUNITIES (Simule l'import de constants.py)
# Les coordonnées sont approximatives pour l'affichage de la carte
data_communities = {
    "Nom": ["Wemindji", "Chisasibi", "Mistissini"],
    "lat": [53.00, 53.80, 50.30],
    "lon": [-75.80, -78.80, -70.90],
    "color": ["#F8BBD0", "#C8E6C9", "#BBDEFB"],
    "icon": ["🏠", "🛶", "🌲"],
    "legend_cr": ["ᐅᐧᐋᐦᑖ", "ᐊᐱᔥᑯᓯᐤ", "ᓂᔭᐦᑖᐤ"],
}
COMMUNITIES = pd.DataFrame(data_communities)

# --- MOCK: DONNÉES METEO (Simule l'import de constants.py)
WEATHER_COLORS = {
    0: "#fff9c4",
    1: "#dcedc8",
    2: "#c8e6c9",
    3: "#b2dfdb",
    45: "#b3e5fc",
    48: "#b3e5fc",
    51: "#e1f5fe",
    61: "#bbdefb",
    71: "#e3f2fd",
    80: "#90caf9",
    95: "#f8bbd0",
}
WEATHER_LEGENDS_FR = {
    0: "Ciel clair.",
    1: "Principalement clair.",
    3: "Nuageux.",
    71: "Neige légère.",
}
WEATHER_LEGENDS_CR = {0: "ᑖᐧᐋᐦᑖᐤ.", 1: "ᐊᐧᐱᐦᑖᐤ.", 3: "ᓂᔭᐦᑖᐤ.", 71: "ᐃᔨᔨᐤ."}
CREE_CONDITIONS = {0: "Wâsow", 71: "Konas"}

TEMPO = 6  # Temps d'attente pour le carrousel

# --- FIX 4: Mappage des fiches culturelles par rôle ---
CULTURAL_CARD_ROLES = {
    # Indices des cartes dans la liste retournée par get_cultural_cards()
    "PATIENT": [
        0,
        2,
        3,
        4,
    ],  # Accueil territoire, Berceau nature, Maternité, Le retour attendu
    "MIDWIFE": [
        0,
        1,
        3,
        5,
    ],  # Accueil territoire, Transmission savoirs, Maternité, Tissage et transmission
    "NURSE": [1, 3, 4],  # Transmission savoirs, Maternité, Le retour attendu
    "DOCTOR": [1, 5],  # Transmission savoirs, Tissage et transmission
    "INTERN": [0, 1, 5],
    "STUDENT": [1, 5],
    "DOCTORAL": [1, 5],
    "ADMIN": [0, 1, 2, 3, 4, 5],
    "DEFAULT": [0, 1, 2, 3, 4, 5],  # Pour PUBLIC et autres rôles
}


# ---------------------------------------------------------
# 3. FONCTIONS UTILITAIRES DE BASE (NON-UI / DONNÉES)
# ---------------------------------------------------------

# FIX 1: Suppression du bloc d'audio global et de la fonction play_audio
# L'audio est maintenant géré par injection JS dans le dashboard


def get_cultural_cards():
    """Fiches culturelles pour le carrousel."""
    return [
        {
            "file": "/static/Accueil_territoire.png",
            "title": "Accueil sur le territoire",
            "description": "Le lien sacré avec la terre, les ancêtres et les esprits protecteurs.",
            "citation": "« Chaque pas sur cette terre est une prière. »",
            "icon": "🪶",  # territoire et spiritualité
        },
        {
            "file": "static/Grand_mere_et_enfant.png",
            "title": "Transmission des savoirs",
            "description": "Les aînées partagent leur sagesse à travers les récits et les gestes.",
            "citation": "« Ce que tu apprends avec ton cœur, tu ne l’oublies jamais. »",
            "icon": "📚",  # transmission et apprentissage
        },
        {
            "file": "static/Berceau_nature.png",
            "title": "Le berceau de la nature",
            "description": "La terre comme première gardienne.",
            "citation": "« Là où pousse la mousse, naît la mémoire. »",
            "icon": "🌱",  # nature et naissance
        },
        {
            "file": "static/Mere_crie.png",
            "title": "Maternité et continuité",
            "description": "La force des mères cries, gardiennes de la vie et de l’avenir.",
            "citation": "« Porter la vie, c’est porter l’histoire. »",
            "icon": "🤱",  # maternité
        },
        {
            "file": "static/Le_retour_attendu.png",
            "title": "Le souffle de l'avenir",
            "description": "Deux jeunes mères partageant un moment de quiétude avec leurs nouveau-nés.",
            "citation": "« Le silence partagé est parfois le plus grand des chants. »",
            "icon": "👶",  # nouveau-nés et avenir
        },
        {
            "file": "static/Tissage_et_transmission.png",
            "title": "La transmission du savoir ancestral",
            "description": "Gestes et traditions qui relient la maternité à l'esprit de la terre.",
            "citation": "« Chaque fil tissé relie une génération à l’autre. »",
            "icon": "🧵",  # tissage et tradition
        },
    ]


def load_static_asset(filename: str) -> str:
    """
    Retourne le chemin relatif de l'asset statique pour l'affichage.
    Les fichiers sont censés être dans le dossier 'static/' à la racine.
    FIX 1: Retourne le chemin réel au lieu d'un placeholder URL.
    """
    return f"static/{filename}"


def validate_project(username, password):
    """Simule la validation des identifiants."""
    # Correction: Utilisation de USER_PASSWORDS
    st.session_state["role"] = username.upper().replace(" ", "")
    return (
        USER_PASSWORDS.get(username.upper()) == password
    )  # Assure que la clé est en majuscule


def get_time_period():
    """Détermine la période de la journée (matin, après-midi, soir, nuit)."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "matin"
    elif 12 <= hour < 18:
        return "après-midi"
    elif 18 <= hour < 22:
        return "soir"
    else:
        return "nuit"


def get_weather(lat, lon):
    """Récupère les données météo actuelles pour des coordonnées données."""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url, timeout=TEMPO)  # Utilise la variable TEMPO
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        weather_data = response.json().get("current_weather", {})
        if not weather_data:
            return {
                "temperature": 15,
                "windspeed": 10,
                "weathercode": 3,
            }  # Simule nuageux (code 3)
        return weather_data
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Erreur lors de la récupération de la météo pour ({lat}, {lon}): {e}")
        return {
            "temperature": 12,
            "windspeed": 8,
            "weathercode": 71,  # Simule une légère neige (code 71)
        }


def get_weather_legend(code, lang="Français"):
    """Retourne la légende météo selon le code et la langue."""
    if lang == "Français":
        return WEATHER_LEGENDS_FR.get(code, "Le ciel nous parle, écoutons-le.")
    elif lang == "Cri":
        return WEATHER_LEGENDS_CR.get(code, "ᐃᔨᔨᐤ ᐊᓂᔑᓈᐤ ᐊᐱᔥᑯᓯᐤ.")
    else:
        return WEATHER_LEGENDS_FR.get(code, "The sky speaks, let us listen.")


# ---------------------------------------------------------
# 4. RENDU DES COMPOSANTS UI (Éléments réutilisables)
# ---------------------------------------------------------

# Global CSS pour le carrousel (Meilleure pratique)
st.markdown(
    """
    <style>
    /* CSS pour le Carrousel Dynamique (FIX 4) */
    .cultural-card-single {
        background-color: #f7f3f9;
        border-radius: 16px;
        padding: 25px;
        min-height: 350px; 
        box-shadow: 0 8px 20px rgba(186, 104, 200, 0.2);
        border: 2px solid #ba68c8;
        text-align: center;
        animation: fadeIn 1s;
        transition: all 0.5s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0.2; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .cultural-icon-single {
        font-size: 3.5rem;
        margin-bottom: 15px;
    }
    .cultural-citation-single {
        font-style: italic;
        color: #7d4f3b;
        margin-top: 15px;
        border-top: 1px dashed #e0c0a6;
        padding-top: 10px;
        font-size: 1.1em;
    }
    .card-image {
        width: 100%;
        max-height: 150px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #ddd;
    }
    /* Styles pour le FIX Météo (Assurer la clarté) */
    .weather-card h3 {
        color: #7d4f3b !important;
    }
    .cree-legend {
        color: #ba68c8 !important;
    }
    /* Styles pour le menu sidebar */
    .sidebar .stRadio > label {
        display: flex;
        align-items: center;
        padding: 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_cultural_carrousel(role):
    """FIX 4: Affiche une seule fiche culturelle dynamique en fonction du rôle."""
    st.markdown("### ✨ Fiches culturelles sur l'Eeyou Istchee (Carrousel)")

    # 1. Filtrage par rôle
    all_cards = get_cultural_cards()
    role_cards_indices = CULTURAL_CARD_ROLES.get(role, CULTURAL_CARD_ROLES["DEFAULT"])
    cards = [all_cards[i] for i in role_cards_indices]

    if not cards:
        st.info("Aucune fiche culturelle pertinente disponible pour votre rôle.")
        return

    # 2. Logique de cycle dynamique (Utilisation de st.session_state pour l'index)
    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0

    # Calcule l'index actuel
    current_index = st.session_state.carousel_index % len(cards)
    card = cards[current_index]

    # Crée un placeholder pour la carte (nécessaire si on voulait mettre à jour sans rerender,
    # mais Streamlit nécessite un rerender complet ici)
    card_placeholder = st.empty()

    # Rendu de la carte unique
    with card_placeholder:
        # FIX 1: Utilisation du chemin statique correct pour l'image
        image_url = load_static_asset(card["file"])

        st.markdown(
            f"""
            <div class='cultural-card-single'>
                <img src='{image_url}' class='card-image' alt='{card["title"]}'/>
                <div class='cultural-icon-single'>{card["icon"]}</div>
                <h3 style='color:#ba68c8; margin-top:0;'>{card["title"]}</h3>
                <p style='font-size:1em; font-weight: 500;'>{card["description"]}</p>
                <div class='cultural-citation-single'>"{card["citation"]}"</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. Mécanisme de Rerun pour le cycle (Toutes les 6 secondes)
    time.sleep(TEMPO)
    st.session_state.carousel_index += 1
    # Force le rerender pour afficher la carte suivante
    st.rerun()


def render_weather_card(name, weather):
    """Rend la carte météo pour une seule communauté. (FIX 2: Styles revus)"""
    code = weather.get("weathercode", 0)
    temp = weather.get("temperature", "?")
    wind = weather.get("windspeed", "?")

    # Détermination du style (simulé)
    bg = WEATHER_COLORS.get(code, "#f0f0f0")
    community_data = COMMUNITIES[COMMUNITIES["Nom"] == name]
    if community_data.empty:
        legend_cr = "N/A"
        icon_emoji = "❓"
    else:
        legend_cr = community_data["legend_cr"].iloc[0]
        icon_emoji = community_data["icon"].iloc[0]

    period = get_time_period()
    PERIOD_GRADIENTS = {
        "matin": "linear-gradient(to bottom, #e3f2fd, #fff)",
        "après-midi": "linear-gradient(to bottom, #fffde7, #fff)",
        "soir": "linear-gradient(to bottom, #ede7f6, #fff)",
        "nuit": "linear-gradient(to bottom, #263238, #37474f)",
    }
    bg_gradient = PERIOD_GRADIENTS.get(period, "#fff")

    lang = st.session_state.get("weather_lang", "Français")
    legend = get_weather_legend(code, lang=lang)

    # Détection du type météo pour l'ombre
    weather_type = "default"
    if code in [0, 1]:
        weather_type = "clear"
    elif code in [71, 73, 75]:
        weather_type = "snow"
    elif code in [61, 63, 65]:
        weather_type = "rain"
    elif code in [2, 3]:
        weather_type = "cloud"

    WEATHER_SHADOWS = {
        "clear": "0 0 12px rgba(144,202,249,0.4)",
        "snow": "0 0 12px rgba(255,255,255,0.5)",
        "rain": "0 0 12px rgba(120,144,156,0.4)",
        "cloud": "0 0 12px rgba(200,200,200,0.3)",
        "default": "0 0 8px rgba(186,104,200,0.3)",
    }
    shadow = WEATHER_SHADOWS.get(weather_type)

    animated_icon = {
        "clear": "☀️",
        "snow": "❄️",
        "rain": "🌧️",
        "cloud": "☁️",
        "default": "🌤️",
    }.get(weather_type, "🌤️")

    # Injection du style
    st.markdown(
        f"""
        <div style='text-align:center; margin-bottom:-10px; font-size:40px;
                     animation: floatPlume 3s ease-in-out infinite;'>{animated_icon}</div>
        <style>
        @keyframes floatPlume {{
            0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0px); }}
        }}
        </style>
        <div class='weather-card' style='
            background: {bg_gradient}; background-color: {bg}; padding: 1em;
            border-radius: 12px; margin-bottom: 1em;
            transition: background-color 0.5s ease; box-shadow: {shadow};'>

            <h3 style='margin-bottom:0.2em;'>{icon_emoji} {name}</h3>
            <p style='font-size:18px; margin:0.2em 0;'>
                <strong>{temp}°C</strong>, vent {wind} km/h
            </p>
            <p style='font-style:italic; color:#444;'>{legend}</p>
            <div class='cree-legend' style='margin-top:0.5em; font-weight:bold;'>
                🧠 {legend_cr}
            </div>
            <div style='margin-top:0.3em; color:#1e88e5; font-family:Georgia, serif; font-size:1.1rem;'>
                <i>{CREE_CONDITIONS.get(code, "")}</i>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_weather_for_all():
    """Rend la section météo pour toutes les communautés avec carte interactive. (FIX 2: Titres et carte clairs)"""
    st.markdown("## ☀️ Météo actuelle dans les communautés de l'Eeyou Istchee")

    cols = st.columns(3)
    col_index = 0

    # Utilisation de la DataFrame mockée
    for row in COMMUNITIES.itertuples():
        with cols[col_index % 3]:
            weather = get_weather(row.lat, row.lon)
            if weather:
                render_weather_card(row.Nom, weather)
            else:
                st.warning(f"Impossible de récupérer la météo pour {row.Nom}")
        col_index += 1

    # 🗺️ Carte interactive
    st.markdown("## 🗺️ Visualisation des communautés")
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=52.0,
                longitude=-76.0,
                zoom=4,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=COMMUNITIES,
                    get_position="[lon, lat]",
                    get_color="[186, 104, 200, 160]",
                    get_radius=50000,
                    pickable=True,
                ),
                pdk.Layer(
                    "TextLayer",
                    data=COMMUNITIES,
                    get_position="[lon, lat]",
                    get_text="Nom",
                    get_size=16,
                    get_color=[186, 104, 200],
                    get_alignment_baseline="'bottom'",
                ),
            ],
        )
    )

    lang = st.selectbox(
        "🌐 Choisir la langue d’affichage",
        ["Français", "Cri", "Anglais"],
        index=0,
        help="Affiche les légendes météo dans la langue choisie",
        key="weather_lang_selectbox",
    )
    st.session_state.weather_lang = lang


def show_public_header():
    """Affiche l'en-tête de navigation horizontal et fixe."""
    themes = {
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

    # Ajout des styles pour le header
    st.markdown(
        """
        <style>
        .nav-bar {
            position: fixed; top: 0; left: 0; right: 0;
            background-color: #fff8f0; padding: 10px 20px;
            display: flex; gap: 12px; justify-content: center;
            border-bottom: 2px solid #f0e0d6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05); z-index: 9999;
        }
        .nav-bar a {
            text-decoration: none; color: #333; font-weight: 600;
            font-size: 0.9rem; padding: 8px 14px; border-radius: 8px;
            transition: background-color 0.3s, color 0.3s;
            display: flex; align-items: center; white-space: nowrap;
        }
        .nav-bar a:hover {
            background-color: #f0e0d6; color: #7d4f3b;
        }
        .nav-bar a.active-link {
            background-color: #ba68c8; color: white; font-weight: 700;
            box-shadow: 0 2px 5px rgba(186,104,200,0.5);
        }
        </style>
        <div class='nav-bar'>
        """,
        unsafe_allow_html=True,
    )

    # Récupère la page active de la session
    active_page = st.session_state.get("info_page", "Notre mission")

    # Création des liens cliquables
    for label, icon in themes.items():
        # Utilisation d'un bouton Streamlit caché via CSS/JS pour simuler la navigation
        # et s'assurer que l'état Streamlit est mis à jour
        is_active = " active-link" if label == active_page else ""

        # Ce markdown simule un lien et met à jour l'état de la session Streamlit via JS (si le JS est permis)
        # Sinon, l'utilisation de st.button/form est plus fiable, mais la structure en barre de navigation est préférée.
        st.markdown(
            f"""
            <a href='#' 
                id='nav_{label.replace(" ", "_")}' 
                class='{is_active}' 
                onclick='
                    // Envoie un événement pour mettre à jour l'état de la session Streamlit
                    window.parent.postMessage({{
                        type: 'streamlit:setSessionState', 
                        state: {{ info_page: "{label}" }}
                    }}, "*");
                    // Nécessite un rerender pour que Streamlit prenne en compte l'état
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        componentId: 'rerender_trigger', // Un ID bidon pour forcer
                        value: Math.random()
                    }}, "*");
                '
            >
                {icon} {label}
            </a>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    # Espace pour le contenu principal
    st.markdown(
        "<div style='padding-top: 5rem;'>", unsafe_allow_html=True
    )  # Pour compenser le header fixe
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# 5. RENDU DES PAGES COMPLÈTES (Vues principales)
# ---------------------------------------------------------


def render_info_section():
    """Rend le contenu dynamique de la section d'information publique."""
    if "info_page" not in st.session_state:
        st.session_state["info_page"] = "Notre mission"

    current_page = st.session_state["info_page"]

    st.markdown(
        f"<a name='{current_page.replace(' ', '_')}'></a>", unsafe_allow_html=True
    )
    st.markdown(f"## {current_page}", unsafe_allow_html=True)

    # Contenu générique pour la démo
    if current_page == "Notre mission":
        st.write(
            "Notre mission est de tisser des liens solides entre les soins de maternité et la richesse culturelle crie, assurant une expérience de naissance empreinte de respect et de dignité."
        )
        # L'image utilisera maintenant le chemin correct 'static/mission.png'
        st.image(load_static_asset("mission.png"))
    elif current_page == "Les Papotines":
        st.write(
            "Le fil des Papotines, c'est un espace de parole, de partage et de guérison. Ici, les mères peuvent laisser un message, un poème, ou simplement un silence qui résonne avec leurs sœurs."
        )
        st.info("Formulaire et carrousel des Papotines simulés. (Nécessite Supabase)")
    elif current_page == "Organisation":
        render_weather_for_all()  # Affichage de la météo pour la démo (Uniquement ici)
    else:
        st.write(
            f"Contenu détaillé pour la section **{current_page}** à venir. En attendant, voici un aperçu de l'engagement de la communauté."
        )


def render_login_page():
    """
    Rend la page de connexion, propre et stylisée, avec un poème intégré.
    """

    # CSS pour le style de connexion (background, cartes, poème)
    st.markdown(
        """
        <style>
        /* Conteneur principal */
        .login-container {
            max-width: 800px; margin: 50px auto; padding: 30px;
            background-color: #fff8f0; /* Couleur douce et chaude */
            border-radius: 15px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid #f0e0d6;
        }
        /* Style du formulaire de connexion */
        .login-form-card {
            padding: 25px; background-color: white; border-radius: 10px;
            box-shadow: 0 4px 15px rgba(186, 104, 200, 0.1);
            border-left: 5px solid #ba68c8;
        }
        /* Style de la carte du poème */
        .poem-card {
            padding: 25px;
            background: linear-gradient(135deg, #f0e0d6 0%, #fff4ec 100%); /* Dégradé doux */
            border-radius: 10px; font-family: 'Georgia', serif; color: #555;
            text-align: center; font-style: italic; border: 1px solid #dcdcdc;
            box-shadow: 0 4px 15px rgba(255, 179, 179, 0.1);
        }
        .poem-card h4 {
            color: #7d4f3b; /* Couleur terre/racine */ margin-bottom: 15px;
            font-style: normal; border-bottom: 1px dashed #dcdcdc; padding-bottom: 10px;
        }
        .stButton>button {
            width: 100%; background-color: #ba68c8; color: white;
            border-radius: 8px; border: none; padding: 10px; font-weight: bold;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #9c4d9e;
        }
        </style>
        <div class='login-container'>
            <h1 style='text-align:center; color:#ba68c8;'>
                Bienvenue sur l'Espace Maternité 🤝
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Création des colonnes pour le formulaire et le poème
    col_form, col_poem = st.columns([1, 1])

    with col_form:
        st.markdown("<div class='login-form-card'>", unsafe_allow_html=True)
        st.subheader("Connexion sécurisée")

        # Formulaire de connexion
        with st.form("login_form"):
            # L'input doit être en majuscule pour correspondre à USER_PASSWORDS
            username = st.text_input(
                "Nom d'utilisateur (Rôle: MIDWIFE, PATIENT, etc.)", key="login_username"
            )
            password = st.text_input(
                "Mot de passe (Test!1234@)", type="password", key="login_password"
            )
            submitted = st.form_submit_button("Se connecter ➡️")

            if submitted:
                if validate_project(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = username
                    # Détermination du rôle pour le tableau de bord
                    st.session_state["role"] = username.upper().replace(
                        " ", ""
                    )  # Assure que le rôle est défini pour le sidebar
                    st.success("Connexion réussie ! Redirection...")
                    time.sleep(1)  # Délai pour l'affichage du succès
                    st.rerun()
                else:
                    st.error("Identifiants incorrects. Veuillez réessayer.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_poem:
        st.markdown("<div class='poem-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Le Chant de la Tente de Naissance</h4>")

        cree_poem = """
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
        st.markdown(cree_poem, unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align:right; margin-top:20px;'>— Inspiré par l'Esprit de Eeyou Istchee</p>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)


def render_dashboard_content(nav_selection):
    """Contenu principal du tableau de bord selon la sélection de navigation."""
    role = st.session_state["role"]

    if nav_selection == "Accueil":
        # Contenu de l'accueil (similaire au tableau de bord)
        st.markdown(f"## Tableau de Bord — Rôle: {role.capitalize()}")

        col_left, col_right = st.columns([2, 1])

        with col_left:
            render_cultural_carrousel(role)

        with col_right:
            st.markdown("### 📢 Annonces et alertes")
            if role == "MIDWIFE" or role == "NURSE":
                st.warning(
                    "Alerte: Vérifier les signes vitaux du nouveau-né 47-E à Chisasibi."
                )
                st.info(
                    "Mise à jour: Nouveau protocole de soins post-partum disponible."
                )
            elif role == "PATIENT":
                st.success(
                    "Félicitations pour votre nouvelle arrivée ! Consultez la section 'Ressources' pour les aides disponibles."
                )
            else:
                st.info("Aucune alerte critique pour votre rôle actuellement.")

            st.markdown("### 💬 Espace d'échange")
            st.text_area("Partage rapide:", height=100, max_chars=200)
            st.button("Envoyer le message ✉️", key="send_message_auth", width="stretch")

    elif nav_selection == "Tableau de bord":
        st.markdown(f"## Tableau de Bord Général — Rôle: {role.capitalize()}")
        st.info(
            "Cette section afficherait les métriques clés, les statistiques de naissances, et les indicateurs de santé pour la région."
        )
        # Ajout d'une visualisation simulée
        st.subheader("Indicateurs de Performance (Simulés)")
        chart_data = pd.DataFrame(
            {"mois": ["Jan", "Fév", "Mar", "Avr"], "naissances": [5, 8, 7, 10]}
        ).set_index("mois")
        st.bar_chart(chart_data)

    elif nav_selection == "Formulaires spécifiques":
        st.markdown(f"## Formulaires Spécifiques à votre Rôle ({role.capitalize()})")

        form_specifique = st.selectbox(
            "Choisir un formulaire spécifique",
            [
                "Nouveau-né (MIDWIFE)",
                "Évaluation pré-natale (NURSE)",
                "Rapport de recherche (DOCTORAL)",
            ],
            key="selectbox_form_specifique",
        )
        st.info(f"Le formulaire **{form_specifique}** serait chargé ici.")

    elif nav_selection == "Formulaires partagés":
        st.markdown("## Formulaires Partagés (Tous Rôles Professionnels)")

        form_partage = st.selectbox(
            "Choisir un formulaire partagé",
            [
                "Demande de ressource",
                "Rapport d'incident mineur",
                "Mise à jour d'adresse patient",
            ],
            key="selectbox_form_partage",
        )
        st.info(f"Le formulaire **{form_partage}** serait chargé ici.")

    elif nav_selection == "Ressources et Formation":
        st.markdown("## Ressources et Formation Continue")
        st.write(
            "Accédez à des guides, des vidéos de formation culturelle et des articles scientifiques."
        )
        st.image(
            load_static_asset("grand_mere_savoir.png"), caption="Transmission du savoir"
        )
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Placeholder vidéo

    elif nav_selection == "FAQ Professionnelle":
        st.markdown("## Foire aux Questions (FAQ) Professionnelle")
        st.expander("Comment consulter les dossiers patients?").write(
            "Utilisez la section 'Dossier Patient (Simulé)' pour une démonstration."
        )
        st.expander("Quel est le protocole d'urgence?").write(
            "Consultez le document 'Protocole d'urgence v2.1' dans l'onglet 'Ressources'."
        )

    elif nav_selection == "Déconnexion":
        st.markdown("## Déconnexion")
        st.warning("Êtes-vous sûr de vouloir vous déconnecter?")
        if st.button("Confirmer la Déconnexion 🚪", key="confirm_logout"):
            st.session_state["authenticated"] = False
            st.session_state["role"] = "PUBLIC"
            st.session_state["user"] = None
            st.rerun()

    else:
        st.markdown("## Bienvenue!")
        st.info(
            f"Veuillez sélectionner une option dans la barre latérale. Votre rôle actuel est **{role.capitalize()}**."
        )


def render_authenticated_dashboard():
    """
    Rend l'interface utilisateur pour un utilisateur authentifié (Tableau de bord)
    avec le menu de navigation demandé dans la barre latérale.
    """
    # --- Espace Authentifié (Tableau de Bord) ---
    st.sidebar.title(f"Bienvenue, {st.session_state['user'].capitalize()} 👋")

    # 3.1 Définition du rôle
    role = st.session_state["role"]

    # --- NOUVEAU: Selectbox pour changer de rôle rapidement (Point 4) ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎭 Changer de Rôle (Test)")

    current_role_index = ALL_ROLES.index(role) if role in ALL_ROLES else 0

    new_role = st.sidebar.selectbox(
        "Tester un autre rôle",
        ALL_ROLES,
        index=current_role_index,
        key="role_switcher",
        help="Change le rôle sans déconnexion, utile pour les tests d'accès.",
    )

    if new_role != role:
        st.session_state["role"] = new_role
        st.session_state["user"] = new_role  # Met à jour l'utilisateur pour l'affichage
        st.rerun()
    # --------------------------------------------------------------------

    # 3.2 Gestion du son (FIX 1: Audio par injection JS)
    if "audio_running" not in st.session_state:
        st.session_state.audio_running = True  # Initialisation à True
    if "audio_level" not in st.session_state:
        st.session_state.audio_level = "🔊"

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 🎵 Contrôle Audio")

    # Audio HTML injection (sera réinjecté à chaque rerun si 'audio_running' est True)
    if st.session_state.audio_running:
        # Balise audio avec ID pour le contrôle par JS (FIX 2: Ajout src sur audio et preload)
        st.markdown(
            """
            <audio id="bebe_audio" src="static/bebe_pleure.mp3" autoplay loop preload="auto">
                Votre navigateur ne supporte pas l'élément audio.
            </audio>
            <script>
                // Tente de jouer l'audio, contournant les restrictions Streamlit/Navigateur
                var audio = document.getElementById('bebe_audio');
                if (audio) { 
                    audio.volume = 0.5; // Volume par défaut
                    // Tente de jouer. En cas d'échec (restriction navigateur), log l'erreur.
                    audio.play().catch(e => console.log('Autoplay failed (requires user interaction):', e)); 
                }
            </script>
            """,
            unsafe_allow_html=True,
        )

    # Affichage de l'état du son
    audio_status = (
        "🔊 Le son est actif"
        if st.session_state.audio_running
        else "🔇 Le son est en pause"
    )
    st.sidebar.markdown(
        f"<div style='text-align:center; font-size:18px;'>{audio_status}</div>",
        unsafe_allow_html=True,
    )

    volume_icon = st.sidebar.select_slider(
        "Niveau du son",
        ["🔈", "🔉", "🔊"],
        value=st.session_state.audio_level,
        key="volume_slider_auth",
    )
    st.session_state.audio_level = volume_icon

    # Injection JS pour ajuster le volume
    volume_map = {"🔈": 0.25, "🔉": 0.5, "🔊": 1.0}
    st.markdown(
        f"""
        <script>
            var audio = document.getElementById('bebe_audio');
            if (audio) {{ audio.volume = {volume_map[volume_icon]}; }}
        </script>
    """,
        unsafe_allow_html=True,
    )

    # Boutons de contrôle (utilisent JS pour la pause/lecture explicite)
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("⏸️ Couper le son", key="stop_audio"):
            st.session_state.audio_running = False
            # Injection JS pour mettre en pause
            st.markdown(
                """<script>
                var audio = document.getElementById('bebe_audio');
                if (audio) { audio.pause(); }
            </script>""",
                unsafe_allow_html=True,
            )
            st.rerun()  # Rerun pour mettre à jour l'état visuel et ne plus injecter l'audio
    with col2:
        if st.button(f"{volume_icon} Reprendre le son", key="start_audio"):
            st.session_state.audio_running = True
            # Injection JS pour jouer
            st.markdown(
                """<script>
                var audio = document.getElementById('bebe_audio');
                if (audio) { 
                    audio.play().catch(e => console.log('Explicit play failed:', e));
                }
            </script>""",
                unsafe_allow_html=True,
            )
            st.rerun()  # Rerun nécessaire pour réafficher l'élément <audio> complet (autoplay/loop)

    # --- NOUVEAU: Menu latéral de navigation (Points 2/3) ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🗂️ Que voulez-vous faire?")

    # Définition des options pour le menu principal
    nav_options = [
        "Accueil",
        "Tableau de bord",
        "Formulaires spécifiques",
        "Formulaires partagés",
        "Déconnexion",
    ]

    # Surcharge de la page sélectionnée par le menu principal
    nav_selection = st.sidebar.radio(
        "Sélectionnez la page",
        nav_options,
        key="main_nav_sidebar",
        index=(
            0
            if st.session_state.get("current_auth_page") not in nav_options
            else nav_options.index(st.session_state.get("current_auth_page"))
        ),
    )

    st.session_state["current_auth_page"] = nav_selection

    # --- 3.4 Logique de rendu central ---
    if nav_selection == "Déconnexion":
        # Traitement spécifique pour la déconnexion
        st.markdown("## Déconnexion")
        st.warning("Êtes-vous sûr de vouloir vous déconnecter?")
        if st.button("Confirmer la Déconnexion 🚪", key="confirm_logout_dash"):
            st.session_state["authenticated"] = False
            st.session_state["role"] = "PUBLIC"
            st.session_state["user"] = None
            st.rerun()
    else:
        render_dashboard_content(nav_selection)


# ---------------------------------------------------------
# 6. LOGIQUE DE L'APPLICATION PRINCIPALE
# ---------------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["role"] = "PUBLIC"

# 1. Page Publique (Non authentifiée)
if not st.session_state["authenticated"]:
    # st.sidebar.image(load_static_asset("logo_crie.png"), use_column_width=True) # Ex de logo
    st.sidebar.title("Plateforme Maternité Crie")

    st.sidebar.markdown("---")
    public_choice = st.sidebar.radio(
        "Accès Public",
        ["Connexion Professionnelle"],
        key="public_nav",
        index=0,
    )

    if public_choice == "Informations Générales":
        show_public_header()
        render_info_section()
    elif public_choice == "Connexion Professionnelle":
        render_login_page()

# 2. Page Authentifiée (Tableau de Bord)
else:
    render_authenticated_dashboard()
