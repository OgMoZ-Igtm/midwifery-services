import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px
import io


def render():
    """
    Cette application Streamlit sert de formulaire de saisie pour les données
    des soins postnatals, intégrant des fonctionnalités de sécurité et d'ergonomie cruciales.
    """
    st.set_page_config(page_title="Suivi Postnatal", page_icon="👩‍🍼", layout="wide")
    st.title("👩‍🍼 Suivi Postnatal")
    st.info(
        "Formulaire détaillé pour le suivi de la mère et du nouveau-né, avec alertes de sécurité et visualisation des données."
    )

    # Données simulées pour la sélection du patient
    patients_data = {
        "id": ["P101", "P102"],
        "nom": ["Jane Doe", "Alice Smith"],
        "poids_naissance_kg": [3.5, 3.2],
        "date_naissance_bebe": [date(2025, 9, 1), date(2025, 8, 28)],
    }
    df_patients = pd.DataFrame(patients_data)

    # Données simulées de suivi postnatal pour Jane Doe
    jane_doe_postnatal_history = pd.DataFrame(
        {"jours_postpartum": [0, 2, 5, 8], "poids_bebe_kg": [3.5, 3.3, 3.4, 3.6]}
    )

    # Sécurité: obtenir l'utilisateur courant (simulé ici)
    current_user = "Sage-femme Leclerc"

    with st.form(key="postnatal_care_form"):
        # --- Section 1: Identification et informations générales ---
        st.subheader("1. Identification de la mère et du nouveau-né")
        col1, col2 = st.columns(2)
        with col1:
            # Sécurité: Sélection du patient dans une liste
            selected_patient_name = st.selectbox(
                "Nom de la mère", df_patients["nom"].tolist()
            )
            selected_patient = df_patients[
                df_patients["nom"] == selected_patient_name
            ].iloc[0]

            # Calcul du jour post-partum
            days_postpartum = (
                date.today() - selected_patient["date_naissance_bebe"]
            ).days
            st.info(f"**Jour post-partum : {days_postpartum}**")
            st.info(f"Saisie par : **{current_user}**")

        with col2:
            consultation_date = st.date_input(
                "Date de la consultation", value=date.today()
            )
            breastfeeding_status = st.selectbox(
                "Allaitement",
                [
                    "Exclusif au sein",
                    "Allaitement mixte",
                    "Allaitement artificiel",
                    "Non-allaitante",
                ],
            )

        st.markdown("---")

        # --- Section 2: État de la mère ---
        st.subheader("2. État de la mère")
        col3, col4 = st.columns(2)
        with col3:
            systolic = st.number_input(
                "Tension artérielle systolique (mmHg)", min_value=0, step=1
            )
            diastolic = st.number_input(
                "Tension artérielle diastolique (mmHg)", min_value=0, step=1
            )
            temperature = st.number_input(
                "Température (°C)", min_value=35.0, max_value=42.0, step=0.1
            )
        with col4:
            bleeding = st.selectbox(
                "Saignements (Lochies)",
                ["Normaux", "Légers", "Modérés", "Abondants", "Inexistants"],
            )
            uterus_state = st.selectbox(
                "État de l'utérus", ["Fermé et rétracté", "Mou", "Douloureux"]
            )
            # Échelle de dépistage de la dépression post-partum (simplifiée)
            st.markdown("**Dépistage de la dépression post-partum**")
            dp_score = st.slider(
                "Humeur (échelle de 0 à 10)",
                0,
                10,
                help="0=excellente, 10=humeur très sombre.",
            )

        if temperature > 38.0:
            st.error("🚨 ALERTE : Fièvre. Risque d'infection (endométrite, mastite).")
        if bleeding == "Abondants":
            st.error(
                "🚨 ALERTE : Hémorragie post-partum. Prendre des mesures immédiates."
            )
        if dp_score >= 7:
            st.warning(
                "⚠️ ATTENTION : Score d'humeur élevé. Risque de dépression post-partum. Recommandation de soutien psychologique."
            )

        st.text_area(
            "État général et cicatrisation",
            placeholder="Ex: Humeur, douleur, état de la cicatrice...",
        )

        st.markdown("---")

        # --- Section 3: État du nouveau-né ---
        st.subheader("3. État du nouveau-né")
        col5, col6 = st.columns(2)
        with col5:
            baby_weight = st.number_input(
                "Poids du bébé (kg)", min_value=0.0, step=0.01
            )
            st.info(
                f"Poids à la naissance : **{selected_patient['poids_naissance_kg']} kg**"
            )
        with col6:
            baby_temp = st.number_input(
                "Température du bébé (°C)", min_value=35.0, max_value=40.0, step=0.1
            )
            baby_jaundice = st.selectbox(
                "Ictère (jaunisse)", ["Absent", "Léger", "Modéré", "Sévère"]
            )

        # Alertes sur le poids du bébé
        if baby_weight < (selected_patient["poids_naissance_kg"] * 0.9):
            st.error(
                "🚨 ALERTE : Perte de poids de plus de 10%. Risque de déshydratation ou de problème d'alimentation."
            )
        if baby_jaundice in ["Modéré", "Sévère"]:
            st.error(
                "🚨 ALERTE : Ictère modéré à sévère. Nécessite une évaluation clinique."
            )

        st.text_area(
            "Observations du bébé",
            placeholder="Ex: Comportement, alimentation, nombre de couches mouillées et souillées...",
        )

        # Visualisation de la croissance du bébé
        st.subheader("Courbe de poids du nouveau-né")
        new_data_df = pd.DataFrame(
            [{"jours_postpartum": days_postpartum, "poids_bebe_kg": baby_weight}]
        )
        combined_df = pd.concat(
            [jane_doe_postnatal_history, new_data_df], ignore_index=True
        )

        fig = px.line(
            combined_df,
            x="jours_postpartum",
            y="poids_bebe_kg",
            markers=True,
            title="Évolution du poids du nouveau-né",
        )
        fig.update_layout(xaxis_title="Jours post-partum", yaxis_title="Poids (kg)")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        submit_button = st.form_submit_button("✅ Enregistrer le suivi postnatal")

    if submit_button:
        st.success("✅ Suivi postnatal sauvegardé avec succès!")
        st.balloons()


if __name__ == "__main__":
    render()
