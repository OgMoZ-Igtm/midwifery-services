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
import folium
from streamlit_folium import st_folium


# --- Imports des Fonctions/Formulaires Partagés ---
from modules.shared.form_carrousel_soins import (
    render_carrousel_soins_form,
    render_bebe_pleure,
)

# --- Registre centralisé des formulaires et dashboards ---
from modules.public.form_registry import (
    get_forms_for_role,
    get_all_registries,
    get_dashboards_for_role,
    get_shared_forms,  # ← ajouté pour les formulaires partagés
)

from modules.public.form_registry import get_shared_forms
from modules.utils.form_loader import (
    load_form,
    get_form_functions,
)  # si tu as une fonction utilitaire pour charger un module


# --- Fonction générique pour charger un formulaire ---
def load_form(module_path: str):
    """
    Charge dynamiquement un formulaire à partir de son chemin de module.
    Chaque module doit exposer une fonction `render_form()`.
    """
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, "render_form"):
            module.render_form()
        else:
            st.warning(f"⚠️ Le module {module_path} n'a pas de fonction render_form().")
    except Exception as e:
        st.error(f"Erreur lors du chargement du formulaire {module_path}: {e}")


# --- Fonction générique pour charger un dashboard ---
def load_dashboard(module_path: str):
    """
    Charge dynamiquement un dashboard à partir de son chemin de module.
    Chaque module doit exposer une fonction de rendu (ex: render_dashboard_*).
    """
    try:
        module_name, func_name = module_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        renderer = getattr(module, func_name, None)
        if callable(renderer):
            renderer()
        else:
            st.warning(f"⚠️ Le module {module_path} n'a pas de fonction valide.")
    except Exception as e:
        st.error(f"Erreur lors du chargement du dashboard {module_path}: {e}")


# =========================================================================
# 📦 SECTION 1 : IMPORTS NÉCESSAIRES
# =========================================================================


def render_weather_map():
    """Affiche une carte météo ou un placeholder."""
    st.subheader("🌦️ Carte météo")
    st.info("La fonctionnalité météo sera bientôt disponible.")


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
        for key, config in get_forms_for_role(role).items():
            label = config.get("title", key)
            if st.button(f"📄 {label}", key=key):
                load_form(config["module"])

    # 🌐 FONCTIONS PARTAGÉES
    elif section == "Fonctions partagées":
        st.title("🌐 Fonctions partagées")
        for key, config in get_forms_for_role("SHARED").items():
            label = config.get("title", key)
            if st.button(f"🔗 {label}", key=key):
                load_form(config["module"])

    # 🧵 WORKSHOPS
    elif section == "Workshops":
        st.title("🧵 Ateliers & Carrousels")
        render_carrousel_soins_form()
        render_bebe_pleure()

    else:
        st.warning("⚠️ Section inconnue ou non implémentée.")


# =========================================================================
# ⚙️ SECTION 2 : CONSTANTES ET DONNÉES STATIQUES
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
        st.error(f"Image introuvable : {image_path}")
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
            slides += f"""
            <div class="swiper-slide">
                <h3>{fiche['titre']}</h3>
                <p>⚠️ Image introuvable ou chemin invalide.</p>
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
        <!-- Si vous voulez des flèches, ajoutez ceci: -->
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


def load_dashboard(role):
    """Charge dynamiquement le tableau de bord selon le rôle. (Logique conservée)"""
    try:
        # La logique de l'original est conservée mais le module n'existe pas,
        # on appelle donc directement le placeholder de la Section 2
        dashboard_func = globals().get(f"form_dashboard_{role.upper()}")
        if dashboard_func:
            dashboard_func()
        else:
            st.warning(f"Aucun tableau de bord trouvé pour le rôle {role}")

    except Exception:
        st.warning(f"Aucun tableau de bord trouvé pour le rôle {role}")


def load_form(module_path: str):
    """Charge dynamiquement le module et retourne sa fonction render_form()."""
    module = importlib.import_module(module_path)
    return getattr(module, "render_form")


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
        # Debug pour vérifier la correspondance rôle → chemin
        st.write(f"🔎 Rôle détecté: {role} → Chemin: {dashboard_path}")
        try:
            load_dashboard(dashboard_path)
        except Exception as e:
            st.error(f"Erreur lors du chargement du tableau de bord {role}: {e}")
    else:
        st.warning(f"⚠️ Aucun tableau de bord trouvé pour le rôle '{role}'.")

        # --- Suite logique : appel avec le rôle de l'utilisateur ---
        user_role = st.session_state.get("user_role", "GUEST")
        render_dashboard_section(user_role)


def render_workshops():
    """Affiche la section Workshops/Ateliers. (Logique conservée)"""
    st.title("🧵 Ateliers & Carrousels")
    st.markdown("### Leçon sur la vie et la culture")
    # L'original appelle render_bebe_pleure() via un commentaire, ici on l'inclut pour être conforme à la demande.
    render_bebe_pleure()
    st.markdown("---")
    # Le carrousel des soins est appelé via load_form
    load_form("modules.shared.form_carrousel_soins")


# --- Fonctions de rendu de la partie Publique (non-connectée) ---


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
                Veuillez utiliser votre rôle et votre mot de passe (Ex: MIDWIFE, admin123).
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
            st.session_state["info_page"] = "Tableau de bord"
            st.session_state["main_section_auth"] = (
                "Tableau de bord"  # Ajout pour la cohérence
            )
            st.session_state["login_time"] = (
                time.time()
            )  # Ajout pour initialiser l'heure de connexion
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
        render_info_section()

    # 🟥 Colonne droite : login et carrousel/expérience bébé
    with login_col:
        # Affiche le carrousel sur la page de connexion
        render_home_page()
        st.markdown("---")
        # Placeholder pour les messages de connexion
        message_placeholder = st.empty()
        handle_login_form(message_placeholder)

        # ✅ AJOUT DE LA VIDÉO EXPLICATIVE
        st.markdown("---")
        st.markdown("#### 📽️ Vidéo Explicative")

        # Appel direct avec chemin relatif (pas de / au début)
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
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "info_page" not in st.session_state:
        st.session_state["info_page"] = "Accueil"

    # Si l'utilisateur est déjà connecté, afficher le tableau de bord avec onglets
    if st.session_state.get("logged_in", False):
        st.success(f"Bienvenue, **{st.session_state.get('user_role', 'invité')}**!")
        st.button("Déconnexion", on_click=lambda: st.session_state.clear())

        st.header("📊 Tableau de bord de l'utilisateur")

        # --- Onglets Streamlit ---
        tab1, tab2, tab3, tab4 = st.tabs(
            ["👤 Profil", "📑 Formulaires", "🔔 Notifications", "📈 Statistiques"]
        )

        # 👤 Profil
        with tab1:
            st.subheader("Informations de session")
            st.write(
                {
                    "Utilisateur": st.session_state.get("username", "Anonyme"),
                    "Rôle": st.session_state.get("user_role", "Invité"),
                    "Dernière connexion": st.session_state.get(
                        "last_login", "Non disponible"
                    ),
                }
            )

        # 📑 Formulaires
        with tab2:
            st.subheader("Formulaires disponibles")
            role = st.session_state.get("user_role", "").upper()
            if role:
                from modules.public.form_registry import get_forms_for_role

                forms = get_forms_for_role(role)
                if forms:
                    for name, config in forms.items():
                        st.markdown(
                            f"- **{config.get('title', name)}** ({config.get('description', '')})"
                        )
                else:
                    st.info("Aucun formulaire disponible pour ce rôle.")
            else:
                st.info("Rôle non défini, aucun formulaire affiché.")

        # 🔔 Notifications
        with tab3:
            st.subheader("Notifications")
            st.write("✅ Vous n'avez aucune notification pour le moment.")

        # 📈 Statistiques
        with tab4:
            st.subheader("Statistiques")
            st.metric("Formulaires soumis", 12)
            st.metric("Dernière activité", "il y a 2 jours")

        return

    # ✅ Interface publique si non connecté
    render_public_header()
    render_public_content()


# =========================================================================
# 🧭 SECTION 5 : LOGIQUE PRINCIPALE DE L'APPLICATION (MAIN FLOW)
# =========================================================================


def render_sidebar():
    """Gère toute la logique de la barre latérale pour l'interface authentifiée."""

    # --- Barre latérale sacrée ---
    with st.sidebar:
        st.markdown("## 🌿 Navigation")
        st.markdown("#### Détails de Session")

        # Détails de connexion
        login_timestamp = st.session_state.get("login_time")
        if login_timestamp:
            # Assurez-vous que c'est un timestamp pour time.localtime
            # Le timestamp est déjà un float ici, pas besoin de .timestamp()
            login_dt = time.localtime(login_timestamp)
            st.markdown(
                f"**Connexion :** {time.strftime('%Y-%m-%d', login_dt)} à {time.strftime('%H:%M:%S', login_dt)}"
            )

        # Affichage de la dernière session (logique conservée)
        last_sess = normalize_session(st.session_state.get("last_session", {}))

        # Assurez-vous que les valeurs sont des floats (timestamps) pour time.localtime
        start_ts = (
            last_sess["start"].timestamp()
            if isinstance(last_sess["start"], datetime.datetime)
            else last_sess["start"]
        )
        end_ts = (
            last_sess["end"].timestamp()
            if isinstance(last_sess["end"], datetime.datetime)
            else last_sess["end"]
        )

        if start_ts and end_ts:
            start_dt = time.localtime(start_ts)
            end_dt = time.localtime(end_ts)
            st.markdown("---")
            st.markdown(f"**Dernière Session ({last_sess['role'].capitalize()})**:")
            st.markdown(f"Déb. : {time.strftime('%Y-%m-%d %H:%M:%S', start_dt)}")
            st.markdown(f"Fin : {time.strftime('%Y-%m-%d %H:%M:%S', end_dt)}")

            st.markdown("---")

        # --- Navigation dans la barre latérale (Que souhaitez-vous faire?) ---
        navigation_options = [
            "Accueil",
            "Tableau de bord",
            "Formulaires spécifiques",
            "Fonction partagée",
            "Workshops",
        ]

        # Initialisation sécurisée (logique conservée)
        if "main_section_auth" not in st.session_state:
            st.session_state["main_section_auth"] = "Accueil"

        # Sélecteur de navigation (logique conservée)
        st.session_state["main_section_auth"] = st.sidebar.radio(
            "🧭 Que souhaitez-vous afficher ?",
            navigation_options,
            index=navigation_options.index(
                st.session_state.get("main_section_auth", "Accueil")
            ),
        )

        # Séparateur visuel
        st.sidebar.markdown("---")

        # Bouton de déconnexion (logique conservée)
        if st.sidebar.button("🚪 Déconnexion"):
            # Enregistrement de la session
            st.session_state["last_session"] = {
                "role": st.session_state.get("user_role", "INVITÉ"),
                "start": st.session_state.get("login_time"),
                "end": time.time(),  # Capture l'heure de fin
            }
            # Nettoyage
            st.session_state["logged_in"] = False
            st.session_state["user_role"] = None
            st.session_state["info_page"] = "Accueil"
            st.session_state["selected_form"] = None
            st.session_state["login_time"] = None
            # st.toast("🌿 Vous avez quitté votre espace avec succès !", icon="🕊️") # Ligne commentée conservée
            st.rerun()


def main_authenticated_interface():
    """Interface pour les utilisateurs connectés."""
    render_sidebar()

    # --- Corps principal selon la section choisie (logique conservée) ---
    section = st.session_state["main_section_auth"]
    # role = st.session_state.get("user_role", "GUEST") # Non utilisé directement dans ce bloc

    # 🏠 ACCUEIL
    if section == "Accueil":
        st.title("🌸 Bienvenue dans MSA !")
        st.markdown("Un lieu de soin, de culture et de célébration partagée.")

        # 🎠 Carrousel culturel (logique conservée)
        st.markdown("### 🎠 Fiches culturelles")
        carousel_html = generate_carousel_html(fiches)
        st.components.v1.html(carousel_html, height=650, scrolling=False)

        # 🌤️ Carte météo interactive (logique conservée)
        st.markdown("### ☀️ Météo des communautés")
        if folium and st_folium:
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
                    popup = f"{name}<br>{icon} {weather['temp']}°C<br>Vent: {weather['wind']} km/h"
                    folium.Marker(
                        location=[info["lat"], info["lon"]],
                        popup=popup,
                        icon=folium.Icon(color=info["color"], icon="cloud"),
                    ).add_to(m)
            st_folium(m, width=700, height=450)
        else:
            st.warning(
                "Veuillez installer folium et streamlit-folium pour afficher la carte météo."
            )


# --- Section publique ---


def render_info_section():
    """Affiche la section publique sélectionnée (PUBLIC) depuis le registre centralisé."""
    public_forms = get_form_functions("PUBLIC")

    # Par défaut, on tombe sur 'accueil'
    current_page = st.session_state.get("info_page", "accueil")

    if current_page not in public_forms:
        st.error(f"⚠️ Page '{current_page}' non trouvée dans le registre PUBLIC.")
        return

    module_path = public_forms[current_page]
    st.header(f"📖 {current_page.capitalize()}")
    load_form(module_path)


# --- Section partagée ---


def render_shared_section():
    """Affiche les formulaires partagés (SHARED) depuis le registre centralisé."""
    shared_forms = get_form_functions("SHARED")

    if not shared_forms:
        st.warning("⚠️ Aucun formulaire partagé disponible pour l'instant.")
        return

    # --- Navigation dynamique ---
    sub_choice = st.radio(
        "Choisir un formulaire partagé",
        list(shared_forms.keys()),  # affiche les titres (Agenda, Calendrier, etc.)
        key="shared_forms_navigation",
    )

    # --- Affichage du titre et du contenu ---
    st.header(f"🤝 {sub_choice}")
    module_path = shared_forms[sub_choice]
    load_form(module_path)

    # 📊 TABLEAU DE BORD

    section = st.session_state["main_section_auth"]
    role = st.session_state.get("user_role", "GUEST")

    render_section(section, role)

    # 🌈 Transitions animées (CSS conservé)
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

    # ✅ Validation du rôle et des modules (logique conservée)
    config = {
        "module": "form_utility_general_contact",  # ou le module que tu veux tester
        "page_id": "PAGE_ID_UTILITY_CONTACT_FORM",
    }
    if is_valid_module(config["module"]):
        # load_form(config["module"]) # Commenté car l'appel est incorrect hors des sections
        pass
    else:
        # st.warning("Ce module n’est pas encore disponible.") # Commenté pour ne pas polluer l'interface
        pass  # Laisse le pass original


# --- BLOC DE DÉMARRAGE PRINCIPAL DE L'APPLICATION ---
if __name__ == "__main__":
    # Configuration de la page
    st.set_page_config(
        page_title="MSA - Midwifery Services Application",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialisation de la session (logique conservée/complétée)
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = "GUEST"
    if "info_page" not in st.session_state:
        st.session_state["info_page"] = "Accueil"
    if "main_section_auth" not in st.session_state:
        st.session_state["main_section_auth"] = "Accueil"
    if "login_time" not in st.session_state:
        st.session_state["login_time"] = (
            None  # Initialisé à None, pas à time.time() pour le public
        )

    # --- Routeur Principal ---
    # Détermine l'interface à afficher
    if st.session_state.get("logged_in", False):
        main_authenticated_interface()
    else:
        main_public_interface()
