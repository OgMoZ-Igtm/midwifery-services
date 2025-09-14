# BANNER_INJECTED
import streamlit as st
from datetime import date

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire pour la saisie et le suivi
    des cours suivis par l'étudiant ou le stagiaire.
    """
    st.title("📚 Cours Suivis")
    st.info(
        "Utilisez ce formulaire pour documenter les cours et formations que vous avez suivis."
    )

    with st.form("cours_suivis_form"):
        st.subheader("Détails du cours")

        nom_cours = st.text_input(
            "Nom du cours ou de la formation",
            placeholder="Ex: Soins infirmiers en obstétrique",
        )

        col1, col2 = st.columns(2)
        with col1:
            institution = st.text_input(
                "Institution ou organisme de formation",
                placeholder="Ex: Université de Montréal",
            )
        with col2:
            date_completion = st.date_input(
                "📅 Date de complétion", max_value=date.today()
            )

        certificat = st.file_uploader(
            "📥 Télécharger le certificat ou l'attestation",
            type=["pdf", "png", "jpg", "jpeg"],
        )

        notes = st.text_area(
            "Notes personnelles",
            placeholder="Réflexions sur le cours, compétences acquises, etc.",
        )

        submit = st.form_submit_button("✅ Enregistrer")

        if submit:
            if nom_cours and institution and date_completion:
                st.success("✅ Données enregistrées avec succès!")
                st.balloons()
            else:
                st.error("❌ Veuillez remplir tous les champs obligatoires.")


if __name__ == "__main__":
    render()
