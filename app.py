# modules.py
# =========================================================
# 🎬 Application Midwifery Tool - Version Ultra Complète
# =========================================================

import streamlit as st
import os
from datetime import datetime
from PIL import Image

# =========================================================
# 🛠️ SESSION INIT
# =========================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None
if "login_time" not in st.session_state:
    st.session_state.login_time = None
if "last_login" not in st.session_state:
    st.session_state.last_login = None
if "logout_time" not in st.session_state:
    st.session_state.logout_time = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


# =========================================================
# 🔑 AUTH
# =========================================================
USERS = {
    "admin": {"password": "password", "role": "admin"},
    "doctor": {"password": "password", "role": "doctor"},
    "sagefemme": {"password": "password", "role": "midwife"},
    "infirmiere": {"password": "password", "role": "nurse"},
    "etudiante": {"password": "password", "role": "student"},
    "patient": {"password": "password", "role": "patient"},
}


def login_page():
    """Page de connexion simple"""
    st.title("🔐 Connexion")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    role = st.selectbox(
        "Choisissez votre rôle attribué",
        ["admin", "doctor", "midwife", "nurse", "student", "patient"],
    )

    if st.button("Se connecter"):
        if (
            username in USERS
            and USERS[username]["password"] == password
            and USERS[username]["role"] == role
        ):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.login_time = datetime.now()
            st.success("✅ Connexion réussie!")
            st.rerun()
        else:
            st.error("❌ Identifiants invalides")


def logout():
    """Déconnexion avec enregistrement heure"""
    if st.sidebar.button("🚪 Se déconnecter"):
        st.session_state.logout_time = datetime.now()
        st.session_state.authenticated = False
        st.rerun()


# =========================================================
# 🌟 PACKS (Menus Thématiques)
# =========================================================
MENU_PACKS = {
    # Communication interne
    "messages": {
        "📨 Messages": {
            "📥 Inbox": "inbox",
            "💬 Chat": "chat",
            "📤 Envoyer un message": "send_msg",
            "📩 Réception": "recv_msg",
        }
    },
    # Patients
    "patient": {
        "👶 Mon dossier": {
            "📅 Mes rendez-vous": "patient_rdv",
            "📖 Mon carnet de santé": "patient_carnet",
        }
    },
    # Médecins
    "doctor": {
        "🩺 Médecins": {
            "👨‍⚕️ Espace Médecins": "doctor_space",
            "🧬 Diagnostic": "doctor_diag",
            "💊 Prescriptions": "doctor_rx",
            "📜 Historique": "doctor_hist",
            "📞 Consultations": "doctor_consult",
        }
    },
    # Sages-femmes
    "midwife": {
        "🌸 Sages-femmes": {
            "👩‍🍼 Mes patientes": "midwife_patients",
            "📅 Mes rendez-vous": "midwife_rdv",
            "📝 Saisir consultation": "midwife_consult",
        }
    },
    # Infirmières
    "nurse": {
        "💉 Infirmières": {
            "👩‍⚕️ Mes patients": "nurse_patients",
            "💊 Médicaments": "nurse_rx",
        }
    },
    # Suivi des patientes
    "suivi": {
        "👩‍⚕️ Suivi des patientes": {
            "👩‍⚕️ Demographics": "suivi_demo",
            "🤰 Prenatal": "suivi_prenatal",
            "🌸 Intrapartum": "suivi_intra",
            "🍼 Postnatal": "suivi_postnatal",
            "🌿 Throughout": "suivi_global",
        }
    },
    # Organisation
    "orga": {
        "📅 Organisation": {
            "📅 Calendar": "orga_cal",
            "📁 Folder": "orga_folder",
            "🧠 Complications": "orga_complications",
        }
    },
    # Administration
    "admin": {
        "⚙️ Administration": {
            "🔐 Sécurité & Hashage": "admin_hash",
            "👥 Rôles & Permissions": "admin_roles",
            "👤 Gestion Utilisateurs": "admin_users",
            "⚙️ Paramètres": "admin_settings",
        }
    },
}


# =========================================================
# ✨ INTRO ANIMÉE PACKS
# =========================================================
def pack_intro(pack: str):
    if pack == "admin":
        st.sidebar.markdown(
            """<div style="background:#8b0000;color:white;
               padding:8px;border-radius:12px;animation:pulse 2s infinite;">
               ⚡️ Admin Zone ⚡️</div>
               <style>@keyframes pulse {
                 0%{box-shadow:0 0 5px red;}50%{box-shadow:0 0 25px yellow;}100%{box-shadow:0 0 5px red;}
               }</style>""",
            unsafe_allow_html=True,
        )
    elif pack == "doctor":
        st.sidebar.markdown(
            """<div style="background:#0072ff;color:white;
               padding:8px;border-radius:12px;animation:heartbeat 1.5s infinite;">
               🩺 Médecins</div>
               <style>@keyframes heartbeat {
                 0%{transform:scale(1);}25%{transform:scale(1.1);}50%{transform:scale(1);}
                 75%{transform:scale(1.1);}100%{transform:scale(1);}
               }</style>""",
            unsafe_allow_html=True,
        )
    elif pack == "midwife":
        st.sidebar.markdown(
            """<div style="background:#fad0c4;color:black;
               padding:8px;border-radius:12px;animation:glow 3s infinite;">
               🌸 Sages-femmes</div>
               <style>@keyframes glow {
                 0%{box-shadow:0 0 5px pink;}50%{box-shadow:0 0 25px violet;}100%{box-shadow:0 0 5px pink;}
               }</style>""",
            unsafe_allow_html=True,
        )
    elif pack == "nurse":
        st.sidebar.markdown(
            """<div style="background:#43cea2;color:white;
               padding:8px;border-radius:12px;animation:fade 4s infinite;">
               💉 Infirmières</div>
               <style>@keyframes fade {
                 0%{opacity:.4;}50%{opacity:1;}100%{opacity:.4;}
               }</style>""",
            unsafe_allow_html=True,
        )
    elif pack == "patient":
        st.sidebar.markdown(
            """<div style="background:#ffefba;color:black;
               padding:8px;border-radius:12px;animation:beat 2s infinite;">
               ❤️ Patients</div>
               <style>@keyframes beat {
                 0%{transform:scale(1);}50%{transform:scale(1.05);}100%{transform:scale(1);}
               }</style>""",
            unsafe_allow_html=True,
        )
    elif pack == "messages":
        st.sidebar.markdown(
            """<div style="background:linear-gradient(90deg,#00f260,#0575e6);
               color:white;padding:8px;border-radius:12px;animation:slide 6s infinite;">
               💬 Messages</div>
               <style>@keyframes slide {
                 0%{background-position:0% 50%;}50%{background-position:100% 50%;}
                 100%{background-position:0% 50%;}
               }</style>""",
            unsafe_allow_html=True,
        )
    elif pack == "suivi":
        st.sidebar.markdown(
            """<div style="background:#a1ffce;color:black;
               padding:8px;border-radius:12px;animation:zoom 3s infinite;">
               👩‍⚕️ Suivi patientes</div>
               <style>@keyframes zoom {
                 0%{transform:scale(1);}50%{transform:scale(1.05);}100%{transform:scale(1);}
               }</style>""",
            unsafe_allow_html=True,
        )
    elif pack == "orga":
        st.sidebar.markdown(
            """<div style="background:#f7971e;color:white;
               padding:8px;border-radius:12px;animation:flash 2s infinite;">
               📅 Organisation</div>
               <style>@keyframes flash {
                 0%{opacity:.4;}50%{opacity:1;}100%{opacity:.4;}
               }</style>""",
            unsafe_allow_html=True,
        )


# =========================================================
# 🧭 SIDEBAR BUILDER
# =========================================================
def build_sidebar(role: str):
    st.sidebar.title("📌 Navigation")

    # Messages → toujours visibles
    packs_to_show = ["messages"]

    if role == "admin":
        packs_to_show += [
            "admin",
            "doctor",
            "midwife",
            "nurse",
            "patient",
            "suivi",
            "orga",
        ]
    elif role == "doctor":
        packs_to_show += ["doctor", "patient", "suivi", "orga"]
    elif role == "midwife":
        packs_to_show += ["midwife", "patient", "suivi", "orga"]
    elif role == "nurse":
        packs_to_show += ["nurse", "patient", "suivi", "orga"]
    elif role == "patient":
        packs_to_show += ["patient"]

    # construire sidebar
    for pack in packs_to_show:
        pack_intro(pack)
        for theme, pages in MENU_PACKS[pack].items():
            with st.sidebar.expander(theme, expanded=False):
                for label, path in pages.items():
                    if st.button(label, key=f"btn_{path}"):
                        st.session_state.current_page = path
                        st.rerun()


# =========================================================
# 📄 PAGES (exemples placeholders)
# =========================================================
def home_page():
    st.title("🏡 Page d'accueil")
    st.markdown("✨ Bienvenue sur la plateforme Midwifery!")

    # Carrousel Cree Culture (images statiques)
    img_folder = "static/images_crie"
    if os.path.exists(img_folder):
        cols = st.columns(3)
        for i, f in enumerate(os.listdir(img_folder)[:6]):
            with cols[i % 3]:
                st.image(os.path.join(img_folder, f), caption=f"Cree {i+1}")

    # Bébé qui pleure
    audio_path = "static/bebe_pleure.mp3"
    if os.path.exists(audio_path):
        st.audio(audio_path)

    navigation_controls("home")


def inbox_page():
    st.subheader("📥 Boîte de réception")
    st.info("Ici les messages reçus s'afficheraient.")
    navigation_controls("inbox")


def chat_page():
    st.subheader("💬 Chat")
    st.info("Chat en temps réel.")
    navigation_controls("chat")


# =========================================================
# ⏮️⏭️ NAVIGATION PRÉC/SUIV
# =========================================================
PAGE_ORDER = [
    "home",
    "inbox",
    "chat",
    "send_msg",
    "recv_msg",
    "patient_rdv",
    "patient_carnet",
    "doctor_space",
    "doctor_diag",
    "doctor_rx",
    "doctor_hist",
    "doctor_consult",
    "midwife_patients",
    "midwife_rdv",
    "midwife_consult",
    "nurse_patients",
    "nurse_rx",
    "suivi_demo",
    "suivi_prenatal",
    "suivi_intra",
    "suivi_postnatal",
    "suivi_global",
    "orga_cal",
    "orga_folder",
    "orga_complications",
    "admin_hash",
    "admin_roles",
    "admin_users",
    "admin_settings",
]

PAGE_NAMES = {p: p.replace("_", " ").capitalize() for p in PAGE_ORDER}
PAGE_NAMES["home"] = "Accueil"


def navigation_controls(current: str):
    """Ajoute boutons précédent / suivant avec noms"""
    if current in PAGE_ORDER:
        idx = PAGE_ORDER.index(current)
        prev_page = PAGE_ORDER[idx - 1] if idx > 0 else None
        next_page = PAGE_ORDER[idx + 1] if idx < len(PAGE_ORDER) - 1 else None

        st.markdown("---")
        cols = st.columns([1, 2, 1])

        with cols[0]:
            if prev_page:
                if st.button(f"⬅️ Précédent ({PAGE_NAMES[prev_page]})"):
                    st.session_state.current_page = prev_page
                    st.rerun()
        with cols[1]:
            st.write(f"📄 Page actuelle : {PAGE_NAMES[current]}")
        with cols[2]:
            if next_page:
                if st.button(f"Suivant ({PAGE_NAMES[next_page]}) ➡️"):
                    st.session_state.current_page = next_page
                    st.rerun()


# =========================================================
# 🚀 MAIN
# =========================================================
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        # Infos utilisateur
        st.sidebar.markdown(f"👋 Utilisateur: **{st.session_state.username}**")
        st.sidebar.markdown(f"🎭 Rôle: **{st.session_state.role}**")
        st.sidebar.markdown(
            f"⏰ Connecté le: {st.session_state.login_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        if st.session_state.last_login:
            st.sidebar.markdown(
                f"📅 Dernière connexion: {st.session_state.last_login.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        if st.session_state.logout_time:
            st.sidebar.markdown(
                f"🚪 Déconnexion précédente: {st.session_state.logout_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        st.sidebar.markdown("---")

        # Sidebar
        build_sidebar(st.session_state.role)

        # Déconnexion
        logout()

        # Router
        current = st.session_state.current_page
        if current == "home":
            home_page()
        elif current == "inbox":
            inbox_page()
        elif current == "chat":
            chat_page()
        else:
            st.info(f"📄 Page {current} (placeholder)")
            navigation_controls(current)


if __name__ == "__main__":
    main()
