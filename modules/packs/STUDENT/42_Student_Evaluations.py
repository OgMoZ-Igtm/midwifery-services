# BANNER_INJECTED
import streamlit as st
import pandas as pd
from datetime import date

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire pour la saisie et la
    consultation des évaluations de stage des étudiantes.
    """
    st.title("📝 Évaluations de Stage")
    st.info(
        "Complétez ou consultez les évaluations de vos stages. Ces évaluations sont essentielles pour votre développement professionnel."
    )

    # Simuler une base de données d'évaluations
    if "evaluations" not in st.session_state:
        st.session_state.evaluations = []

    st.subheader("➕ Soumettre une nouvelle évaluation")
    with st.form("student_eval_form"):
        col1, col2 = st.columns(2)
        with col1:
            stage_nom = st.text_input(
                "🏥 Nom du stage", placeholder="Ex: Gynécologie-Obstétrique"
            )
            date_debut = st.date_input("📅 Date de début")
        with col2:
            nom_superviseur = st.text_input(
                "🧑‍⚕️ Nom du superviseur", placeholder="Ex: Dr. Dubois"
            )
            date_fin = st.date_input("📅 Date de fin")

        st.markdown("---")

        st.subheader("Évaluation")

        col3, col4 = st.columns(2)
        with col3:
            note_superviseur = st.slider(
                "⭐ Évaluation du superviseur",
                0,
                10,
                5,
                help="Notez vos performances de 0 à 10.",
            )
        with col4:
            auto_eval = st.slider(
                "📊 Auto-évaluation", 0, 10, 5, help="Évaluez vos propres performances."
            )

        commentaires = st.text_area(
            "💬 Commentaires",
            placeholder="Ajoutez vos commentaires ou ceux du superviseur sur la performance, les points forts et les axes d'amélioration.",
        )

        submitted = st.form_submit_button("✅ Soumettre l'évaluation")
        if submitted:
            if stage_nom and nom_superviseur:
                new_evaluation = {
                    "Stage": stage_nom,
                    "Superviseur": nom_superviseur,
                    "Date de début": str(date_debut),
                    "Date de fin": str(date_fin),
                    "Note Superviseur": note_superviseur,
                    "Auto-évaluation": auto_eval,
                    "Commentaires": commentaires,
                }
                st.session_state.evaluations.append(new_evaluation)
                st.success("📝 Évaluation enregistrée avec succès!")
                st.experimental_rerun()
            else:
                st.error(
                    "❌ Veuillez remplir le nom du stage et le nom du superviseur."
                )

    st.markdown("---")

    st.subheader("📋 Historique des évaluations")
    if st.session_state.evaluations:
        df_evaluations = pd.DataFrame(st.session_state.evaluations)
        st.dataframe(df_evaluations, use_container_width=True)
    else:
        st.info("Aucune évaluation n'a encore été soumise.")


if __name__ == "__main__":
    render()
