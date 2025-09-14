# BANNER_INJECTED
import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.graph_objects as go


if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire de saisie pour les données
    des soins prénatals, intégrant des fonctionnalités de sécurité et d'ergonomie cruciales.
    """
    st.set_page_config(page_title="Suivi Prénatal", page_icon="🤰", layout="wide")
    st.title("🤰 Suivi Prénatal")
    st.info(
        "Formulaire détaillé pour le suivi des consultations prénatales, avec vérification des données et alertes de sécurité."
    )

    # --- Données simulées (à remplacer par une connexion à une base de données) ---
    patients_data = {
        "id": ["P101", "P102"],
        "nom": ["Jane Doe", "Alice Smith"],
        "ddr": [date(2025, 4, 1), date(2025, 5, 10)],
    }
    df_patients = pd.DataFrame(patients_data)

    # Données simulées de suivi pour Jane Doe
    jane_doe_history = pd.DataFrame(
        [
            {"semaine": 10, "poids_kg": 65.0, "hauteur_uterine_cm": 0},
            {"semaine": 14, "poids_kg": 66.5, "hauteur_uterine_cm": 14},
            {"semaine": 18, "poids_kg": 67.8, "hauteur_uterine_cm": 18},
            {"semaine": 22, "poids_kg": 69.1, "hauteur_uterine_cm": 22},
        ]
    )

    # Sécurité: obtenir l'utilisateur courant (simulé ici)
    current_user = "Dr. Dupont"

    with st.form(key="prenatal_care_form"):
        # --- Section : Identification du patient et Informations de la consultation ---
        st.subheader(
            "1. Identification de la patiente et informations de la consultation"
        )
        col_id, col_info = st.columns(2)
        with col_id:
            # Sécurité: Sélection du patient dans une liste
            selected_patient_name = st.selectbox(
                "Sélectionner la patiente", df_patients["nom"].tolist()
            )
            selected_patient = df_patients[
                df_patients["nom"] == selected_patient_name
            ].iloc[0]

            # Calcul de l'âge gestationnel à partir de la DDR
            ddr = selected_patient["ddr"]
            age_gestationnel_semaines = (date.today() - ddr).days // 7
            st.info(
                f"**Âge gestationnel actuel : {age_gestationnel_semaines} semaines**"
            )

        with col_info:
            consultation_date = st.date_input("Date de la consultation")
            next_appointment_date = st.date_input(
                "Date du prochain rendez-vous", min_value=date.today()
            )
            st.info(f"Saisie par : **{current_user}**")

        st.markdown("---")

        # --- Section : Mesures et observations (avec validation) ---
        st.subheader("2. Mesures et observations")

        col3, col4, col5 = st.columns(3)
        with col3:
            poids_kg = st.number_input(
                "Poids (kg)", min_value=0.0, step=0.1, key="poids"
            )
            tension_systolique = st.number_input(
                "Tension artérielle systolique (mmHg)",
                min_value=0,
                step=1,
                key="ta_sys",
            )
        with col4:
            hauteur_uterine_cm = st.number_input(
                "Hauteur utérine (cm)", min_value=0.0, step=0.5, key="hu"
            )
            tension_diastolique = st.number_input(
                "Tension artérielle diastolique (mmHg)",
                min_value=0,
                step=1,
                key="ta_dia",
            )
        with col5:
            frequence_cardiaque_foetale = st.number_input(
                "Fréquence cardiaque fœtale (bpm)", min_value=0, step=1, key="fcf"
            )
            mouvements_foetaux = st.selectbox(
                "Mouvements fœtaux",
                ["Présents", "Absents", "Non mesuré"],
                key="mouvements",
            )

        # Alertes de sécurité
        if tension_systolique > 140 or tension_diastolique > 90:
            st.error("🚨 ALERTE : Tension artérielle élevée. Risque de pré-éclampsie.")
        if mouvements_foetaux == "Absents":
            st.error(
                "🚨 ALERTE : Mouvements fœtaux absents. Veuillez vérifier immédiatement."
            )

        st.text_area(
            "Observations cliniques et examens",
            placeholder="Ex: Toucher vaginal, résultats d'analyse d'urine...",
        )

        # Visualisation de la croissance (poids et hauteur utérine)
        st.subheader("Courbes de croissance")

        # Ajout des données de la nouvelle consultation aux données historiques pour le graphique
        new_data_df = pd.DataFrame(
            [
                {
                    "semaine": age_gestationnel_semaines,
                    "poids_kg": poids_kg,
                    "hauteur_uterine_cm": hauteur_uterine_cm,
                }
            ]
        )
        combined_df = pd.concat([jane_doe_history, new_data_df], ignore_index=True)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=combined_df["semaine"],
                y=combined_df["poids_kg"],
                mode="lines+markers",
                name="Poids (kg)",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=combined_df["semaine"],
                y=combined_df["hauteur_uterine_cm"],
                mode="lines+markers",
                name="Hauteur utérine (cm)",
            )
        )
        fig.update_layout(
            title="Suivi de la croissance prénatale",
            xaxis_title="Âge gestationnel (semaines)",
            yaxis_title="Valeur",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        st.subheader("Ordonnances et recommandations")
        st.text_area(
            "Médicaments et recommandations",
            placeholder="Ex: Prescriptions de vitamines, conseils nutritionnels...",
        )

        submit_button = st.form_submit_button("✅ Enregistrer le suivi prénatal")

    if submit_button:
        # Ici, vous ajouteriez la logique pour sauvegarder les données
        st.success("✅ Suivi prénatal enregistré avec succès!")
        st.balloons()


if __name__ == "__main__":
    render()
