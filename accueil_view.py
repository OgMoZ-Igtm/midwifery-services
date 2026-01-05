# accueil/view.py/
# ⚠️ import cassé : streamlit as st
# ⚠️ import cassé : requests
# ⚠️ import cassé : os
# ⚠️ import cassé : time
# ⚠️ import cassé : uuid
# ⚠️ from PIL import Image
# ⚠️ from streamlit_folium import st_folium
# ⚠️ import cassé : folium
# ⚠️ import cassé : streamlit.components.v1 as components
# ⚠️ import cassé : base64
# ⚠️ from datetime import datetime
# ⚠️ from streamlit_carousel import carousel
from modules.tools.home import render_form

# ⚠️ import cassé : streamlit as st
# ← si ce fichier est bien défini ailleurs
from modules.tools.home import render_form
from modules.backend.supabase_client import supabase


def run_home():
    st.title("🏠 Bienvenue dans Midwifery Services Data COOL Collection")
    st.write("Page d’accueil personnalisée.")


render_page(st.session_state.role)

# =========================================================
# 🏠 VARIABLES ET RESSOURCES GLOBALES
# =========================================================

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# 📍 Coordonnées des communautés (ID pour l'API Environnement Canada)
COMMUNITIES_API = {
    "Mistissini": "QC/s0000305",  # Réel: Lac Mistissini (ou le plus proche)
    "Chisasibi": "QC/s0000673",  # Réel: Chisasibi
    "Waskaganish": "QC/s0000326",  # Réel: Waskaganish
}
COMMUNITIES_COORDS = {
    "Mistissini": (50.426, -73.882),
    "Chisasibi": (53.666, -78.792),
    "Waskaganish": (51.733, -78.757),
}

# 🧠 Traduction cri des conditions météo
CREE_CONDITIONS = {
    "Clear": "Wāwīpān",
    "Mostly Cloudy": "Mīna wāwīpān",
    "Cloudy": "Yūtin",
    "Fog": "Wāpiskāw mīna yūtin",
    "Light Rain": "Nipīhūn",
    "Rain": "Nipīhūn",
    "Snow": "Wāpiskāw",
    "Thunderstorm": "Nipīhūn mīna yūtin",
}
# 🌤️ Icônes météo
WEATHER_ICONS = {
    "Clear": "☀️",
    "Mostly Cloudy": "🌤️",
    "Cloudy": "☁️",
    "Fog": "🌫️",
    "Light Rain": "🌦️",
    "Rain": "🌧️",
    "Snow": "❄️",
    "Thunderstorm": "⛈️",
    "default": "❔",
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

# =========================================================
# 🛠️ FONCTIONS UTILITAIRES
# =========================================================


def image_to_base64(image_path):
    """Convertit une image/fichier en chaîne base64."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = os.path.splitext(image_path)[1][1:]
            # Retourne le type MIME correct pour l'HTML
            return (
                f"data:image/{ext};base64,{encoded}"
                if ext.lower() not in ["mp3"]
                else f"data:audio/mpeg;base64,{encoded}"
            )
    else:
        return None


@st.cache_data(ttl=600)  # Mise en cache pendant 10 minutes
def get_current_weather_ec(community_id: str):
    """
    Récupère et met en cache les données météo actuelles d'Environnement Canada
    via une API non officielle (Simulation d'extraction XML).
    """
    url = f"https://dd.weather.gc.ca/citypage_weather/xml/{community_id}_e.xml"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # SIMULATION d'extraction (à remplacer par une vraie analyse XML)
        temp_tag = '<temperature unitType="metric" unit="C">'
        condition_tag = "<condition>"
        wind_tag = '<wind speed unit="km/h">'

        temp = "N/A"
        condition = "Cloudy"  # Default
        wind = "N/A"

        if temp_tag in response.text:
            start = response.text.find(temp_tag) + len(temp_tag)
            end = response.text.find("</temperature>", start)
            temp = response.text[start:end].strip().split("<")[0]

        if condition_tag in response.text:
            start = response.text.find(condition_tag) + len(condition_tag)
            end = response.text.find("</condition>", start)
            condition = response.text[start:end].strip()

        if wind_tag in response.text:
            start = response.text.find(wind_tag) + len(wind_tag)
            end = response.text.find("</speed>", start)
            wind = response.text[start:end].strip()

        clean_condition = " ".join(
            [word for word in condition.split() if word.isalpha()]
        )

        return {
            "temp": temp,
            "condition": clean_condition,
            "wind": wind,
        }
    except requests.exceptions.RequestException:
        return None
    except Exception:
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


def render_form():
    # ⚠️ import cassé : streamlit as st

    st.title("🏠 Page d’accueil")
    st.write("Bienvenue sur le tableau de bord obstétrique.")


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


# st.markdown("### 📽️ Diaporama doux")

script_dir = os.path.dirname(os.path.abspath(__file__))
image_paths = [
    os.path.join(script_dir, "static", f"maman_bebe_{i}.jpg") for i in range(1, 7)
]

# # Initialiser l'index du carrousel
# if "carousel_index" not in st.session_state:
#     st.session_state.carousel_index = 0

# # Navigation
# col1, col2, col3 = st.columns([1, 6, 1])

# with col1:
#     if st.button("⬅️"):
#         st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(
#             image_paths
#         )

# with col3:
#     if st.button("➡️"):
#         st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(
#             image_paths
#         )

# # Affichage
# current_index = st.session_state.carousel_index
# st.image(
#     image_paths[current_index],
#     caption=f"Maman & Bébé {current_index + 1}",
#     use_column_width=True,
# )
# st.write("Un moment tendre et complice 💕")

# # # # 🎒 Packs culturels


# 📁 Dossier contenant les médias
media_dir = "/home/ygd/projets-midwifery-Services-backup/static"

# 📦 Définition des éléments du carrousel
carousel_items = [
    {
        "img": "Accueil_territoire.png",
        "title": "🌍 Accueil du territoire",
        "text": "Là où chaque pas est mémoire, chaque souffle est racine.",
    },
    {
        "img": "Ainee_berce_enfant.png",
        "title": "👵 L’aînée berce l’enfant",
        "text": "Le chant des générations traverse les bras.",
    },
    {
        "img": "Berceau_nature.png",
        "title": "🌿 Berceau de nature",
        "text": "La forêt veille, le vent murmure.",
    },
    {
        "img": "Grand_mere_et_enfant.png",
        "title": "💞 Grand-mère et enfant",
        "text": "Un regard, une histoire, un avenir.",
    },
    {
        "img": "Le_feu_sacre.png",
        "title": "🔥 Le feu sacré",
        "text": "L’esprit veille dans la chaleur du cercle.",
    },
    {
        "img": "Le_retour_attendu.png",
        "title": "🚶‍♀️ Le retour attendu",
        "text": "Chaque pas vers l’autre est une guérison.",
    },
]

# 🔊 Audio d’ambiance
audio_path = os.path.join(media_dir, "bebe_pleure.mp3")
if os.path.exists(audio_path):
    st.audio(audio_path)

# 🕹️ Contrôle du carrousel
st.markdown("### 📽️ Diaporama doux")
auto_mode = st.toggle("⏱️ Carrousel automatique", value=True)
duration = st.slider(
    "⏳ Durée entre les images (secondes)", min_value=2, max_value=15, value=5
)

# 🧠 Initialisation des états
if "carousel_index" not in st.session_state:
    st.session_state.carousel_index = 0
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# ⏳ Minuterie automatique
if auto_mode and time.time() - st.session_state.last_update > duration:
    st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(
        carousel_items
    )
    st.session_state.last_update = time.time()
    st.rerun()

# 🔁 Navigation manuelle
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️"):
        st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(
            carousel_items
        )
        st.session_state.last_update = time.time()
        st.rerun()
with col3:
    if st.button("➡️"):
        st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(
            carousel_items
        )
        st.session_state.last_update = time.time()
        st.rerun()

# 📸 Affichage de l’élément courant
current = carousel_items[st.session_state.carousel_index]
image_path = os.path.join(media_dir, current["img"])

if os.path.exists(image_path):
    st.image(Image.open(image_path), use_column_width=True)
    st.markdown(f"### {current['title']}")
    st.markdown(f"*{current['text']}*")
else:
    st.warning(f"Image introuvable : {current['img']}")


# Poème d’introduction
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
st.subheader("🌦️ Météo des communautés (Environnement Canada)")

cols = st.columns(len(COMMUNITIES_API))
for col, (name, api_id) in zip(cols, COMMUNITIES_API.items()):
    weather = get_current_weather_ec(api_id)
    if weather and weather.get("temp") != "N/A":
        condition = weather["condition"]
        icon = WEATHER_ICONS.get(condition, WEATHER_ICONS["default"])
        cree_cond = CREE_CONDITIONS.get(condition, condition)
        col.metric(
            label=name,
            value=f"{weather['temp']}°C {icon}",
            delta=cree_cond,
            delta_color="off",  # Évite la flèche up/down pour une traduction
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
    for name, coords in COMMUNITIES_COORDS.items():
        api_id = COMMUNITIES_API.get(name)
        weather = get_current_weather_ec(api_id)

        if weather and weather.get("temp") != "N/A":
            condition = weather["condition"]
            icon = WEATHER_ICONS.get(condition, "❔")
            cree_cond = CREE_CONDITIONS.get(condition, "Inconnu")
            popup_html = f"<b>{name}</b><br>{icon} {cree_cond}<br>{
                weather['temp']}°C"
        else:
            popup_html = f"<b>{name}</b><br>Météo indisponible (API EC)"

        folium.Marker(
            location=coords,
            tooltip=name,
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="red", icon="fa-baby", prefix="fa"),
        ).add_to(map)

    unique_key = f"map_{uuid.uuid4()}"
    st_folium(map, width=700, height=400, key=unique_key)

    # ======================================================
    # 📅 Prochains rendez-vous
    # ======================================================
    st.markdown("---")
    st.subheader("📅 Prochains rendez-vous")
    st.info("Aucun rendez-vous planifié pour aujourd'hui.")

    # 🌤️ Météo locale en cri par communauté (Détail)
    st.markdown("---")
    st.subheader("🌤️ Météo locale par communauté")
    communaute = st.selectbox(
        "Choisissez votre communauté :", ["Mistissini", "Waskaganish", "Chisasibi"]
    )
    api_id = COMMUNITIES_API.get(communaute)
    weather = get_current_weather_ec(api_id)

    if weather and weather.get("temp") != "N/A":
        condition = weather["condition"]
        temp = weather["temp"]
        wind = weather["wind"]
        icon = WEATHER_ICONS.get(condition, "❔")
        cri = CREE_CONDITIONS.get(condition, "Inconnu")

        if role == "MIDWIFE":
            st.info(
                f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n🌾 À {communaute}, prévoyez vos déplacements pour les accouchements."
            )
        elif role == "PATIENT":
            st.info(
                f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n💖 À {communaute}, une météo douce pour une promenade avec bébé !"
            )
        else:
            st.warning(
                f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n❓ Rôle non reconnu — météo affichée sans personnalisation."
            )
    else:
        st.error("Impossible de récupérer la météo d'Environnement Canada.")

    role = st.session_state.get("role", "guest")

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
    if role in ["MIDWIFE", "ADMIN"]:
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
    """
    Lecteur audio qui démarre automatiquement avec option d'arrêt/redémarrage.
    Minuterie intégrée pour couper le son après 15 secondes.
    """
    audio_path = os.path.join(script_dir, "..", "..", "static", "bebe_pleure.mp3")

    if os.path.exists(audio_path):
        audio_base64 = image_to_base64(audio_path)

        st.markdown("---")
        st.subheader("👶 Simulation : Bruit de fond")
        st.markdown(
            f"""
            <audio id="bebeAudio" autoplay loop>
                <source src="{audio_base64}" type="audio/mpeg">
                Votre navigateur ne supporte pas l'audio.
            </audio>
            <script>
                const audio = document.getElementById('bebeAudio');
                const button = document.getElementById('audioButton');

                function toggleAudio() {{
                    if (audio.paused) {{
                        audio.play();
                        button.innerText = '🔇 Couper le Son';
                    }} else {{
                        audio.pause();
                        button.innerText = '🔊 Rejouer le Son';
                    }}
                }}

                // ⏱️ Minuterie : couper le son après 15 secondes
                setTimeout(() => {{
                    if (!audio.paused) {{
                        audio.pause();
                        button.innerText = '🔊 Rejouer le Son';
                    }}
                }}, 15000);
            </script>
            <div style='text-align:center; margin-top:10px;'>
                <button id="audioButton" onclick="toggleAudio()" style='padding:8px 16px; font-size:16px;'>🔇 Couper le Son</button>
            </div>
            <p style='text-align:center; font-size:12px;'>Le son démarre automatiquement et s'arrêtera après 15 secondes.</p>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Fichier audio 'bebe_pleure.mp3' non trouvé pour le lecteur.")


# =========================================================
# 🚀 POINT D'ENTRÉE DE L'APPLICATION
# =========================================================
st.set_page_config(page_title="🌾 Accueil MIDWIFE", page_icon="🌾", layout="wide")

# Initialisation des variables de session nécessaires pour l'affichage
# (supposant qu'app.py les configure)
if "user_role" not in st.session_state:
    st.session_state.user_role = "GUEST"  # Rôle par défaut si non défini par app.py
if "user_name" not in st.session_state:
    st.session_state.user_name = "Invité"  # Nom par défaut si non défini par app.py
if "current_view" not in st.session_state:
    st.session_state.current_view = "Accueil"
if "redirect_counter" not in st.session_state:
    st.session_state.redirect_counter = 0

# --- Affichage du message de bienvenue et des informations de session ---
now = datetime.now()
heure = now.hour
date_connexion = now.strftime("%A %d %B %Y")
heure_connexion = now.strftime("%H:%M")

salutation = "Bonjour" if heure < 12 else "Bon après-midi" if heure < 18 else "Bonsoir"

st.markdown(
    f"""
### 👋 {salutation}, {st.session_state.user_name}
Vous êtes connecté en tant que **{st.session_state.user_role}**
🕒 Heure de connexion : **{heure_connexion}**
📅 Date : **{date_connexion}**
🗂️ Dernière connexion : *non enregistrée*
"""
)

# ======================================================
# 🎯 LOGIQUE DE REDIRECTION AUTOMATIQUE
# ======================================================
st.markdown("---")

# Placez le widget de délai et les boutons dans un conteneur pour la cohérence
with st.container(border=True):
    st.subheader("🚀 Accès Rapide au Tableau de Bord")
    col_delay, col_button_manual = st.columns([1, 2])

    # 1. Sélecteur de Délai
    delay = col_delay.number_input(
        "⏳ Délai (secondes) avant redirection :",
        min_value=0,
        max_value=10,
        value=5,
        step=1,
        key="redirect_delay",
        disabled=st.session_state.redirect_counter
        > 0,  # Désactiver pendant le compte à rebours
    )

    # 2. Bouton de Redirection Manuelle
    if col_button_manual.button(
        "Cliquez pour être redirigé vers votre tableau de bord",
        key="go_to_dashboard_manual",
    ):
        st.session_state.current_view = "🏠 Tableau de bord"
        st.toast(
            f"Redirection immédiate vers le tableau de bord ({
                st.session_state.user_role})..."
        )
        st.rerun()

    # 3. Message d'avertissement et Compte à Rebours
    if st.session_state.redirect_counter == 0 and delay > 0:
        # Démarrer le compte à rebours
        if st.button(
            f"Commencer le compte à rebours ({delay}s)", key="start_countdown"
        ):
            st.session_state.redirect_counter = delay
            st.rerun()

    if st.session_state.redirect_counter > 0:

        # Afficher la barre de progression et le message
        placeholder = st.empty()
        # Évite la division par zéro si delay est 0 (même si min_value est 0,
        # on gère le > 0 au démarrage)
        progress_value = st.session_state.redirect_counter / delay if delay > 0 else 1
        progress_bar = placeholder.progress(progress_value)

        alert_cols = st.columns([3, 1])
        alert_cols[0].warning(
            f"La redirection vers votre tableau de bord principal ({
                st.session_state.user_role}) se fera dans **{
                st.session_state.redirect_counter}** secondes."
        )

        if alert_cols[1].button("Annuler la Redirection", key="cancel_countdown"):
            st.session_state.redirect_counter = 0
            placeholder.empty()
            st.toast("Redirection annulée.")
            st.rerun()

        # Logique du compte à rebours : décrémenter et attendre
        if st.session_state.redirect_counter > 0:
            time.sleep(1)
            st.session_state.redirect_counter -= 1
            st.rerun()

        # Redirection finale
        if st.session_state.redirect_counter == 0:
            placeholder.empty()
            st.session_state.current_view = "🏠 Tableau de bord"
            st.toast("Redirection terminée.")
            st.rerun()

st.markdown("---")

# Afficher le contenu de la page
render_page(st.session_state.user_role)

# Afficher le lecteur audio
try:
    lecteur_audio()
except Exception as e:
    st.error(f"Une erreur est survenue lors du chargement du lecteur audio: {e}")
