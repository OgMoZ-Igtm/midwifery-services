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
    Cette application Streamlit sert de carnet de stage pour l'étudiante
    en obstétrique, lui permettant de documenter ses activités cliniques.
    """
    st.title("📘 Carnet de Stage - Obstétrique")
    st.info(
        "Utilisez ce carnet de stage pour enregistrer les informations concernant votre pratique clinique et vos observations."
    )

    # Simuler une base de données d'activités de stage
    if "stage_logbook" not in st.session_state:
        st.session_state.stage_logbook = []

    st.subheader("➕ Enregistrer une nouvelle entrée")
    with st.form("student_practice_form"):
        col1, col2 = st.columns(2)
        with col1:
            stage_site = st.text_input(
                "🏥 Lieu de stage", placeholder="Ex: Hôpital St-Luc"
            )
            date_pratique = st.date_input("📅 Date de la pratique")
        with col2:
            superviseur = st.text_input(
                "👩‍⚕️ Nom du superviseur", placeholder="Ex: Mme Julie Leclerc"
            )
            heures = st.number_input("⏱️ Heures complétées ce jour", min_value=0, step=1)

        type_activite = st.selectbox(
            "Type d'activité",
            [
                "Consultation prénatale",
                "Suivi d'accouchement",
                "Soins post-partum",
                "Observation",
                "Atelier de prévention",
                "Autre",
            ],
        )

        activites = st.text_area(
            "✍️ Description détaillée de l'activité",
            placeholder="Décrivez les soins prodigués, les techniques apprises, les observations cliniques...",
        )

        submitted = st.form_submit_button("✅ Enregistrer l'entrée")
        if submitted:
            if stage_site and superviseur and activites:
                new_entry = {
                    "Date": str(date_pratique),
                    "Lieu de stage": stage_site,
                    "Superviseur": superviseur,
                    "Heures": heures,
                    "Activité": type_activite,
                    "Description": activites,
                }
                st.session_state.stage_logbook.append(new_entry)
                st.success("📌 Entrée de carnet de stage mise à jour avec succès.")
                st.experimental_rerun()
            else:
                st.error(
                    "❌ Veuillez remplir les champs obligatoires (Lieu de stage, Superviseur, Description de l'activité)."
                )

    st.markdown("---")

    st.subheader("📋 Historique du carnet de stage")
    if st.session_state.stage_logbook:
        df_logbook = pd.DataFrame(st.session_state.stage_logbook)
        st.dataframe(df_logbook, use_container_width=True)
    else:
        st.info("Aucune entrée n'a encore été enregistrée.")


if __name__ == "__main__":
    render()
