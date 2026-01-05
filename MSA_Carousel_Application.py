# 🐍 Librairies standards et tierces
import streamlit as st
import time
import os
import base64
import sys
import importlib
import requests
import datetime
import requests
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd  # Ajout explicite pour la Section 1 (Météo)


# --- Imports des Fonctions/Formulaires Partagés ---
from modules.shared.form_carrousel_soins import (
    render_carrousel_soins_form,
    render_bebe_pleure,
)

# --- Registre centralisé des formulaires et dashboards ---
# NOTE: Ces imports sont maintenus même si form_registry.py n'est pas fourni,
# car l'application en dépend structurellement.
from modules.public.form_registry import (
    get_forms_for_role,
    get_all_registries,
    get_dashboards_for_role,
    get_shared_forms,  # ← utilisé pour les formulaires partagés
)

# from modules.common.carousel import render_cultural_carousel
from modules.public.form_registry import get_shared_forms
from modules.common.carousel import render_cultural_carousel
from modules.utils.display import (
    render_bebe_pleure,
    play_audio,
    play_audio_if_enabled,
    render_audio_controls,
)


# L'import de form_loader est redondant avec les fonctions locales, mais maintenu pour la structure
from modules.utils.form_loader import (
    load_form as _load_form_util,  # Renommé pour éviter le conflit avec la fonction locale
    get_form_functions,
)


# Initialisation de la variable audio_running
if "audio_running" not in st.session_state:
    st.session_state["audio_running"] = False

# Toggle interactif
st.sidebar.markdown("### 🔊 Contrôle du son")
st.session_state["audio_running"] = st.sidebar.toggle(
    "Activer le son", value=st.session_state["audio_running"], key="audio_toggle"
)

# Message visuel + lecture audio
if st.session_state["audio_running"]:
    st.success("🔊 Le son est actif")
    play_audio("/home/ygd/projets-midwifery-Services/static/bebe_pleure.mp3")
else:
    st.info("🔇 Le son est en pause")


# --- Fonction générique pour charger un formulaire ---
def load_form(module_path: str):
    """
    Charge dynamiquement un formulaire à partir de son chemin de module
    et exécute sa fonction `render_form()`.

    ATTENTION: Pour que cela fonctionne, les modules (ex: modules.specific.form_patient)
    doivent être importables et contenir une fonction 'render_form'.
    """
    st.subheader(
        f"📄 Formulaire : {module_path.split('.')[-1].replace('_', ' ').title()}"
    )
    st.markdown("---")
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, "render_form"):
            # Exécution du vrai formulaire
            module.render_form()
        else:
            # Remplacement du placeholder: Afficher une erreur si le module est là mais la fonction manque.
            st.error(
                f"❌ Le module {module_path} a été chargé, mais la fonction `render_form()` est manquante. Impossible d'afficher le formulaire."
            )

    except ModuleNotFoundError:
        st.error(
            f"Erreur: Le module {module_path} est introuvable. Assurez-vous que le chemin est correct."
        )
    except Exception as e:
        st.error(
            f"Erreur lors du chargement ou du rendu du formulaire {module_path}: {e}"
        )


# --- Fonction générique pour charger un dashboard ---
def load_dashboard(module_path: str):
    """
    Charge dynamiquement un dashboard à partir de son chemin de module.
    Chaque module doit exposer une fonction de rendu (ex: render_dashboard_*).
    """
    try:
        # Tente de charger et d'exécuter la fonction de rendu (Ex: modules.dashboards.dashboard_admin.render_dashboard_admin)
        module_name, func_name = module_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        renderer = getattr(module, func_name, None)
        if callable(renderer):
            renderer()
        else:
            # Remplacement du placeholder: Afficher une erreur si la fonction de rendu est manquante.
            st.error(
                f"❌ La fonction de rendu `{func_name}` dans le module `{module_name}` est introuvable ou non valide. Impossible de charger le Tableau de bord."
            )

    except ModuleNotFoundError:
        st.error(
            f"Erreur: Le module {module_path} est introuvable. Vérifiez le `form_registry.py`."
        )
    except Exception as e:
        st.error(f"Erreur lors du chargement du dashboard {module_path}: {e}")


# =========================================================================
# 📦 SECTION 1 : FONCTIONS DE RENDU SPÉCIFIQUES (ACCUEIL)
# =========================================================================

# Coordonnées des communautés
communities = {
    "Waskaganish": {"lat": 51.47, "lon": -78.77, "color": "red"},
    "Mistissini": {"lat": 50.42, "lon": -73.87, "color": "blue"},
    "Chisasibi": {"lat": 53.75, "lon": -78.93, "color": "green"},
}


def get_weather(lat, lon, hourly=False):
    """Appelle l’API Open-Meteo pour obtenir la météo en temps réel ou horaire."""
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
    if hourly:
        url = f"{base_url}&hourly=temperature_2m,windspeed_10m&timezone=America/Toronto"
    else:
        url = f"{base_url}&current_weather=true&timezone=America/Toronto"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}


import streamlit.components.v1 as components


def render_cultural_carousel(image_width: int = 90, image_height: int = 320):
    html = generate_carousel_html(fiches, image_width, image_height)
    components.html(html, height=image_height + 250)


def render_weather_map():
    """Carte interactive + sélecteur + graphiques météo."""
    st.subheader("🌦️ Carte météo: Waskaganish - Chisasibi - Mistissini")

    # Carte centrée sur la Baie-James
    m = folium.Map(location=[53.0, -77.0], zoom_start=6, tiles="OpenStreetMap")

    # Ajout des marqueurs avec météo en tooltip
    for name, info in communities.items():
        data = get_weather(info["lat"], info["lon"])
        weather = data.get("current_weather", {})
        tooltip_text = f"🌡️ {weather.get('temperature','?')}°C | 💨 {weather.get('windspeed','?')} km/h | ⏰ {weather.get('time','?')}"
        folium.Marker(
            location=[info["lat"], info["lon"]],
            popup=f"<b>{name}</b><br>{tooltip_text}",
            tooltip=f"{name} → {tooltip_text}",
            icon=folium.Icon(color=info["color"], icon="cloud"),
        ).add_to(m)

    # Affichage de la carte
    st_folium(m, width=800, height=600)

    # Sélecteur de communauté
    choice = st.selectbox(
        "Choisir une communauté pour détails météo :", list(communities.keys())
    )

    # Météo détaillée + graphiques
    selected = communities[choice]
    data = get_weather(selected["lat"], selected["lon"], hourly=True)

    if "hourly" in data:
        temps = data["hourly"]["temperature_2m"]
        winds = data["hourly"]["windspeed_10m"]
        times = data["hourly"]["time"]

        df = pd.DataFrame(
            {"Heure": times, "Température (°C)": temps, "Vent (km/h)": winds}
        )

        st.markdown(f"### 🌍 Météo détaillée à {choice}")
        st.write(f"🌡️ Température actuelle : {data['hourly']['temperature_2m'][0]} °C")
        st.write(f"💨 Vent actuel : {data['hourly']['windspeed_10m'][0]} km/h")

        # Graphique température
        fig_temp = px.line(
            df,
            x="Heure",
            y="Température (°C)",
            title=f"🌡️ Température sur 24h à {choice}",
            markers=True,
        )
        st.plotly_chart(fig_temp, use_container_width=True)

        # Graphique vent
        fig_wind = px.line(
            df,
            x="Heure",
            y="Vent (km/h)",
            title=f"💨 Vitesse du vent sur 24h à {choice}",
            markers=True,
        )
        st.plotly_chart(fig_wind, use_container_width=True)
    else:
        st.error(f"Impossible de récupérer la météo pour {choice}.")


def render_home_page():
    st.title("Bienvenue dans MSA ! 💖")
    st.markdown("Un lieu de soin, de culture et de célébration partagée.")

    st.markdown("---")
    render_weather_map()
    st.markdown("---")
    render_cultural_carousel()
    st.markdown("---")
    st.subheader("")
    play_audio_if_enabled("bebe_pleure.mp3")

    # Synchronisation : le son ne joue que si le carrousel est actif
    if st.session_state.get("main_section_auth") == "Accueil":
        render_bebe_pleure()


def render_section(section: str, role: str):
    """Affiche le contenu principal selon la section choisie."""

    # 🏠 ACCUEIL
    if section == "Accueil":
        # Utilise la fonction de rendu unifiée de l'accueil pour la session authentifiée
        render_home_page()

    # 📊 TABLEAU DE BORD
    elif section == "Tableau de bord":
        render_dashboard_section(role)

    # 📂 FORMULAIRES SPÉCIFIQUES
    elif section == "Formulaires spécifiques":
        st.title("📂 Formulaires spécifiques")
        st.info(f"Sélectionnez un formulaire spécifique pour le rôle : **{role}**")
        forms_for_role = get_forms_for_role(role)

        if not forms_for_role:
            st.warning("Aucun formulaire spécifique trouvé pour ce rôle.")
            return

        # Utiliser un conteneur pour les boutons de formulaire
        form_container = st.container()

        for key, config in forms_for_role.items():
            label = config.get("title", key)

            with form_container:
                # Appel réel à load_form pour afficher le contenu
                if st.button(f"📄 {label}", key=f"specific_form_{key}"):
                    # Afficher le titre de la section au-dessus du formulaire chargé
                    st.session_state["active_form"] = config["module"]
                    st.session_state["active_form_title"] = label
                    st.rerun()  # Rerun pour que le formulaire se charge dans le corps principal.

        # Affichage du formulaire sélectionné après la boucle de boutons
        if (
            st.session_state.get("active_form")
            and st.session_state["main_section_auth"] == section
        ):
            st.subheader(
                f"Formulaire Actif : **{st.session_state['active_form_title']}**"
            )
            load_form(st.session_state["active_form"])

    # 🌐 FONCTIONS PARTAGÉES (CORRIGÉ POUR CHARGER LES VRAIS FORMULAIRES)
    elif section == "Fonctions partagées":
        st.title("🌐 Fonctions partagées")
        st.info("Sélectionnez une fonction partagée disponible pour tous les rôles.")
        forms_shared = get_shared_forms()

        if not forms_shared:
            st.warning("Aucune fonction partagée trouvée.")
            return

        # Utiliser un conteneur pour les boutons de fonction partagée
        shared_func_container = st.container()

        for key, config in forms_shared.items():
            label = config.get("title", key)

            with shared_func_container:
                # Appel réel à load_form pour afficher le contenu
                if st.button(f"🔗 {label}", key=f"shared_func_{key}"):
                    # Stocker la sélection pour le rechargement
                    st.session_state["active_shared_func"] = config["module"]
                    st.session_state["active_shared_func_title"] = label
                    st.rerun()  # Rerun pour que la fonction se charge dans le corps principal.

        # Affichage du formulaire/fonction partagée sélectionné après la boucle de boutons
        if (
            st.session_state.get("active_shared_func")
            and st.session_state["main_section_auth"] == section
        ):
            st.subheader(
                f"Fonction Active : **{st.session_state['active_shared_func_title']}**"
            )
            load_form(st.session_state["active_shared_func"])
            # Réinitialiser après affichage pour permettre de sélectionner une autre fonction
            # Note: Un rerender sera nécessaire après le load_form() si le formulaire utilise st.form()

    # 🧵 WORKSHOPS
    elif section == "Workshops":
        st.title("🧵 Ateliers & Carrousels")
        render_carrousel_soins_form()
        st.markdown("---")
        render_bebe_pleure()

    else:
        # Ceci est le cas non implémenté. Maintenant, toutes les sections principales sont gérées.
        st.warning("⚠️ Section inconnue ou non implémentée.")


# =========================================================================
# ⚙️ SECTION 2 : CONSTANTES ET DONNÉES STATIQUES
# (Logique inchangée, conservée pour la complétude)
# =========================================================================

# 🌐 URLs d'assets statiques simulées (pour le carrousel sur la page de connexion)
STATIC_ASSET_URLS = {
    "img_1": "https://placehold.co/900x400/3498db/ffffff?text=Carrousel+1",
    "img_2": "https://placehold.co/900x400/2ecc71/ffffff?text=Carrousel+2",
    "img_3": "https://placehold.co/900x400/e74c3c/ffffff?text=Carrousel+3",
}

# 🌤️ Icônes météo (pour la carte)
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
# 📚 Fiches culturelles (carrousel sur la page d'accueil)
import os

# Définir le chemin vers le dossier static (à la racine du projet)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

fiches = {
    "Transmission des savoirs": {
        "titre": "Transmission des savoirs",
        "image": os.path.join(STATIC_DIR, "Grand_mere_et_enfant.png"),
        "description": "👵 Les aînées partagent leur sagesse à travers les récits et les gestes.",
        "citation": "« Ce que tu apprends avec ton cœur, tu ne l’oublies jamais. »",
    },
    "Accueil sur le territoire": {
        "titre": "Accueil sur le territoire",
        "image": os.path.join(STATIC_DIR, "Accueil_territoire.png"),
        "description": "🌿 Le lien sacré avec la terre, les ancêtres et les esprits protecteurs.",
        "citation": "« Chaque pas sur cette terre est une prière. »",
    },
    "Maternité et continuité": {
        "titre": "Maternité et continuité",
        "image": os.path.join(STATIC_DIR, "Mere_crie.png"),
        "description": "👩‍👧 La force des mères cries, gardiennes de la vie et de l’avenir.",
        "citation": "« Porter un enfant, c’est porter l’histoire de notre peuple. »",
    },
    "Le retour attendu": {
        "titre": "Le souffle de l'avenir",
        "image": os.path.join(STATIC_DIR, "Le_retour_attendu.png"),
        "description": "Deux jeunes mères partageant un moment de quiétude avec leurs nouveau-nés.",
        "citation": "« La vie que nous tenons dans nos bras est l'héritage de nos ancêtres et le futur de notre peuple. »",
    },
    "La transmission du savoir ancestral": {
        "titre": "La transmission du savoir ancestral",
        "image": os.path.join(STATIC_DIR, "Tissage_et_transmission.png"),
        "description": "Gestes et traditions qui relient la maternité à l'esprit de la terre.",
        "citation": "« Dans chaque pli de la peau d'une aînée se cachent les histoires qui protégeront le nouveau-né. »",
    },
    "Le berceau de la nature": {
        "titre": "Le berceau de la nature",
        "image": os.path.join(STATIC_DIR, "Berceau_nature.png"),
        "description": "Dès leurs premiers instants, la nature est intégrée dans le soin des tout-petits.",
        "citation": "« Comme une graine dans la terre, notre bébé trouvera sa force dans le territoire. »",
    },
}


# =========================================================================
# 🗂️ SECTION 2 : CONSTANTES ET REGISTRES
# =========================================================================

# --- Simulation des mots de passe (à remplacer par une source sécurisée en production) ---
USER_PASSWORDS = {
    "MIDWIFE": "msa2024",
    "NURSE": "nurse2024",
    "DOCTOR": "doc2024",
    "PATIENT": "pat2024",
    "STUDENT": "stud2024",
    "INTERN": "intern2024",
    "DOCTORAL": "phd2024",
    "ADMIN": "admin2024",
}


# --- Assets Statiques Simples (URLs simulées) ---
# Utilisation de placeholders pour simuler les images/vidéos
PLACEHOLDER_IMG_BASE64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

STATIC_ASSET_URLS = {
    "logo": PLACEHOLDER_IMG_BASE64,
    "img_1": "https://placehold.co/800x400/87CEEB/ffffff?text=MSA",
    "img_2": "https://placehold.co/800x400/90EE90/000000?text=Midwifery+Services",
    "img_3": "https://placehold.co/800x400/FFB6C1/000000?text=Community+Support",
    # Chemins simulés pour image_to_base64. Ces fichiers doivent exister pour l'affichage réel.
    "aurores.png": "/static/aurores.png",
    "fiche_2.jpg": "data/images/fiche_2.jpg",
    "fiche_3.jpg": "data/images/fiche_3.jpg",
    "video_explicative": "/static/mov_bbb.mp4",  # Vidéo explicative simulée
}


# =========================================================================
# 🧩 SECTION 3 : FONCTIONS UTILITAIRES (HELPERS)
# (Logique inchangée, conservée pour la complétude)
# =========================================================================


def load_static_asset(asset_name):
    """Charge l'URL d'un asset statique simulé (usage pour URL/HTML)."""
    return STATIC_ASSET_URLS.get(asset_name, "")


@st.cache_data
def get_current_weather(lat, lon):
    """Récupère et met en cache les données météo actuelles d'Open-Meteo. (Logique conservée)"""
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
        # st.error(f"Erreur lors de la récupération météo pour {lat}, {lon}")
        return None


def image_to_base64(image_path: str) -> str:
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return "data:image/png;base64," + base64.b64encode(data).decode("utf-8")
    except FileNotFoundError:
        return None


def generate_carousel_html(fiches: dict, image_width: int, image_height: int) -> str:
    slides = ""
    for fiche in fiches.values():
        img_data = image_to_base64(fiche["image"])
        if img_data:
            slides += f"""
                <div class="swiper-slide">
                    <h3>{fiche['titre']}</h3>
                    <img src="{img_data}" style="width:{image_width}%; height:{image_height}px; object-fit:cover; border-radius:12px; margin:auto; display:block;" />
                    <p>{fiche['description']}</p>
                    <blockquote><em>{fiche['citation']}</em></blockquote>
                </div>
            """
        else:
            slides += f"""
                <div class="swiper-slide">
                    <h3>{fiche['titre']}</h3>
                    <div style="height:{image_height}px; background-color:#F0F0F0; border-radius:10px; display:flex; align-items:center; justify-content:center; width:{image_width}%; margin:auto;">
                        Image introuvable : {os.path.basename(fiche['image'])}
                    </div>
                    <p>{fiche['description']}</p>
                    <blockquote><em>{fiche['citation']}</em></blockquote>
                </div>
            """

    return f"""
        <link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css"/>
        <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>

        <style>
            .swiper-slide {{
                transition: opacity 1s ease-in-out;
            }}
        </style>

        <div class="swiper-container" style="width:100%; max-width:700px; margin:auto;">
            <div class="swiper-wrapper">
                {slides}
            </div>
            <div class="swiper-pagination"></div>
            <div class="swiper-button-prev"></div>
            <div class="swiper-button-next"></div>
        </div>

        <script>
            var swiper = new Swiper('.swiper-container', {{
                effect: 'fade',
                fadeEffect: {{
                    crossFade: true
                }},
                direction: 'horizontal',
                loop: true,
                autoplay: {{
                    delay: 6000,
                    disableOnInteraction: false
                }},
                slidesPerView: 1,
                spaceBetween: 0,
                pagination: {{
                    el: '.swiper-pagination',
                    clickable: true
                }},
                navigation: {{
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev'
                }}
            }});
        </script>
    """


def render_bebe_experience():
    """Affiche l'animation du nouveau-né et le son réel."""
    # Bloc visuel avec effet "machine à écrire"
    st.markdown(
        """
        <div style="border: 2px solid #ffb6c1; border-radius: 12px; padding: 1rem; background-color: #fff0f5;">
            <h3 style="color:#d63384;"></h3>
            <div id="typewriter" style="font-size:1.1rem; font-family:monospace; color:#333;"></div>
        </div>
        <script>
        const text = "Un nouveau-né pleure doucement... et le monde s’éveille avec tendresse.";
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                document.getElementById("typewriter").innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        if (document.getElementById("typewriter") && !document.getElementById("typewriter").getAttribute("data-typed")) {
            typeWriter();
            document.getElementById("typewriter").setAttribute("data-typed", "true");
        }
        </script>
        """,
        unsafe_allow_html=True,
    )

    # # Définir le chemin vers le fichier audio
    # audio_path = os.path.join("static", "bebe_pleure.mp3")

    # # Vérifier que le fichier existe avant de l'afficher
    # if os.path.exists(audio_path):
    #     st.audio(audio_path, format="audio/mp3")
    # else:
    #     st.warning(
    #         "⚠️ Le fichier audio 'bebe_pleure.mp3' est introuvable dans le dossier static."
    #     )


def render_bebe_pleure():
    """Fonction wrapper pour le son du bébé pleure, comme demandé par l'appel dans l'original."""
    render_bebe_experience()


def normalize_session(last_sess):
    """Normalise la session en dict avec clés 'start' et 'end'. (Logique conservée)"""
    if isinstance(last_sess, dict):
        return {
            "start": last_sess.get("start"),
            "end": last_sess.get("end"),
            "role": last_sess.get("role", "inconnu"),
        }
    elif isinstance(last_sess, datetime.datetime):
        return {
            "start": last_sess,
            "end": None,
            "role": "inconnu",
        }
    else:
        return {
            "start": None,
            "end": None,
            "role": "inconnu",
        }


def is_valid_module(path: str) -> bool:
    """Vérifie si le module existe avant de le charger. (Logique conservée)"""
    try:
        module_name = path.replace("/", ".")
        # Vérifie si le module est déjà chargé
        if module_name in sys.modules:
            return True
        # Sinon, tente de l'importer
        importlib.import_module(module_name)
        return True
    except ModuleNotFoundError:
        return False


def load_form_renderer(module_path: str):
    """Charge dynamiquement le module et retourne sa fonction render_form()."""
    # Mise à jour: Tente d'importer et d'exécuter, ou signale l'erreur
    try:
        module = importlib.import_module(module_path)
        return getattr(module, "render_form")
    except ModuleNotFoundError:
        st.error(
            f"Erreur: Le module {module_path} est introuvable. Impossible de charger le renderer."
        )
        return lambda: st.error("Fonction de rendu indisponible.")


# =========================================================================
# 🖼️ SECTION 4 : FONCTIONS DE RENDU PRINCIPALES (PAGES)
# =========================================================================

# --- Fonctions de rendu de la partie Authentifiée ---


def render_accueil():
    """Affiche la page d'accueil après connexion. (Logique conservée)"""
    st.title("🏠 Accueil")
    st.markdown("Bienvenue dans l'application Midwifery Services.")


def render_dashboard_section(role: str):
    """Affiche le tableau de bord correspondant au rôle via le registre."""
    dashboard_path = get_dashboards_for_role(role)

    if dashboard_path:
        st.write(f"🔎 Rôle détecté: {role} → Chemin: {dashboard_path}")
        try:
            # Appel à la fonction load_dashboard qui est maintenant un placeholder
            load_dashboard(dashboard_path)
        except Exception as e:
            st.error(f"Erreur lors du chargement du tableau de bord {role}: {e}")
    else:
        st.warning(f"⚠️ Aucun tableau de bord trouvé pour le rôle **{role}**.")


def render_workshops():
    """Affiche la section Workshops/Ateliers. (Logique conservée)"""
    st.title("🧵 Ateliers & Carrousels")
    st.markdown("### Leçon sur la vie et la culture")
    # L'original appelle render_bebe_pleure() via un commentaire, ici on l'inclut pour être conforme à la demande.
    render_bebe_pleure()
    st.markdown("---")
    # L'original appelle load_form("modules.shared.form_carrousel_soins"), mais puisque cette fonction n'existe pas en dehors du carrousel lui-même, nous l'appelons directement
    render_carrousel_soins_form()


# --- Fonctions de rendu de la partie Publique (non-connectée) ---


def render_non_auth_home():
    """
    Affiche la page d'accueil publique (sans les fiches culturelles ni la météo).
    CORRIGÉ (Point 3): Empêche l'affichage du carrousel/météo avant connexion.
    """
    st.markdown("### Présentation du projet")
    st.write(
        """
        Le projet **MSA** vise à améliorer l'accès et la qualité des soins de sage-femme
        pour les familles des communautés cries de **Waskaganish**, **Chisasibi** et **Mistissini** *(à venir)*,
        dans les Territoires-cries-de-la-Baie-James.

        Notre objectif est d’offrir un soutien médical et émotionnel respectueux des cultures autochtones,
        en favorisant les soins de proximité, l’intégration culturelle et la formation des professionnel·les.

        🔑 **Partenaires clés :** Nishiyuu, National Indigenous Association of Midwives, I‑CLSC, Care 4, CHB, RSFQ,
        Canadian Midwifery Minimum Database, MSSS.

        📊 Les données recueillies seront partagées chaque année avec les communautés d’Eeyou Istchee
        par le rapport annuel des Services de sage‑femme et du Cree Health Board.

        ❤️ Merci à toutes et tous pour votre engagement à offrir des soins de sage-femme de haute qualité
        aux familles d’Eeyou Istchee.
        """
    )


def render_info_section():
    """Affiche le contenu de la page d'information publique sélectionnée (Accueil, À propos, etc.)."""
    # Remplacement du placeholder : utilisation de "accueil" par défaut (point 3)
    page_key = st.session_state.get("info_page", "accueil")

    public_forms = get_forms_for_role("PUBLIC")
    config = public_forms.get(page_key)

    st.subheader(
        f"Informations Publiques : {config.get('title', page_key).capitalize()}"
    )
    st.markdown("---")

    if page_key == "accueil":
        # Affiche la version allégée de l'accueil public
        render_non_auth_home()

    elif config and config.get("module"):
        # Correction : Tente de charger le VRAI formulaire public (si le module est défini)
        try:
            render_func = load_form_renderer(config["module"])
            render_func()
        except Exception as e:
            # Remplacement du placeholder: Afficher une erreur si l'import/l'exécution échoue
            st.error(
                f"❌ Erreur lors du chargement du formulaire public `{config.get('title', page_key)}` depuis le module `{config.get('module')}`: {e}"
            )

    else:
        st.error("Page d'information publique inconnue ou manquante.")


def render_public_header():
    """Affiche l'en-tête public avec les liens d'information stylisés (via form_registry)."""

    # --- CSS pour styliser les boutons ---
    st.markdown(
        """
        <style>
        .public-header-row .stButton > button {
            background: none !important;
            border: none !important;
            color: #1e40af;
            padding: 5px 10px;
            text-decoration: none !important;
            box-shadow: none;
            margin: 0;
            width: 100%;
        }
        .public-header-row .stButton > button:hover {
            background-color: #eff6ff !important;
            text-decoration: underline !important;
            color: #3b82f6 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Titre et sous-titre ---
    st.title("Midwifery Services Application")
    st.caption(
        "Plateforme de soutien et de coordination dans les communautés de Waskaganish, "
        "Chisasibi et Mistissini (à venir)."
    )

    # --- Génération dynamique des boutons depuis le registre ---
    public_forms = get_forms_for_role("PUBLIC")

    if public_forms:
        cols = st.columns(len(public_forms))
        st.markdown("<div class='public-header-row'>", unsafe_allow_html=True)

        for i, (col, (key, config)) in enumerate(zip(cols, public_forms.items())):
            with col:
                # Affiche le titre (ex. "Accueil") mais stocke la clé interne (ex. "accueil")
                if st.button(config.get("title", key), key=f"nav_pub_{i}_{key}"):
                    # Correction : Cette ligne permet de changer l'état et de déclencher le rerender
                    st.session_state["info_page"] = key  # clé interne cohérente
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Aucun formulaire public trouvé dans le registre.")


def render_sidebar_auth(role: str):
    apply_sidebar_theme(role)

    st.sidebar.markdown(f"**Utilisateur :** `{role}`")
    st.sidebar.markdown("---")

    # Sections internes (propres)
    sections = [
        "Accueil",
        "Tableau de bord",
        "Formulaires spécifiques",
        "Fonctions partagées",
        "Workshops",
    ]

    # Labels enrichis
    labels = {
        "Accueil": "🌿 Accueil",
        "Tableau de bord": "📊 Tableau de bord",
        "Formulaires spécifiques": "📝 Formulaires spécifiques",
        "Fonctions partagées": "🤝 Fonctions partagées",
        "Workshops": "🎓 Workshops",
    }

    # Initialisation
    if "main_section_auth" not in st.session_state:
        st.session_state["main_section_auth"] = "Accueil"

    # Radio avec labels enrichis
    selected_label = st.sidebar.radio(
        "Navigation principale",
        [labels[s] for s in sections],
        index=sections.index(st.session_state["main_section_auth"]),
    )

    # Convertir le label choisi en clé interne
    selected_section = [k for k, v in labels.items() if v == selected_label][0]
    st.session_state["main_section_auth"] = selected_section

    st.sidebar.markdown("---")

    # # 🔊 Toggle audio avec clé unique par rôle
    # audio_enabled = st.sidebar.toggle("🔊 Activer le son", key=f"audio_toggle_{role}")

    # # # Utiliser directement audio_enabled ou st.session_state[f"audio_toggle_{role}"]
    # # if audio_enabled:
    # #     st.sidebar.success("Le son est activé.")
    # # else:
    # #     st.sidebar.info("Le son est désactivé.")

    if st.sidebar.button("Déconnexion 🚪"):
        st.session_state["authenticated"] = False
        for key in [
            "role",
            "active_form",
            "active_form_title",
            "active_shared_func",
            "active_shared_func_title",
            "main_section_auth",
            f"audio_toggle_{role}",  # nettoyer aussi le toggle
        ]:
            st.session_state.pop(key, None)
        st.rerun()

    return selected_section


def apply_sidebar_theme(role: str):
    # Palette de couleurs par rôle
    colors = {
        "MIDWIFE": "#f8c8dc",  # rose tendre
        "GUEST": "#c8e4f8",  # bleu doux
        "ADMIN": "#d3d3d3",  # gris sobre
        "STUDENT": "#e6f7d9",  # vert clair
        "DOCTOR": "#cce5ff",  # bleu médical
        "NURSE": "#fff0f5",  # lilas doux
        "PATIENT": "#fdf5e6",  # beige réconfortant
        "INTERN": "#f0fff0",  # vert pâle
        "DOCTORAL": "#f5f5dc",  # ivoire académique
    }

    # Typographie par rôle
    fonts = {
        "MIDWIFE": "cursive",  # doux et poétique
        "GUEST": "sans-serif",  # simple et accueillant
        "ADMIN": "monospace",  # sobre et structuré
        "STUDENT": "Comic Sans MS",  # ludique et apprentissage
        "DOCTOR": "Helvetica",  # clair et professionnel
        "NURSE": "Verdana",  # lisible et rassurant
        "PATIENT": "Georgia",  # chaleureux et réconfortant
        "INTERN": "Tahoma",  # moderne et léger
        "DOCTORAL": "Times New Roman",  # académique et classique
    }

    color = colors.get(role, "#ffffff")
    font = fonts.get(role, "sans-serif")

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-color: {color};
            font-family: {font};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# def apply_sidebar_theme(role: str):
#     colors = {
#         "MIDWIFE": "#f8c8dc",  # rose tendre
#         "GUEST": "#c8e4f8",  # bleu doux
#         "ADMIN": "#d3d3d3",  # gris sobre
#         "STUDENT": "#e6f7d9",  # vert clair, apprentissage
#         "DOCTOR": "#cce5ff",  # bleu médical
#         "NURSE": "#fff0f5",  # lilas doux, soin
#         "PATIENT": "#fdf5e6",  # beige réconfortant
#         "INTERN": "#f0fff0",  # vert pâle, initiation
#         "DOCTORAL": "#f5f5dc",  # ivoire académique
#     }

#     # Couleur par défaut si rôle inconnu
#     color = colors.get(role, "#ffffff")

#     st.markdown(
#         f"""
#         <style>
#         [data-testid="stSidebar"] {{
#             background-color: {color};
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# --- Logique d'authentification ---


def check_password(username, password):
    """Vérifie le nom d'utilisateur et le mot de passe."""
    # Convertir en majuscules pour correspondre aux clés du dictionnaire
    username = username.upper()
    return USER_PASSWORDS.get(username) == password, username


def render_login_form():
    """Affiche l'interface de connexion dans la barre latérale."""

    st.sidebar.title("🔑 Connexion")
    st.sidebar.markdown("---")

    # Formulaire de connexion
    with st.sidebar.form("login_form"):
        username = st.text_input("Identifiant", key="username_input")
        password = st.text_input("Mot de passe", type="password", key="password_input")
        submitted = st.form_submit_button("Se connecter")

        if submitted:
            is_valid, role = check_password(username, password)
            if is_valid:
                st.session_state["authenticated"] = True
                st.session_state["role"] = role
                st.session_state["main_section_auth"] = (
                    "Accueil"  # Initialisation forcée
                )
                st.rerun()
            else:
                st.sidebar.error("Identifiant ou mot de passe incorrect.")


# =========================================================================
# 🚀 SECTION 5 : FONCTION PRINCIPALE (MAIN)
# =========================================================================


def init_session_state():
    defaults = {
        "authenticated": False,
        "role": "PUBLIC",
        "main_section_auth": "Accueil",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main():
    """Fonction principale de l'application Streamlit."""
    st.set_page_config(
        page_title="MSA - Midwifery Services App",
        page_icon="🌸",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 1. Initialisation
    init_session_state()

    # 2. Gestion de l'état
    if st.session_state["authenticated"]:
        role = st.session_state["role"]
        render_sidebar_auth(role)

        selected_section = st.session_state.get("main_section_auth", "Accueil")
        render_section(selected_section, role)
    else:
        render_login_form()
        render_public_header()
        render_info_section()


if __name__ == "__main__":
    main()
