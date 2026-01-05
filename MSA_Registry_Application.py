# 🌿 MSA_Application.py

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

from modules.public.form_registry import get_shared_forms

# L'import de form_loader est redondant avec les fonctions locales, mais maintenu pour la structure
from modules.utils.form_loader import (
    load_form as _load_form_util,  # Renommé pour éviter le conflit avec la fonction locale
    get_form_functions,
)


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
# 📦 SECTION 1 :
# =========================================================================
import folium
import requests
import streamlit as st
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd

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


def render_cultural_carousel():
    """Carrousel automatique des fiches culturelles (défilement toutes les 6 secondes)."""
    st.subheader("📚 Fiches culturelles")

    placeholder = st.empty()

    # Boucle sur les fiches
    for key, fiche in fiches.items():
        with placeholder.container():
            st.image(fiche["image"], use_column_width=True)
            st.markdown(f"### {fiche['titre']}")
            st.write(fiche["description"])
            st.caption(fiche["citation"])
        time.sleep(6)  # ⏱️ Attente de 6 secondes avant de passer à la fiche suivante


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


def render_section(section: str, role: str):
    """Affiche le contenu principal selon la section choisie."""

    # 🏠 ACCUEIL
    if section == "Accueil":
        st.title("🌸 Bienvenue dans MSA !")
        st.markdown("Un lieu de soin, de culture et de célébration partagée.")
        render_weather_map()

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
script_dir = os.path.dirname(os.path.abspath(__file__))
# Note : Les chemins d'images sont simulés ou nécessitent d'exister dans le dossier 'static'
fiches = {
    "Transmission des savoirs": {
        "titre": "Transmission des savoirs",
        # Simuler un chemin inexistant ou remplacer par un chemin réel
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


def image_to_base64(image_path):
    """Convertit une image en chaîne base64."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = os.path.splitext(image_path)[1][1:]
            ext_mime = ext if ext else "png"
            return f"data:image/{ext_mime};base64,{encoded}"
    else:
        # st.error(f"Image introuvable : {image_path}") # Afficher l'erreur peut perturber le flux Streamlit
        return None


def generate_carousel_html(fiches):
    """Génère le HTML du carrousel culturel. (Logique conservée)"""
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
            # Remplacer par un placeholder si l'image n'est pas trouvée
            slides += f"""
            <div class="swiper-slide" style="display:flex; flex-direction:column; justify-content:center;">
                <h3>{fiche['titre']}</h3>
                <div style="height:260px; background-color:#F0F0F0; border-radius:10px; display:flex; align-items:center; justify-content:center;">
                    Image Indisponible
                </div>
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
            direction: rtl; /* RTL comme demandé */
        }}
        .swiper-slide {{
            text-align: center;
            font-size: 18px;
            background: #fff;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-radius: 15px;
        }}
        .swiper-slide h3 {{ color: #d63384; }}
        .swiper-slide blockquote {{ border-left: 5px solid #ffb6c1; padding-left: 10px; margin: 15px 0; }}

    </style>
    <div class="swiper">
        <div class="swiper-wrapper">
            {slides}
        </div>
        <div class="swiper-button-prev" style="color:#d63384;"></div>
        <div class="swiper-button-next" style="color:#d63384;"></div>
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
            navigation: {{
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            }},
        }});
    </script>
    """
    return html_code


def render_bebe_experience():
    """Affiche l'animation du nouveau-né et le son (version simulée). (Logique conservée)"""
    # Note: L'audio 'bebe_pleure.mp3' est simulé par un message visuel ici.
    st.markdown(
        """
        <div style="border: 2px solid #ffb6c1; border-radius: 12px; padding: 1rem; background-color: #fff0f5;">
            <h3 style="color:#d63384;">👶 Le souffle de la vie</h3>
            <div id="typewriter" style="font-size:1.1rem; font-family:monospace; color:#333;"></div>
        </div>
        <script>
        const text = "Un nouveau-né pleure doucement... et le monde s’éveille avec tendresse. (Son de bebe_pleure.mp3 simulé)";
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                document.getElementById("typewriter").innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        // Utilisation d'un drapeau pour éviter l'exécution multiple dans Streamlit
        if (document.getElementById("typewriter") && !document.getElementById("typewriter").getAttribute("data-typed")) {
            typeWriter();
            document.getElementById("typewriter").setAttribute("data-typed", "true");
        }
        </script>
    """,
        unsafe_allow_html=True,
    )
    # L'audio réel nécessiterait un fichier accessible
    # st.audio(audio_path, format="audio/mp3")


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


# Nouvelle fonction pour gérer l'affichage de l'information publique (corrigé point 3)


# def render_info_section():
#     """Affiche le contenu de la page d'information publique sélectionnée (Accueil, À propos, etc.)."""
#     page_key = st.session_state.get("info_page", "accueil")

#     public_forms = get_forms_for_role("PUBLIC")
#     config = public_forms.get(page_key)

#     st.subheader(
#         f"Informations Publiques : {config.get('title', page_key).capitalize()}"
#     )
#     st.markdown("---")

#     if page_key == "accueil":
#         # --- Page d'accueil ---
#         render_home_page()

#         # --- Carrousel des fiches culturelles ---
#         render_cultural_carousel()

#         # --- Son de bébé qui pleure ---
#         st.audio(
#             os.path.join(script_dir, "static", "bebe_pleure.mp3"),
#             format="audio/mp3",
#             start_time=0,
#         )

#         # --- Carte météo des trois communautés ---
#         render_weather_map()

#         # --- Mission ---
#         st.markdown("### Notre Mission")
#         st.write(
#             "MSA est une plateforme dédiée au soutien de la maternité et du bien-être des familles crie, "
#             "en intégrant les savoirs ancestraux aux pratiques modernes."
#         )

#     elif config and config.get("module"):
#         # Correction : Tente de charger le VRAI formulaire public (si le module est défini)
#         try:
#             render_func = load_form_renderer(config["module"])
#             render_func()
#         except Exception as e:
#             st.error(
#                 f"❌ Erreur lors du chargement du formulaire public `{config.get('title', page_key)}` "
#                 f"depuis le module `{config.get('module')}`: {e}"
#             )

#     else:
#         st.error("Page d'information publique inconnue ou manquante.")


def render_info_section():
    """Affiche le contenu de la page d'information publique sélectionnée (Accueil, À propos, etc.)."""
    page_key = st.session_state.get("info_page", "accueil")

    public_forms = get_forms_for_role("PUBLIC")
    config = public_forms.get(page_key)

    st.subheader(
        f"Informations Publiques : {config.get('title', page_key).capitalize()}"
    )
    st.markdown("---")

    if page_key == "accueil":
        render_home_page()
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
        st.warning("⚠️ Aucun formulaire public disponible pour l'instant.")


def render_home_page():
    """Affiche le carrousel et le squelette de la page de présentation (dans la colonne de gauche). (Logique conservée)"""
    # --- Carrousel Dynamique (HTML/JS simulé pour le login) ---
    CAROUSEL_HTML = f"""
    <style>
        .carousel-container {{
            overflow: hidden;
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }}
        .carousel-track {{
            display: flex;
            transition: transform 1s ease-in-out;
            width: 300%;
        }}
        .carousel-item {{
            min-width: 33.33%;
            box-sizing: border-box;
        }}
        .carousel-item img {{
            width: 100%;
            height: 400px;
            display: block;
            object-fit: cover;
            border-radius: 8px;
        }}
    </style>
    <div class="carousel-container">
        <div class="carousel-track" id="msa-carousel-track">
            <div class="carousel-item"><img src="{load_static_asset('img_1')}" alt="Image 1"></div>
            <div class="carousel-item"><img src="{load_static_asset('img_2')}" alt="Image 2"></div>
            <div class="carousel-item"><img src="{load_static_asset('img_3')}" alt="Image 3"></div>
        </div>
    </div>
    <script>
        const track = document.getElementById('msa-carousel-track');
        if (track && !window.msaCarouselInterval) {{
            let currentIdx = 0;
            const totalItems = 3;
            const intervalTime = 6000;

            window.msaCarouselInterval = setInterval(() => {{
                currentIdx = (currentIdx + 1) % totalItems;
                const offset = -currentIdx * 100 / totalItems;

                track.style.transform = `translateX(${{offset}}%)`;
            }}, intervalTime);
        }}
    </script>
    """
    st.markdown(CAROUSEL_HTML, unsafe_allow_html=True)


def handle_login_form(message_placeholder):
    """Affiche et gère le formulaire de connexion. (Logique conservée)"""
    # CSS pour styliser le bloc de connexion
    st.markdown(
        """
        <style>
        .login-box {
            padding: 20px;
            border-radius: 15px;
            border: 3px solid #FFD1DC; /* Bordure rose douce */
            background-color: #FFF0F5; /* Fond rose très clair */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .login-box .stTextInput > div > div > input, .login-box .stButton > button {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("🏠 Bienvenue dans MSA !❤️")

        with st.form("msa_login_form", clear_on_submit=True):
            st.markdown(
                """
                <p style="font-size:1rem; color:#d63384; font-style:italic;">
                Veuillez utiliser votre rôle et votre mot de passe (Ex: MIDWIFE, DOCTOR, ADMIN...).
                </p>
                """,
                unsafe_allow_html=True,
            )

            username = st.text_input(
                "Identifiant (rôle)",
                placeholder="Ex: MIDWIFE, DOCTOR, ADMIN...",
            ).upper()

            password = st.text_input("Mot de passe", type="password")
            submitted = st.form_submit_button("Se connecter", type="primary")

        st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        role = username.upper()
        if role in USER_PASSWORDS and password == USER_PASSWORDS[role]:
            message_placeholder.success(
                f"✅ Connexion réussie en tant que **{role}**. Redirection..."
            )
            # Mise à jour de l'état de la session pour la connexion
            st.session_state["user_role"] = role
            st.session_state["logged_in"] = True
            # Correction : L'interface connectée doit pointer vers "Tableau de bord" par défaut
            st.session_state["main_section_auth"] = "Tableau de bord"
            st.session_state["login_time"] = time.time()
            time.sleep(0.5)
            st.rerun()
        else:
            message_placeholder.error("⛔ Identifiant ou mot de passe incorrect.")


def render_public_content():
    """Affiche l'interface publique (contenu + login). (Logique conservée + AJOUT VIDÉO)"""
    # ✅ définir les colonnes ici
    content_col, login_col = st.columns([2, 1])

    # 🟦 Colonne gauche : contenu public
    with content_col:
        # Correction : Affiche le contenu sélectionné par les boutons publics
        render_info_section()

    # 🟥 Colonne droite : login et carrousel/expérience bébé
    with login_col:
        # Affiche le carrousel sur la page de connexion
        # Correction: La fonction render_home_page contient déjà le carrousel
        # render_home_page()
        st.markdown("---")
        # Placeholder pour les messages de connexion
        message_placeholder = st.empty()
        handle_login_form(message_placeholder)

        # ✅ AJOUT DE LA VIDÉO EXPLICATIVE - Remplacement du placeholder
        st.markdown("---")
        st.markdown("#### 📽️ Vidéo Explicative")

        # Activation du vrai composant vidéo
        st.video("static/mov_bbb.mp4", format="video/mp4", start_time=0)

        st.markdown(
            """
            <p style="font-size:0.8rem; color:gray;">
            Cette vidéo présente le fonctionnement de l'application et les procédures de connexion.
            </p>
            """,
            unsafe_allow_html=True,
        )


def main_public_interface():
    """Point d'entrée de l'interface publique (non-connectée)."""
    # Initialisation de l'état de session si manquant
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "info_page" not in st.session_state:
        st.session_state["info_page"] = (
            "accueil"  # Clé en minuscule pour cohérence avec le registre
        )
    if "main_section_auth" not in st.session_state:
        st.session_state["main_section_auth"] = "Accueil"
    if "active_form" in st.session_state:
        del st.session_state["active_form"]

    st.set_page_config(
        page_title="MSA - Midwifery Services Application",
        page_icon="🌸",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Rendu de l'en-tête public (boutons Accueil, À propos, etc.)
    render_public_header()
    st.markdown("---")

    # Rendu du contenu principal de la page publique
    render_public_content()


# =========================================================================
# 🚀 SECTION 5 : POINT D'ENTRÉE DE L'APPLICATION
# =========================================================================


def main_authenticated_interface(user_role):
    # Toujours définir la section courante avant de l'utiliser
    current_section = st.session_state.get("main_section_auth", "Accueil")

    # --- Sidebar pour la navigation ---
    with st.sidebar:
        st.image(load_static_asset("logo"))
        st.title("MSA Navigation")

        # --- Salutations dynamiques ---
        now = datetime.datetime.now()
        hour = now.hour
        if hour < 12:
            greeting = "Bonjour"
        elif 12 <= hour < 18:
            greeting = "Bon après-midi"
        else:
            greeting = "Bonsoir"

        st.caption(f"{greeting}, vous êtes connecté en tant que: **{user_role}**")
        st.markdown("---")

        # Définition des sections de navigation (à adapter selon les rôles)
        sections = [
            "Accueil",
            "Tableau de bord",
            "Formulaires spécifiques",
            "Fonctions partagées",
            "Workshops",
        ]

        # Boucle pour les sections
        for section in sections:
            is_active = section == current_section
            if st.button(
                label=section,
                key=f"nav_auth_{section}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                st.session_state["main_section_auth"] = section
                st.session_state["active_form"] = None
                st.session_state["active_shared_func"] = None
                st.rerun()

        st.markdown("---")

        # --- Bouton Retour à l'accueil distinct ---
        st.markdown(
            """
            <style>
            .home-button > button {
                background-color: #ff69b4 !important;  /* Rose vif */
                color: white !important;
                font-weight: bold;
                border-radius: 10px;
                font-size: 16px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "🏠 Retour à l'accueil", key="nav_auth_back_home", use_container_width=True
        ):
            st.session_state["main_section_auth"] = "Accueil"
            st.session_state["active_form"] = None
            st.session_state["active_shared_func"] = None
            st.rerun()

    # --- Contenu principal ---
    st.header(f"{current_section}")
    st.markdown("---")
    render_section(current_section, user_role)


# --- Le point de départ de l'application Streamlit ---
if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None

    # Applique un style global
    st.markdown(
        """
        <style>
        .stButton>button {
            border: 1px solid #ffb6c1;
            color: #d63384;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            border-color: #d63384;
            color: white;
            background-color: #d63384;
        }
        .st-emotion-cache-p5m8m3 { /* Streamlit container for sidebar */
            border-right: 5px solid #ffb6c1;
            padding-top: 50px;
        }
        .primary-section {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["logged_in"] and st.session_state["user_role"]:
        main_authenticated_interface(st.session_state["user_role"])
    else:
        main_public_interface()
