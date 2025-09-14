# BANNER_INJECTED
import streamlit as st
from datetime import date

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire pour le suivi
    d'une consultation prénatale.
    """
    st.title("🤰 Suivi de Consultation Prénatale")
    st.info("Remplissez ce formulaire pour chaque consultation prénatale suivie.")

    with st.form("consultation_form"):
        st.subheader("Informations de base")

        col1, col2 = st.columns(2)
        with col1:
            date_consultation = st.date_input("📅 Date de la consultation")
            nom_patient = st.text_input(
                "Nom de la patiente", placeholder="Ex: Lucie Martin"
            )
        with col2:
            age_gestationnel = st.text_input(
                "Âge gestationnel (SA)", placeholder="Ex: 32 SA"
            )

        st.markdown("---")

        st.subheader("Mesures et observations")

        col3, col4 = st.columns(2)
        with col3:
            poids = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
            pression = st.text_input("Pression artérielle", placeholder="Ex: 120/80")
        with col4:
            hauteur_uterine = st.number_input(
                "Hauteur utérine (cm)", min_value=0.0, step=0.1
            )
            rythme_cardiaque_foetal = st.text_input(
                "Rythme cardiaque fœtal (bpm)", placeholder="Ex: 145"
            )

        st.markdown("---")

        st.subheader("Détails de la consultation")

        motif = st.text_area(
            "Motif de la consultation",
            placeholder="Ex: Suivi de routine, inquiétude concernant les mouvements du bébé...",
        )

        conseils_donnes = st.text_area(
            "Conseils ou consignes donnés",
            placeholder="Ex: Adapter son alimentation, surveiller les signes, planifier le prochain rendez-vous...",
        )

        submit = st.form_submit_button("✅ Enregistrer la consultation")

        if submit:
            st.success("✅ Fiche de consultation enregistrée avec succès!")


if __name__ == "__main__":
    render()
