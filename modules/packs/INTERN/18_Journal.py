# BANNER_INJECTED
import streamlit as st
from datetime import date

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire pour le journal de stage,
    permettant à une stagiaire de documenter ses activités quotidiennes,
    ses observations et ses réflexions.
    """
    st.title("📔 Journal de Stage")
    st.info(
        "Documentez vos activités, vos observations et vos réflexions de la journée."
    )

    with st.form("journal_stage_form"):

        # --- Section : Date et informations générales ---
        st.subheader("1. Informations de la journée")

        jour = st.date_input("📅 Date", value=date.today())

        st.markdown("---")

        # --- Section : Activités et observations ---
        st.subheader("2. Activités et observations")

        activites = st.text_area(
            "Activités réalisées",
            placeholder="Décrivez les tâches accomplies, les consultations auxquelles vous avez assisté, les procédures que vous avez observées, etc.",
        )

        observations = st.text_area(
            "Observations et réflexions",
            placeholder="Notez vos observations cliniques, les points qui vous ont marqué, et vos réflexions personnelles sur la journée.",
        )

        apprentissage = st.text_area(
            "Points d'apprentissage clés",
            placeholder="Qu'avez-vous appris de nouveau aujourd'hui ? Ex: une technique, un diagnostic, un protocole...",
        )

        st.markdown("---")

        # --- Section : Évaluation et questions ---
        st.subheader("3. Évaluation et questions")

        evaluation = st.slider(
            "Évaluation de la journée (1=Mauvais, 10=Excellent)",
            1,
            10,
            5,
            help="Évaluez la productivité et la richesse de votre journée de stage.",
        )

        questions = st.text_area(
            "Questions pour le superviseur",
            placeholder="Notez ici les questions à poser à votre superviseur lors de votre prochaine rencontre.",
        )

        submit = st.form_submit_button("✅ Enregistrer le journal")

        if submit:
            st.success("✅ Journal de stage sauvegardé avec succès!")
            st.balloons()


if __name__ == "__main__":
    render()
