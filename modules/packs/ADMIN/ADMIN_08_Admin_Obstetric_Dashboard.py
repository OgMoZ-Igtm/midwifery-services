import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta


def render():
    """
    Page : Visualisation des données
    Rôle : ADMIN
    Objectif : Permet à l’administrateur de voir des statistiques globales et obstétriques.
    """
    st.set_page_config(
        page_title="Visualisation des Données", page_icon="📊", layout="wide"
    )

    st.title("📊 Tableau de bord de visualisation des données")
    st.info(
        "Cette page permet aux administrateurs de **voir les tendances** "
        "dans les données collectées (patients, consultations, accouchements, etc.)."
    )

    # Vérification des privilèges
    if st.session_state.get("role") != "admin":
        st.warning("⛔ Accès réservé aux administrateurs.")
        st.stop()

    st.markdown("---")

    # --- Données simulées (à remplacer par la vraie DB) ---
    @st.cache_data
    def load_data():
        # Données pour la partie obstétrique
        data_obstetric = {
            "patient_id": range(1, 201),
            "age": np.random.randint(20, 45, 200),
            "statut_grossesse": np.random.choice(
                ["Grossesse en cours", "Post-partum", "Suivi terminé"],
                200,
                p=[0.6, 0.3, 0.1],
            ),
            "type_accouchement": np.random.choice(
                ["Voie basse", "Césarienne", "Prématuré", "Autres"],
                200,
                p=[0.6, 0.25, 0.1, 0.05],
            ),
            "date_naissance_prevue": [
                (datetime.now() + timedelta(days=np.random.randint(-60, 180))).strftime(
                    "%Y-%m-%d"
                )
                for _ in range(200)
            ],
            "nombre_consultations": np.random.randint(3, 15, 200),
        }
        df_obstetric = pd.DataFrame(data_obstetric)

        # Données pour la partie générale
        data_general = {
            "Mois": ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août"],
            "Consultations": [45, 60, 55, 70, 65, 80, 75, 90],
            "Accouchements": [12, 18, 15, 20, 17, 22, 25, 28],
            "Patients Uniques": [30, 40, 35, 50, 45, 55, 50, 60],
        }
        df_general = pd.DataFrame(data_general)
        return df_obstetric, df_general

    df_obstetric, df_general = load_data()

    # --- Section Tableau de bord Obstétrique ---
    st.subheader("Indicateurs Clés Obstétriques 🤰")

    col1, col2, col3, col4 = st.columns(4)

    naissance_prevue_df = df_obstetric[
        df_obstetric["statut_grossesse"] == "Grossesse en cours"
    ]
    naissances_attendues = len(naissance_prevue_df)
    col1.metric("🍼 Naissances attendues", naissances_attendues, "ce trimestre")

    age_moyen = int(df_obstetric["age"].mean())
    col2.metric("👵 Âge moyen des mères", f"{age_moyen} ans")

    taux_cesarienne = (
        df_obstetric[df_obstetric["type_accouchement"] == "Césarienne"].shape[0]
        / df_obstetric.shape[0]
    ) * 100
    col3.metric("✂️ Taux de césarienne", f"{taux_cesarienne:.1f}%")

    consultations_moyennes = df_obstetric["nombre_consultations"].mean()
    col4.metric("🗓️ Consultations / patient", f"{consultations_moyennes:.1f}")

    st.markdown("---")

    # --- Visualisations des données obstétriques ---
    st.subheader("Visualisations des tendances obstétriques")
    col_vis1, col_vis2 = st.columns(2)

    with col_vis1:
        statut_counts = df_obstetric["statut_grossesse"].value_counts().reset_index()
        statut_counts.columns = ["Statut", "Nombre de patients"]
        fig1 = px.pie(
            statut_counts,
            values="Nombre de patients",
            names="Statut",
            title="Répartition par statut de grossesse",
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_vis2:
        type_counts = df_obstetric["type_accouchement"].value_counts().reset_index()
        type_counts.columns = ["Type d'accouchement", "Nombre"]
        fig2 = px.bar(
            type_counts,
            x="Type d'accouchement",
            y="Nombre",
            title="Répartition par type d'accouchement",
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- Section Données Générales ---
    st.subheader("📈 Aperçu des données générales")
    st.dataframe(df_general, use_container_width=True)

    # Graphiques généraux
    st.write("### Consultations et Accouchements par mois")
    fig = px.line(
        df_general,
        x="Mois",
        y=["Consultations", "Accouchements"],
        title="Tendances mensuelles",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Nombre de patients uniques par mois")
    fig2 = px.bar(
        df_general,
        x="Mois",
        y="Patients Uniques",
        title="Patients uniques par mois",
        color="Patients Uniques",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.info(
        "ℹ️ Ici, tu pourras brancher ta base de données réelle pour afficher des graphiques dynamiques."
    )


if __name__ == "__main__":
    render()
