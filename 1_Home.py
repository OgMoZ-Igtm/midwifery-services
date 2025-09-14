import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.security import est_autorise
from utils.weather import (
    get_current_weather,
    get_forecast,
    WEATHER_ICONS,
    CREE_CONDITIONS,
)
from utils.logger import log_action


# ======================================================
# ⚙️ Configuration de la page et Contrôle d'accès
# ======================================================
st.set_page_config(page_title="Accueil", page_icon="🏠")


# Initialisation de l'état d'authentification
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Redirection vers la page "home" si nécessaire
if st.session_state.get("current_page") != "home":
    st.session_state.current_page = "home"
    st.success("Connexion réussie. Redirection en cours...")
    st.rerun()

    # # Contrôle d’accès : accès réservé aux utilisateurs authentifiés
    # if not st.session_state.get("authenticated", False):
    #     st.warning("⛔ Accès refusé. Veuillez vous connecter.")
    #     st.stop()

    # ======================================================
    # 🏠 PAGE D'ACCUEIL
    # ======================================================
    """
    Fonction principale pour afficher le contenu de la page d'accueil.
    """


def page_home():
    st.set_page_config(page_title="🏠 Accueil", page_icon="🏠")
    st.title("Bienvenue dans Midwifery Tool")

    if "user_info" in st.session_state:
        user = st.session_state.user_info
        st.success(f"Bonjour {user['prenom']} ({user['role']})")
    elif "username" in st.session_state:
        st.success(f"Bonjour {st.session_state.username} ({st.session_state.role})")
    else:
        st.warning("Utilisateur non identifié.")

    if st.button("🔓 Se déconnecter"):
        st.session_state.authenticated = False
        st.session_state.clear()
        st.rerun()


st.markdown(
    "Explorez les services, les données et les communautés avec respect et engagement."
)


# --- Fonctions et données statiques (inchangées) ---
def play_baby_sound():
    if "mute" not in st.session_state:
        st.session_state.mute = False
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(
            "🔇 Couper le son" if not st.session_state.mute else "🔊 Activer le son"
        ):
            st.session_state.mute = not st.session_state.mute
    if not st.session_state.mute:
        play_audio("utils/bebe_pleure.mp3")


def connecter_utilisateur(username: str, password: str, role: str) -> bool:
    """
    Vérifie les identifiants et connecte l'utilisateur si valide.
    Retourne True si la connexion est réussie, False sinon.
    """
    utilisateur = verify_user(username, role)
    if utilisateur and bcrypt.checkpw(password.encode(), utilisateur[3]):
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = role
        st.session_state.utilisateur = utilisateur
        st.success("✅ Connexion réussie.")
        st.switch_page("modules/Home.py")  # ← adapte le chemin si nécessaire
        return True
    else:
        st.error("❌ Identifiants incorrects ou rôle non autorisé.")
        return False


def render_menus():
    st.title("👩‍🍼 Suivi des mamans et bébés")

    # 📸 Galerie horizontale
    cols = st.columns(6)
    images = [
        "static/mere_crie.jpg",
        "static/mother_baby.jpg",
        "static/accueil_territoire.jpg",
        "static/grand_mere_et_enfant.jpg",
    ]
    for i, img in enumerate(images):
        with cols[i]:
            st.image(img, use_column_width=True)

    # 📊 Barre de progression
    st.progress(0.6)  # Exemple : 60% complété


# # ======================================================
# # 📸 Carrousel de photos
# # ======================================================
# st.markdown("---")
# st.markdown("### 📽️ Moments culturels Cri")
# photos = [
#     "https://upload.wikimedia.org/wikipedia/commons/3/3e/Mistissini_Lake.jpg",
#     "https://i.ibb.co/6P07X2P/image-from-waskaganish-website.png",
#     "https://i.ibb.co/3WqPq5B/chisasibi-tepee.jpg",
#     "https://i.ibb.co/y4L2y7M/cree-community-maps-website.png",
# ]
# # `st.selectbox` pour choisir une photo, ajusté pour l'indexation
# selected = st.selectbox("🖼️ Choisissez une photo :", list(range(1, len(photos) + 1)))
# st.image(photos[selected - 1], use_column_width=True)

# ======================================================
# ⚡ Barre d’accès rapide
# ======================================================
st.markdown("---")
st.subheader("⚡ Accès rapide")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("👩‍⚕️ Suivi patientes"):
        st.switch_page("modules/Patients_Suivi.py")
with col2:
    if st.button("📨 Messages"):
        st.switch_page("modules/Messages_Inbox.py")
with col3:
    if st.button("📊 Rapports"):
        st.switch_page("modules/Statistics.py")
with col4:
    if st.button("⚙️ Administration") and role == "admin":
        st.switch_page("modules/Admin_Dashboard.py")

# ======================================================
# 🌦️ Météo en temps réel et prévisions
# ======================================================
st.markdown("---")
st.subheader("🌦️ Météo des communautés")
COMMUNITIES = {
    "Mistissini": (50.426, -73.882),
    "Chisasibi": (53.666, -78.792),
    "Waskaganish": (51.733, -78.757),
}
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

st.subheader("📅 Prévisions 3 jours")
for name, coords in COMMUNITIES.items():
    st.markdown(f"### {name}")
    forecasts = get_forecast(*coords, days=3)
    if forecasts:
        for f in forecasts:
            icon = WEATHER_ICONS.get(f["weather_code"], "🌤️")
            cree_cond = CREE_CONDITIONS.get(f["weather_code"], "")
            st.write(
                f"📆 {f['date']} | 🌡️ {f['temp_min']}°C - {f['temp_max']}°C | "
                f"{icon} {cree_cond}"
            )
    else:
        st.warning(f"⚠️ Pas de prévisions disponibles pour {name}")

# ======================================================
# 🗺️ Carte interactive
# ======================================================
st.markdown("---")
st.subheader("🗺️ Carte des communautés")
map = folium.Map(location=[51.5, -78.7], zoom_start=5)
folium.Marker([50.423, -73.857], tooltip="Mistissini").add_to(map)
folium.Marker([53.8, -78.9], tooltip="Chisasibi").add_to(map)
folium.Marker([51.5, -78.7], tooltip="Waskaganish").add_to(map)
st_folium(map, width=700, height=400)

# ======================================================
# 📅 Prochains rendez-vous
# ======================================================
st.markdown("---")
st.subheader("📅 Prochains rendez-vous")
# 🌤️ Météo locale en cri par communauté
st.markdown("---")
st.subheader("🌤️ Météo locale par communauté")


# Sélection de la communauté
communaute = st.selectbox(
    "Choisissez votre communauté :", ["Mistissini", "Waskaganish", "Chisasibi"]
)

# Coordonnées GPS par communauté
coordonnees = {
    "Mistissini": (50.4184, -73.8693),
    "Waskaganish": (51.4800, -78.7500),
    "Chisasibi": (53.8050, -78.9167),
}

lat, lon = coordonnees.get(communaute, (50.4184, -73.8693))  # par défaut Mistissini

# Appel météo
weather = get_current_weather(lat, lon)

if weather:
    code = weather["weather_code"]
    temp = weather["temp"]
    wind = weather["wind"]

    icon = WEATHER_ICONS.get(code, "❔")
    cri = CREE_CONDITIONS.get(code, "Inconnu")

    # Message personnalisé selon le rôle
    role = None
    if "user_info" in st.session_state:
        role = st.session_state.user_info.get("role")
    elif "role" in st.session_state:
        role = st.session_state.role

    # if not st.session_state.get("authenticated", False):
    #     st.warning("⛔ Accès refusé. Veuillez vous connecter.")
    #     st.stop()

    if role == "midwife":
        st.info(
            f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n🌾 À {communaute}, prévoyez vos déplacements pour les accouchements."
        )
    elif role == "doctor":
        st.info(
            f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n🩺 À {communaute}, météo à surveiller pour les visites à domicile."
        )
    elif role == "nurse":
        st.info(
            f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n💉 À {communaute}, la clinique mobile aura lieu sous {cri.lower()}."
        )
    elif role == "patient":
        st.info(
            f"{icon} **{cri}** — {temp}°C, vent {wind} km/h.\n🧑‍🍼 À {communaute}, météo prévue pour votre rendez-vous : {cri.lower()}."
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
col1.metric("💉 Vaccination", "78%", "↑ 5%")
col2.metric("🍼 Allaitement", "65%", "↔ Stable")
col3.metric("⚠️ Complications", "12%", "↓ 2%")

# ======================================================
# 🔔 Notifications
# ======================================================
st.markdown("---")
st.subheader("🔔 Notifications")
st.warning("📨 Vous avez 2 messages non lus.")
st.info("📅 Rappel : réunion avec l’équipe demain à 9h.")

# ======================================================
# 🎥 Vidéo explicative
# ======================================================
st.markdown("---")
st.subheader("🎥 Vidéo explicative")
st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# -----------------------------------------------------
# 📑 Logging
# -----------------------------------------------------
log_action(
    st.session_state.get("utilisateur", ["", "", ""])[2],
    role if role else "inconnu",
    "Accès à la page Home",
)


if not st.session_state.get("authenticated", False):
    st.warning("⛔ Accès refusé. Veuillez vous connecter.")
    st.stop()

# ======================================================
# Lancer l'application
# ======================================================
if __name__ == "__main__":
    page_home()
