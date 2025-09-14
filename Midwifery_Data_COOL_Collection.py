import streamlit as st
import sqlite3
import bcrypt
import re
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time

# Import des utilitaires et des packs
from utils.navigation import get_page_order, navigation_controls, get_thematic_menus
from utils.security import est_autorise
from utils.logger import log_action, log_alert
from db import verify_user

# Import des packs
from packs.PATIENTs import patient_rdv, patient_carnet
from packs.MESSAGES import inbox, chat, send_message, receive_message
from packs.medecins import (
    doctors_page,
    doctor_diagnosis,
    doctor_prescriptions,
    doctor_history,
    doctor_consultations,
)
from packs.sages_femmes import (
    demographics,
    prenatal,
    intrapartum,
    postnatal,
    throughout,
)
from packs.infirmieres import patients, medicaments
from packs.ORGANISATION import calendar, modify_folder, complications
from packs.ADMIN import admin_users, admin_roles, admin_settings, admin_hashing
from modules.Home import page_home
from modules.Login import page_connexion


# 🧩 Dictionnaire : chaque clé est un nom de page,
# chaque valeur est une fonction `show()` du pack correspondant
router = {
    "home": page_home,
    "login": page_connexion,
    # Patients
    "patient_rdv": patient_rdv.show,
    "patient_carnet": patient_carnet.show,
    # Messages
    "inbox": inbox.show,
    "chat": chat.show,
    "send_message": send_message.show,
    "receive_message": receive_message.show,
    # Médecins
    "doctors_page": doctors_page.show,
    "doctor_diagnosis": doctor_diagnosis.show,
    "doctor_prescriptions": doctor_prescriptions.show,
    "doctor_history": doctor_history.show,
    "doctor_consultations": doctor_consultations.show,
    # Sage-femmes
    "demographics": demographics.show,
    "prenatal": prenatal.show,
    "intrapartum": intrapartum.show,
    "postnatal": postnatal.show,
    "throughout": throughout.show,
    # Infirmières
    "infirmiere_patients": patients.show,
    "infirmiere_medicaments": medicaments.show,
    # Organisation
    "calendar": calendar.show,
    "modify_folder": modify_folder.show,
    "complications": complications.show,
    # Administration
    "admin_users": admin_users.show,
    "admin_roles": admin_roles.show,
    "admin_settings": admin_settings.show,
    "admin_hashing": admin_hashing.show,
}


def get_greeting():
    """Détermine la salutation en fonction de l'heure actuelle."""
    heure = datetime.now().hour
    if 5 <= heure < 12:
        return "Bonjour"
    elif 12 <= heure < 18:
        return "Bon après-midi"
    else:
        return "Bonsoir"


def format_duration(seconds):
    """Formate une durée en heures, minutes et secondes."""
    heures = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secondes = int(seconds % 60)
    return f"{heures}h {minutes}min {secondes}s"


def main():
    st.set_page_config(page_title="Midwifery Tool", page_icon="👩‍🍼", layout="centered")

    # 🔐 Vérifier le statut d'authentification
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        # ------------------ En-tête du profil ------------------
        # Utilisation de .get pour éviter l'erreur si user_info n'existe pas
        user_info = st.session_state.get("user_info", {})
        prenom = user_info.get("prenom", st.session_state.username)
        role = user_info.get("role", st.session_state.role)

        st.sidebar.markdown(f"### {get_greeting()}, {prenom} !")
        st.sidebar.markdown(f"**Vous êtes connecté(e) en tant que** : {role}")

        # Calcul et affichage du temps de session
        temps_total = (datetime.now() - st.session_state.login_time).total_seconds()
        st.sidebar.markdown(
            f"**Heure de connexion** : {st.session_state.login_time.strftime('%H:%M:%S')}"
        )
        st.sidebar.markdown(f"**Temps de session** : {format_duration(temps_total)}")

        # Bouton de déconnexion
        if st.sidebar.button("🚪 Déconnexion"):
            log_action(
                st.session_state.utilisateur[2], st.session_state.role, "Déconnexion"
            )
            st.session_state.authenticated = False
            st.session_state.clear()
            st.rerun()

        # ------------------ Barres rapides ------------------
        st.sidebar.markdown("---")
        st.sidebar.subheader("🚀 Accès rapide")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("📅 Rendez-vous", key="quick_rdv"):
                st.session_state.current_page = "patient_rdv"
                st.rerun()
            if st.button("💬 Chat", key="quick_chat"):
                st.session_state.current_page = "chat"
                st.rerun()
        with col2:
            if st.button("🩺 Diagnostic", key="quick_diagnosis"):
                st.session_state.current_page = "doctor_diagnosis"
                st.rerun()
            if st.button("👥 Patients", key="quick_patients"):
                st.session_state.current_page = "infirmiere_patients"
                st.rerun()

        st.sidebar.markdown("---")
        st.sidebar.subheader("Progression du projet")
        st.sidebar.progress(75)
        st.sidebar.markdown("75% des objectifs accomplis !")

        # ------------------ Navigation thématique (packs) ------------------
        st.sidebar.markdown("---")
        st.sidebar.title("📌 Navigation")
        with st.sidebar.expander("👩‍🍼 Patients", expanded=False):
            if st.button("📅 Rendez-vous"):
                st.session_state.current_page = "patient_rdv"
                st.rerun()
            if st.button("📖 Carnet de santé"):
                st.session_state.current_page = "patient_carnet"
                st.rerun()

        with st.sidebar.expander("💬 Messages", expanded=False):
            if st.button("📥 Inbox"):
                st.session_state.current_page = "inbox"
                st.rerun()
            if st.button("💬 Chat"):
                st.session_state.current_page = "chat"
                st.rerun()
            if st.button("📤 Envoyer un message"):
                st.session_state.current_page = "send_message"
                st.rerun()
            if st.button("📩 Réception"):
                st.session_state.current_page = "receive_message"
                st.rerun()

        with st.sidebar.expander("🩺 Médecins", expanded=False):
            if st.button("👨‍⚕️ Espace Médecins"):
                st.session_state.current_page = "doctors_page"
                st.rerun()
            if st.button("🧬 Diagnostic"):
                st.session_state.current_page = "doctor_diagnosis"
                st.rerun()
            if st.button("💊 Prescriptions"):
                st.session_state.current_page = "doctor_prescriptions"
                st.rerun()
            if st.button("📜 Historique"):
                st.session_state.current_page = "doctor_history"
                st.rerun()
            if st.button("📞 Consultations"):
                st.session_state.current_page = "doctor_consultations"
                st.rerun()

        with st.sidebar.expander("👩‍⚕️ Sage-femmes", expanded=False):
            if st.button("👩 Demographics"):
                st.session_state.current_page = "demographics"
                st.rerun()
            if st.button("🤰 Prénatal"):
                st.session_state.current_page = "prenatal"
                st.rerun()
            if st.button("🌸 Intrapartum"):
                st.session_state.current_page = "intrapartum"
                st.rerun()
            if st.button("🍼 Postnatal"):
                st.session_state.current_page = "postnatal"
                st.rerun()
            if st.button("🌿 Throughout"):
                st.session_state.current_page = "throughout"
                st.rerun()

        with st.sidebar.expander("💉 Infirmières", expanded=False):
            if st.button("👥 Patients"):
                st.session_state.current_page = "infirmiere_patients"
                st.rerun()
            if st.button("💊 Médicaments"):
                st.session_state.current_page = "infirmiere_medicaments"
                st.rerun()

        with st.sidebar.expander("📅 Organisation", expanded=False):
            if st.button("🗓️ Calendrier"):
                st.session_state.current_page = "calendar"
                st.rerun()
            if st.button("📁 Modifier un dossier"):
                st.session_state.current_page = "modify_folder"
                st.rerun()
            if st.button("🧠 Complications"):
                st.session_state.current_page = "complications"
                st.rerun()

        with st.sidebar.expander("⚙️ Administration", expanded=False):
            if st.button("👤 Gestion utilisateurs"):
                st.session_state.current_page = "admin_users"
                st.rerun()
            if st.button("👥 Rôles & permissions"):
                st.session_state.current_page = "admin_roles"
                st.rerun()
            if st.button("⚙️ Paramètres"):
                st.session_state.current_page = "admin_settings"
                st.rerun()
            if st.button("🔐 Hashage & Sécurité"):
                st.session_state.current_page = "admin_hashing"
                st.rerun()

        # ======================================================
        # Lancer la page sélectionnée
        # ======================================================
        if "current_page" not in st.session_state:
            st.session_state.current_page = "home"

        current_page = st.session_state.current_page
        if current_page in router:
            router[current_page]()
        else:
            st.error("⚠️ Page introuvable dans le routeur !")

    else:
        # Si l'utilisateur n'est pas authentifié, afficher la page de connexion
        router["login"]()


if __name__ == "__main__":
    main()
