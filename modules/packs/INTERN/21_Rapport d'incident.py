# BANNER_INJECTED
import streamlit as st
from datetime import datetime

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire pour la déclaration
    d'un incident ou d'une observation inhabituelle.
    """
    st.title("🚨 Rapport d'Incident / Observation")
    st.info(
        "Utilisez ce formulaire pour documenter tout incident, événement ou observation inhabituelle."
    )

    with st.form("incident_report_form"):
        st.subheader("Informations de l'événement")

        col1, col2 = st.columns(2)
        with col1:
            date_evenement = st.date_input("📅 Date de l'événement")
        with col2:
            heure_evenement = st.time_input("⏰ Heure de l'événement")

        lieu = st.text_input(
            "Lieu de l'événement",
            placeholder="Ex: Salle d'accouchement n°3, Unité de soins post-partum",
        )

        st.markdown("---")

        st.subheader("Description de l'événement")

        type_incident = st.selectbox(
            "Type d'événement",
            [
                "Erreur de procédure",
                "Erreur de communication",
                "Observation clinique anormale",
                "Problème d'équipement",
                "Autre",
            ],
        )

        description = st.text_area(
            "Description de l'événement",
            placeholder="Décrivez en détail ce qui s'est passé, les personnes impliquées, les actions prises, etc.",
            height=150,
        )

        submit = st.form_submit_button("✅ Soumettre le rapport")

        if submit:
            if not lieu or not description:
                st.error("❌ Le lieu et la description sont des champs obligatoires.")
            else:
                st.success("✅ Rapport d'incident soumis avec succès!")
                st.balloons()


if __name__ == "__main__":
    render()
