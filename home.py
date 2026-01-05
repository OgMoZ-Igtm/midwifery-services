# Fichier : home.py

import streamlit as st

from MSA_Midwife_Application.auth import login, check_role


# from auth_utils import login  # ton script d'authentification par rôle
# from auth_utils import check_role

st.set_page_config(page_title="Accueil Application", layout="wide")

st.title("🌐 Portail Central - Application Clinique Modulaire")
st.markdown("---")

# # 🔐 Authentification
# login()

if "authenticated" in st.session_state and st.session_state["authenticated"]:
    st.success(f"Bienvenue {st.session_state['role']} 🌿")

    # 🎯 Introduction
    st.markdown(
        """
    Choisissez votre rôle via le menu déroulant ou explorez les boutons poétiques ci-dessous.
    """
    )

    # 🧭 Menu déroulant dynamique
    roles = {
        "🛠️ Admin": "modules/dashboard_admin.py",
        "🧑‍⚕️ Doctor": "modules/dashboard_doctor.py",
        "🧍 Midwife": "modules/dashboard_midwife.py",
        "🧑‍⚕️ Nurse": "modules/dashboard_nurse.py",
        "🧍 Patient": "modules/dashboard_patient.py",
        "🎓 Doctoral": "modules/dashboard_doctoral.py",
        "👨‍🎓 Intern": "modules/dashboard_intern.py",
        "👩‍🎓 Student": "modules/dashboard_student.py",
        "👤 Guest": "modules/dashboard_guest.py",
    }

    selected_role = st.selectbox("🔽 Choisissez votre rôle :", list(roles.keys()))

    st.info(
        f"Vous avez choisi : **{selected_role}**. Lancez avec : `streamlit run {roles[selected_role]}`"
    )

    st.markdown("---")

    # 🎨 Boutons poétiques
    st.subheader("✨ Navigation poétique par rôle")

    cols = st.columns(3)
    i = 0
    for label, path in roles.items():
        with cols[i % 3]:
            if st.button(label):
                st.success(f"🌟 Lancez : `streamlit run {path}`")
        i += 1

    st.markdown("---")

    # 🧩 Fonctions disponibles
    st.subheader("🧰 Fonctionnalités disponibles")

    st.markdown(
        """
    - 📋 Formulaires spécifiques par rôle
    - 🤝 Fonctions partagées : Agenda, Calendrier, Profil, Statistiques…
    - 🎠 Workshops : Carrousel Soins Bébé
    - 📊 Tableaux de bord avec visualisations et export CSV
    - 🔍 Heatmaps et comparatifs de complétion
    """
    )

    # 🎉 Ambiance
    st.success(
        "L’application est prête à être explorée. Chaque rôle a son propre univers, ses formulaires et ses outils."
    )
    st.balloons()

else:
    st.warning("Veuillez vous connecter pour accéder aux rôles et dashboards.")
