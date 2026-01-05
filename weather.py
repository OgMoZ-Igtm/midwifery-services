import requests
import os
import folium
import datetime
from streamlit_folium import st_folium
import streamlit as st
from streamlit.components.v1 import html

# from utils.constants import COMMUNITIES, WEATHER_ICONS, CREE_CONDITIONS


# 🌦️ Météo gratuite via Open-Meteo
def get_current_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()["current_weather"]
        return {
            "weather_code": data["weathercode"],
            "wind": round(data["windspeed"]),
            "temp": round(data["temperature"]),
        }
    except Exception as e:
        print(f"Erreur météo : {e}")
        return None


# 🚨 Détection des alertes météo critiques
def detect_weather_alerts(weather):
    alerts = []
    if not weather:
        return alerts
    temp = weather.get("temp")
    wind = weather.get("wind")
    code = weather.get("weather_code")
    if temp is not None and temp >= 35:
        alerts.append("🔥 Alerte chaleur extrême")
    if temp is not None and temp <= -20:
        alerts.append("🧊 Alerte froid intense")
    if wind is not None and wind >= 70:
        alerts.append("🌪️ Alerte tempête / vents violents")
    if code in [95, 96, 99]:
        alerts.append("⛈️ Alerte orage")
    return alerts


# 🟥 Bannière météo en haut de page
def display_weather_banner():
    critical_alerts = []
    for name, coords in COMMUNITIES.items():
        weather = get_current_weather(*coords)
        alerts = detect_weather_alerts(weather)
        for alert in alerts:
            critical_alerts.append(f"⚠️ {name} : {alert}")
    if critical_alerts:
        st.markdown(
            f"""
            <div style="background-color:#ffcccc;padding:15px;border-radius:10px;">
                <h4 style="color:#990000;">🚨 Alertes météo critiques</h4>
                <ul>
                    {''.join(f"<li>{a}</li>" for a in critical_alerts)}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


# 🔔 Alerte visuelle côté patient
def display_patient_weather_alert():
    weather = get_current_weather(51.2796, -73.7578)  # Mistissini
    alerts = detect_weather_alerts(weather)
    if alerts:
        st.markdown("## 🚨 Alerte météo pour votre région")
        for alert in alerts:
            st.error(f"⚠️ {alert}")
        html(
            """
        <div style="animation: blink 1s infinite; background-color:#ffcccc; padding:10px; border-radius:8px;">
            <strong style="color:#990000;">⚠️ Attention : Conditions météo critiques détectées</strong>
        </div>
        <style>
        @keyframes blink {
            0% {opacity: 1;}
            50% {opacity: 0.5;}
            100% {opacity: 1;}
        }
        </style>
        """,
            height=80,
        )


# 📊 Météo des communautés
def display_community_weather():
    with st.expander("🌦️ Météo des communautés", expanded=True):
        cols = st.columns(len(COMMUNITIES))
        for col, (name, coords) in zip(cols, COMMUNITIES.items()):
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


# 🗺️ Carte météo
def display_weather_map():
    with st.expander("🗺️ Carte des communautés", expanded=False):
        map = folium.Map(location=[51.5, -78.7], zoom_start=5)
        for name, coords in COMMUNITIES.items():
            weather = get_current_weather(*coords)
            if weather:
                icon = WEATHER_ICONS.get(weather["weather_code"], "❔")
                cree_cond = CREE_CONDITIONS.get(weather["weather_code"], "Inconnu")
                popup_html = (
                    f"<b>{name}</b><br>{icon} {cree_cond}<br>{weather['temp']}°C"
                )
            else:
                popup_html = f"<b>{name}</b><br>Météo indisponible"
            folium.Marker(
                location=coords,
                tooltip=name,
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color="red", icon="fa-baby", prefix="fa"),
            ).add_to(map)
        st_folium(map, width=700, height=400)


# =========================================================
# 🏠 VARIABLES ET RESSOURCES GLOBALES
# =========================================================

# Get the directory of the current script (modules/ui/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 📍 Coordonnées des communautés (ID pour l'API Environnement Canada)
COMMUNITIES_API = {
    "Mistissini": "QC/s0000305",
    "Chisasibi": "QC/s0000673",
    "Waskaganish": "QC/s0000326",
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

# Fiches pour le carrousel (NOTE : les chemins d'accès doivent exister :
# ../../static/...)
fiches = {
    "Transmission des savoirs": {
        "titre": "Transmission des savoirs",
        # Chemins basés sur la structure fournie (doit exister dans le
        # répertoire supérieur)
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
        # print(f"Warning: Image file not found at {image_path}") # Debug print
        return None


# Mise en cache pendant 10 minutes (décorateur Streamlit)
@st.cache_data(ttl=600)
def get_current_weather_ec(community_id: str):
    """
    Récupère et met en cache les données météo actuelles d'Environnement Canada.
    (Simulation d'extraction XML).
    """
    url = f"https://dd.weather.gc.ca/citypage_weather/xml/{community_id}_e.xml"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # SIMULATION d'extraction (doit être robuste pour une vraie
        # utilisation)
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

        # Nettoyage de la condition (ex: "Mostly Cloudly" devient "Mostly
        # Cloudy")
        clean_condition = " ".join(
            [word for word in condition.split() if word.isalpha()]
        )

        return {
            "temp": temp,
            "condition": clean_condition,
            "wind": wind,
        }
    except requests.exceptions.RequestException:
        # st.error("Erreur de requête à l'API météo.")
        return None
    except Exception:
        # st.error("Erreur lors du traitement des données météo.")
        return None


def generate_carousel_html(fiches):
    """Génère le code HTML/CSS/JS pour le carrousel Swiper."""
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
            <div class="swiper-slide" style="background-color:#f0f0f0; border-radius:15px;">
                <h3 style="color:#e74c3c;">{fiche['titre']}</h3>
                <p style="color:#c0392b;">⚠️ Image introuvable. Vérifiez le chemin: {fiche['image']}</p>
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
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .swiper-slide h3 {{
            color: #3498db;
            margin-bottom: 10px;
        }}
        img {{
            max-height: 350px;
            object-fit: cover;
        }}
    </style>
    <div class="swiper">
        <div class="swiper-wrapper">
            {slides}
        </div>
        <!-- Si vous voulez les flèches, ajoutez : -->
        <div class="swiper-button-next"></div>
        <div class="swiper-button-prev"></div>
        <div class="swiper-pagination"></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.js"></script>
    <script>
        const swiper = new Swiper('.swiper', {{
            loop: true,
            pagination: {{
                el: '.swiper-pagination',
                clickable: true,
            }},
            navigation: {{
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            }},
            autoplay: {{
                delay: 6000,
                disableOnInteraction: false,
            }},
        }});
    </script>
    """
    return html_code


def lecteur_audio():
    """
    Lecteur audio qui démarre automatiquement avec option d'arrêt/redémarrage.
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
                   function toggleAudio() {{
                       if (audio.paused) {{
                           audio.play();
                           document.getElementById('audioButton').innerText = '🔇 Couper le Son';
                       }} else {{
                           audio.pause();
                           document.getElementById('audioButton').innerText = '🔊 Rejouer le Son';
                       }}
                   }}
              </script>
              <div style='text-align:center; margin-top:10px;'>
                   <button id="audioButton" onclick="toggleAudio()" style='padding:8px 16px; font-size:16px; border-radius:8px; border:none; background-color:#3498db; color:white; cursor:pointer;'>🔇 Couper le Son</button>
              </div>
              <p style='text-align:center; font-size:12px; color:#555;'>Le son a démarré automatiquement. Cliquez pour le couper.</p>
              """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Fichier audio 'bebe_pleure.mp3' non trouvé pour le lecteur.")


# =========================================================
# 🚀 FONCTION PRINCIPALE D'AFFICHAGE DU TABLEAU DE BORD
# =========================================================


def display_dashboard_content(user_id: str, role: str):
    """
    Affiche le tableau de bord complet (Web App) avec le carrousel, la météo, etc.
    Ceci remplace la page d'accueil textuelle pour l'environnement Streamlit.
    """

    # --- Affichage du message de bienvenue ---
    now = datetime.now()
    heure = now.hour
    date_connexion = now.strftime("%A %d %B %Y")
    heure_connexion = now.strftime("%H:%M")

    salutation = (
        "Bonjour" if heure < 12 else "Bon après-midi" if heure < 18 else "Bonsoir"
    )

    st.markdown(
        f"""
### 👋 {salutation}, {user_id.split('@')[0]}
Vous êtes connecté en tant que **{role}**
🕒 Heure de connexion : **{heure_connexion}**
📅 Date : **{date_connexion}**
"""
    )
    st.markdown("---")
    st.title("🏡 Tableau de Bord du Territoire")

    # 🌟 Présentation du projet
    st.info(
        """
        Bienvenue sur votre espace de travail. Utilisez le menu latéral pour naviguer.
        Ci-dessous, retrouvez les informations culturelles, la météo locale et vos indicateurs clés.
        """
    )

    # 🎒 Packs culturels
    st.markdown("---")
    st.subheader("🎒 Packs culturels")
    st.markdown(
        "Explorez les récits, les chants et les savoirs transmis par les aînées."
    )

    # 👉 Carrousel HTML
    try:
        carousel_html = generate_carousel_html(fiches)
        components.html(carousel_html, height=550)
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
                delta_color="off",
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

    st_folium(map, width=700, height=400)

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

        # Personnalisation en fonction du rôle
        if role.upper() == "MIDWIFE":
            st.info(
                rf"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n🌾 À {communaute}, prévoyez vos déplacements pour les accouchements."
            )
        elif role.upper() == "PATIENT":
            st.info(
                rf"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n💖 À {communaute}, une météo douce pour une promenade avec bébé !"
            )
        else:
            st.warning(
                rf"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n❓ Météo affichée sans personnalisation du rôle."
            )
    else:
        st.error("Impossible de récupérer la météo d'Environnement Canada.")

    # ======================================================
    # 📊 Statistiques rapides
    # ======================================================
    st.markdown("---")
    st.subheader("📊 Statistiques rapides")
    col1, col2, col3 = st.columns(3)
    if role.upper() in ["MIDWIFE", "ADMIN", "DOCTOR", "NURSE"]:
        st.info("Statistiques professionnelles:")
        col1.metric("💉 Vaccination", "78%", "↑ 5%")
        col2.metric("🍼 Allaitement", "65%", "↔ Stable")
        col3.metric("⚠️ Complications", "12%", "↓ 2%")
    elif role.upper() == "PATIENT":
        st.info("Statistiques de suivi personnel:")
        col1.metric("❤️ Poids de bébé", "5,2 kg", "↑ 0,3 kg")
        col2.metric("💤 Heures de sommeil", "8h", "↔ Stable")
        col3.metric("🍏 Suivi nutritif", "Excellent", "↑")
    else:
        st.info("Aucune statistique disponible pour ce rôle.")

    # ======================================================
    # 🔔 Notifications
    # ======================================================
    st.markdown("---")
    st.subheader("🔔 Notifications")
    if role.upper() in ["MIDWIFE", "ADMIN"]:
        st.warning("📨 Vous avez 2 messages non lus.")
        st.info("📅 Rappel : réunion avec l’équipe demain à 9h.")
    elif role.upper() == "PATIENT":
        st.warning("🔔 Le suivi de votre bébé est prêt.")
        st.info("💡 Nouveaux articles de blog sur l'allaitement.")
    else:
        st.info("Aucune notification pour ce rôle.")

    # ======================================================
    # 🎥 Vidéo explicative et Audio
    # ======================================================
    st.markdown("---")
    st.subheader("🎥 Vidéo explicative")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    # Afficher le lecteur audio
    try:
        lecteur_audio()
    except Exception as e:
        st.error(f"Une erreur est survenue lors du chargement du lecteur audio: {e}")


def render_page():
    st.title("🏠 Tableau de Bord")
    st.write("Bienvenue sur le tableau de bord principal.")
    # Tu peux ajouter ici des graphiques, des KPIs, des liens, etc.


# =========================================================
# Lancement pour test local si besoin (optionnel)
# =========================================================
if __name__ == "__main__":
    # Pour tester ce composant Streamlit localement:
    # Sauvegardez ce fichier comme 'modules/ui/dashboard_page.py'
    # et lancez-le avec 'streamlit run modules/ui/dashboard_page.py'
    st.set_page_config(page_title="🌾 Accueil MIDWIFE", page_icon="🌾", layout="wide")
    st.title("Mode Test - Dashboard Page")
    st.warning(
        "Pour un test complet, assurez-vous que les fichiers statiques (images, audio) existent dans le dossier '../../static/'."
    )
    display_dashboard_content("utilisateur_test", "MIDWIFE")
