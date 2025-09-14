import streamlit as st
from datetime import datetime
import os

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    username = st.session_state.get("username", "Inconnu")
    role = st.session_state.get("role", "Non défini")
    login_time = st.session_state.get("login_time")
    logout_time = st.session_state.get("logout_time")
    last_login = st.session_state.get("last_login")

    # Message d’accueil selon l’heure
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Bonjour"
    elif hour < 18:
        greeting = "Bon après-midi"
    else:
        greeting = "Bonsoir"

    st.title(f"{greeting}, {username} 👋")
    st.markdown(f"**Vous êtes connectée en tant que :** `{username}`")
    st.markdown(f"**Rôle :** `{role}`")

    st.markdown("---")
    st.subheader("🕒 Historique de session")

    if login_time:
        st.markdown(f"**Heure de connexion :** {login_time.strftime('%H:%M:%S')}")
    if logout_time:
        st.markdown(f"**Heure de déconnexion :** {logout_time.strftime('%H:%M:%S')}")
    if last_login:
        st.markdown(
            f"**Dernière connexion :** {last_login.strftime('%d %B %Y à %H:%M:%S')}"
        )

    st.markdown("---")
    st.subheader("📜 Historique d'accès")

    # Utiliser un chemin relatif et vérifier si le fichier existe
    log_file_path = "logs/access_log.txt"
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Simuler le contenu du fichier de log si il n'existe pas
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Démo : Connexion de {username}.\n")

    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            logs = f.readlines()
        user_logs = [line for line in logs if username in line]
        if user_logs:
            for line in reversed(user_logs[-20:]):
                st.markdown(f"- {line.strip()}")
        else:
            st.info("Aucun accès enregistré pour cet utilisateur.")
    except FileNotFoundError:
        st.warning("Le journal des accès est introuvable.")

    st.markdown("---")
    st.subheader("🖼️ Photo de profil")

    st.image("https://placehold.co/150x150/png?text=Avatar", width=100)
    uploaded_file = st.file_uploader(
        "📷 Téléversez votre photo de profil", type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        st.image(uploaded_file, width=150)

    if st.button("🛠️ Modifier mon profil"):
        st.session_state.edit_profile = True

    if st.session_state.get("edit_profile"):
        st.subheader("🔧 Édition du profil")

        new_username = st.text_input("Nom d'utilisateur", value=username)
        new_role = st.selectbox(
            "Rôle",
            options=[
                "ADMIN",
                "DOCTOR",
                "PATIENT",
                "MIDWIFE",
                "NURSE",
                "STUDENT",
                "DOCTORAL",
            ],
            index=0,
        )

        if st.button("💾 Enregistrer les modifications"):
            st.session_state.username = new_username
            st.session_state.role = new_role
            st.success("✅ Profil mis à jour avec succès.")
            st.session_state.edit_profile = False

    if "user_preferences" not in st.session_state:
        st.session_state.user_preferences = {
            "language": "Français",
            "theme": "Clair",
            "notifications": True,
        }

    st.subheader("⚙️ Préférences")

    langue = st.selectbox(
        "Langue", ["Français", "Anglais", "Cri", "Inuktitut"], index=0
    )
    theme = st.radio("Thème", ["Clair", "Sombre"], horizontal=True)
    notifications = st.checkbox("Recevoir des notifications", value=True)

    if st.button("💾 Sauvegarder les préférences"):
        st.session_state.user_preferences["language"] = langue
        st.session_state.user_preferences["theme"] = theme
        st.session_state.user_preferences["notifications"] = notifications
        st.success("✅ Préférences enregistrées.")


if __name__ == "__main__":