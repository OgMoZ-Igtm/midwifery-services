import streamlit as st
import os
import base64
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import json

script_dir = os.path.dirname(os.path.abspath(__file__))

# Charger le menu
menu_path = os.path.join(script_dir, "..", "..", "data", "menu_mapping.json")
with open(menu_path, "r", encoding="utf-8") as f:
    menu_mapping = json.load(f)

# 🔐 Identifiants autorisés
USERS = {
    "sacre": {"password": "terre2025", "role": "MIDWIFE"},
    "admin": {"password": "admin123", "role": "ADMIN"},
    "nurse": {"password": "soin2025", "role": "NURSE"},
    "doctor": {"password": "medic2025", "role": "DOCTOR"},
    "student": {"password": "learn2025", "role": "STUDENT"},
    "intern": {"password": "stage2025", "role": "INTERN"},
    "patient": {"password": "bienvenue2025", "role": "PATIENT"},
    "doctoral": {"password": "recherche2025", "role": "DOCTORAL"},
}


# 🔊 Convertir le fichier audio en base64
def audio_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            ext = os.path.splitext(path)[1][1:]
            return f"data:audio/{ext};base64,{encoded}"
    return None


# 🔊 Lecteur audio avec bouton
def lecteur_audio():
    audio_path = os.path.join(script_dir, "..", "..", "static", "bebe_pleure.mp3")
    audio_data = audio_to_base64(audio_path)
    if audio_data:
        st.markdown(
            f"""
            <audio id="bebeAudio" autoplay loop>
                <source src="{audio_data}" type="audio/mpeg">
            </audio>
            <script>
                function toggleAudio() {{
                    var audio = document.getElementById("bebeAudio");
                    if (audio.paused) {{
                        audio.play();
                    }} else {{
                        audio.pause();
                    }}
                }}
            </script>
            <div style='text-align:center; margin-top:10px;'>
                <button onclick="toggleAudio()" style='padding:8px 16px;'>🔊 Démarrer / Arrêter le son</button>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("⚠️ Fichier audio introuvable.")


# 📝 Journaliser la connexion
def journaliser_connexion(role):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    heure_str = now.strftime("%H:%M:%S")
    moment = (
        "Bonjour" if now.hour < 12 else "Bon après-midi" if now.hour < 18 else "Bonsoir"
    )
    log_entry = f"[{date_str} {heure_str}] {moment} - Connexion en tant que {role}\n"
    log_path = os.path.join(script_dir, "..", "..", "logs", "connexions.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)


# 📖 Lire la dernière connexion
def lire_derniere_connexion():
    log_path = os.path.join(script_dir, "..", "..", "logs", "connexions.log")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            lignes = f.readlines()
            if lignes:
                return lignes[-1].strip()
    return "Aucune connexion enregistrée"


# 📊 Afficher les stats par rôle
def afficher_stats_connexions():
    log_path = os.path.join(script_dir, "..", "..", "logs", "connexions.log")
    if not os.path.exists(log_path):
        st.info("Aucune donnée de connexion disponible.")
        return

    with open(log_path, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    roles = []
    for ligne in lignes:
        if "Connexion en tant que" in ligne:
            role = ligne.split("Connexion en tant que")[-1].strip()
            roles.append(role)

    df = pd.DataFrame({"Rôle": roles})
    st.markdown("### 📈 Connexions par rôle")
    fig, ax = plt.subplots()
    df["Rôle"].value_counts().plot(kind="bar", ax=ax, color="skyblue")
    ax.set_ylabel("Nombre de connexions")
    st.pyplot(fig)


def authentifier_utilisateur():
    st.markdown("## 🔐 Connexion sécurisée")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state["role"] = user["role"]
            st.session_state["username"] = username
            st.session_state["authentifie"] = True
            st.success(f"Connexion réussie en tant que {user['role']}")
        else:
            st.error("Identifiants incorrects.")


# 🚀 Page principale
def render():
    st.set_page_config(page_title="🌾 Espace sécurisé", page_icon="🌾")

    if "authentifie" not in st.session_state or not st.session_state["authentifie"]:
        authentifier_utilisateur()
        return

    role = st.session_state.get("role", "MIDWIFE")
    with st.sidebar:
        st.header("🧭 Navigation")
    for pack, pages in menu_mapping.items():
        for page in sorted(pages, key=lambda x: x["order"]):
            if role in page["roles"] or "ALL" in page["roles"]:
                st.markdown(f"- {page['name']}")
    st.markdown("---")
    st.markdown(f"👤 Rôle : **{role}**")
    st.markdown(f"👤 Utilisateur : **{st.session_state.get('username', 'inconnu')}**")
    if st.button("🔓 Déconnexion", key="logout_button"):
        st.session_state.clear()
        st.rerun()

    journaliser_connexion(role)
    st.markdown(f"👤 Connecté en tant que **{role}**")
    st.markdown(f"👤 Utilisateur : **{st.session_state.get('username', 'inconnu')}**")

    now = datetime.now()
    heure = now.hour
    date_connexion = now.strftime("%A %d %B %Y")
    heure_connexion = now.strftime("%H:%M")
    salutation = (
        "Bonjour" if heure < 12 else "Bon après-midi" if heure < 18 else "Bonsoir"
    )

    st.markdown(
        f"""
    ### 👋 {salutation}, Sacré
    Vous êtes connecté en tant que **{role}**
    🕒 Heure de connexion : **{heure_connexion}**
    📅 Date : **{date_connexion}**
    🗂️ Dernière connexion : *{lire_derniere_connexion()}*
    """
    )

    with st.sidebar:
        st.header("🧭 Navigation")
    pages_accessibles = []

    for pack, pages in menu_mapping.items():
        for page in sorted(pages, key=lambda x: x["order"]):
            if role in page["roles"] or "ALL" in page["roles"]:
                pages_accessibles.append((page["name"], page["file"]))

    choix = st.radio("📂 Sélectionnez une page :", [p[0] for p in pages_accessibles])

    for nom, chemin in pages_accessibles:
        if choix == nom:
            st.markdown(f"### 📄 Page sélectionnée : {nom}")
        st.markdown(f"[👉 Ouvrir {nom}]({chemin})")
        break

    st.progress(100)
    lecteur_audio()

    st.markdown("---")
    st.subheader("🧡 Bienvenue / Welcome")
    st.markdown(
        f"**FR** : Ceci est votre espace personnalisé en tant que {role.lower()}.\n\n**EN** : This is your personalized space as a {role.lower()}."
    )

    st.markdown("---")
    st.subheader("🖼️ Image du rôle")
    image_path = os.path.join("images", f"welcome_{role.lower()}.png")
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning(f"⚠️ Image introuvable : {image_path}")

    st.markdown("---")
    st.subheader("🖨️ Impression")
    st.markdown(
        """
        <div style='text-align:center; margin-top:30px;'>
            <button onclick='window.print()' style='padding:10px 20px; font-size:16px; background-color:#6b4c3b; color:white; border:none; border-radius:5px;'>
                🖨️ Print This Page
            </button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.button("🌼 Start", key="start_button")


if __name__ == "__main__":
    render()
