import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.express as px


def render():
    """
    Cette application Streamlit sert de formulaire de saisie pour le suivi
    continu de la grossesse et de l'accouchement, avec des fonctionnalités de sécurité et de visualisation.
    """
    st.set_page_config(page_title="Suivi Continu", page_icon="📊", layout="wide")
    st.title("📊 Suivi Continu de la Grossesse et de l'Accouchement")
    st.info(
        "Outil de suivi global de la grossesse et de l'accouchement, avec des alertes de sécurité et des visualisations en temps réel."
    )

    # Données simulées pour la sélection du patient
    patients_data = {
        "id": ["P101", "P102"],
        "nom": ["Jane Doe", "Alice Smith"],
        "poids_initial_kg": [65.0, 70.0],
        "date_debut_grossesse": [date(2025, 1, 1), date(2025, 2, 15)],
    }
    df_patients = pd.DataFrame(patients_data)

    # Données simulées de suivi pour Jane Doe
    jane_doe_history = pd.DataFrame(
        {
            "date_visite": [date(2025, 4, 1), date(2025, 5, 10), date(2025, 6, 20)],
            "poids_kg": [66.5, 68.0, 70.5],
            "hauteur_uterine_cm": [15.0, 20.0, 26.0],
            "tension_sys": [120, 125, 130],
            "tension_dia": [80, 85, 88],
        }
    )

    # Rôle de la sage-femme (pour la traçabilité)
    midwife_name = "Sage-femme Leclerc"

    # --- Formulaire principal de saisie ---
    with st.form(key="suivi_grossesse_form"):

        # --- Section 1: Informations de base ---
        st.subheader("1. Informations de base")
        col1, col2 = st.columns(2)
        with col1:
            # Sécurité : Sélection du patient dans la base de données
            selected_patient_name = st.selectbox(
                "Nom de la patiente", df_patients["nom"].tolist()
            )
            selected_patient = df_patients[
                df_patients["nom"] == selected_patient_name
            ].iloc[0]
            st.info(f"Dossier patient : **{selected_patient['id']}**")

            # Calcul de l'âge gestationnel à partir de la date de début de grossesse
            age_gestationnel_semaines = (
                date.today() - selected_patient["date_debut_grossesse"]
            ).days // 7
            st.write(
                f"Âge gestationnel actuel : **{age_gestationnel_semaines} semaines**"
            )

        with col2:
            date_of_visit = st.date_input("Date de la visite", value=date.today())
            st.info(f"Saisie par : **{midwife_name}**")

        st.markdown("---")

        # --- Section 2: Mesures et observations avec validation ---
        st.subheader("2. Mesures et observations")
        col3, col4, col5 = st.columns(3)
        with col3:
            poids_actuel = st.number_input("Poids (kg)", min_value=0.0, step=0.1)
            tension_sys = st.number_input(
                "Tension systolique (mmHg)", min_value=0, step=1
            )
            # Alerte pour le poids
            prise_de_poids = poids_actuel - selected_patient["poids_initial_kg"]
            if prise_de_poids > 15 and age_gestationnel_semaines > 20:
                st.warning("⚠️ Prise de poids excessive.")

        with col4:
            hauteur_uterine = st.number_input(
                "Hauteur utérine (cm)", min_value=0.0, step=0.5
            )
            tension_dia = st.number_input(
                "Tension diastolique (mmHg)", min_value=0, step=1
            )
            # Alerte pour la tension artérielle
            if tension_sys > 140 or tension_dia > 90:
                st.error("🚨 ALERTE : Risque de pré-éclampsie.")

        with col5:
            fetal_heart_rate = st.number_input(
                "Fréquence cardiaque fœtale (bpm)", min_value=0, step=1
            )
            presentation_foetale = st.selectbox(
                "Présentation fœtale", ["Céphalique", "Siège", "Transverse", "Inconnu"]
            )
            if not (110 <= fetal_heart_rate <= 160):
                st.error("🚨 ALERTE : FCF anormale. Nécessite une évaluation.")

        st.text_area(
            "Observations cliniques",
            placeholder="Notes sur les œdèmes, la fatigue, etc.",
        )

        # Ajout des données saisies à l'historique pour la visualisation
        new_entry = pd.DataFrame(
            [
                {
                    "date_visite": date_of_visit,
                    "poids_kg": poids_actuel,
                    "hauteur_uterine_cm": hauteur_uterine,
                    "tension_sys": tension_sys,
                    "tension_dia": tension_dia,
                }
            ]
        )
        combined_history = pd.concat([jane_doe_history, new_entry], ignore_index=True)

        st.markdown("---")

        # --- Visualisations des données (graphiques) ---
        st.subheader("3. Courbes de suivi")
        fig_poids = px.line(
            combined_history,
            x="date_visite",
            y="poids_kg",
            title="Évolution du poids de la patiente",
            markers=True,
        )
        fig_poids.update_layout(
            xaxis_title="Date de la visite", yaxis_title="Poids (kg)"
        )
        st.plotly_chart(fig_poids, use_container_width=True)

        fig_hu = px.line(
            combined_history,
            x="date_visite",
            y="hauteur_uterine_cm",
            title="Évolution de la hauteur utérine",
            markers=True,
        )
        fig_hu.update_layout(
            xaxis_title="Date de la visite", yaxis_title="Hauteur utérine (cm)"
        )
        st.plotly_chart(fig_hu, use_container_width=True)

        st.markdown("---")

        # --- Section 4: Données d'accouchement (saisie conditionnelle et structurée) ---
        st.subheader("4. Données d'accouchement")
        is_delivery_data = st.checkbox("Inclure les données d'accouchement ?")

        if is_delivery_data:
            col6, col7 = st.columns(2)
            with col6:
                delivery_date = st.date_input("Date de l'accouchement")
                delivery_time = st.time_input("Heure de l'accouchement")
                delivery_type = st.selectbox(
                    "Type d'accouchement",
                    ["Vaginal", "Césarienne", "Forceps", "Ventouse"],
                )
            with col7:
                apgar_score_1min = st.slider("Score d'Apgar à 1 minute", 0, 10)
                apgar_score_5min = st.slider("Score d'Apgar à 5 minutes", 0, 10)
                st.info(
                    "Le score d'Apgar est une évaluation rapide de la santé du nouveau-né."
                )

            st.text_area(
                "Notes d'accouchement",
                placeholder="Durée du travail, complications, etc.",
            )

        submit_button = st.form_submit_button("✅ Sauvegarder les données")

    if submit_button:
        # Ici, vous inséreriez le code pour sauvegarder les données
        st.success("✅ Données sauvegardées avec succès !")
        st.balloons()


if __name__ == "__main__":
    render()
