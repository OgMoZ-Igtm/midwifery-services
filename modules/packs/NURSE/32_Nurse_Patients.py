import streamlit as st
import pandas as pd
from datetime import datetime
import re  # pour la validation de la pression artérielle


def render():
    """
    Cette application Streamlit sert de formulaire pour la documentation
    des soins prodigués aux patients en obstétrique, avec des fonctionnalités
    de sécurité et de normalisation.
    """
    st.set_page_config(
        page_title="Documentation des soins", page_icon="🩹", layout="wide"
    )
    st.title("🩹 Documentation des Soins aux Patients")
    st.info(
        "Ce formulaire permet de documenter les soins et les observations cliniques de la patiente de manière sécurisée et structurée."
    )

    # Données simulées pour la démo
    patients_data = {
        "id": ["P101", "P102"],
        "nom": ["Jane Doe", "Alice Smith"],
        "chambre": ["302", "305"],
    }
    df_patients = pd.DataFrame(patients_data)

    # Simule l'utilisateur connecté pour la traçabilité
    current_nurse = "Infirmière Sophie L."

    with st.form("soins_patients_form"):
        # --- Section 1: Informations du patient et de l'infirmière ---
        st.subheader("1. Identification")
        col1, col2 = st.columns(2)
        with col1:
            # Sécurité: Sélection du patient dans une base de données
            selected_patient_name = st.selectbox(
                "Nom de la patiente",
                df_patients["nom"].tolist(),
                help="Sélectionnez la patiente pour lier le soin à son dossier.",
            )
            selected_patient = df_patients[
                df_patients["nom"] == selected_patient_name
            ].iloc[0]

        with col2:
            st.info(f"Numéro de chambre : **{selected_patient['chambre']}**")
            st.info(f"Soin documenté par : **{current_nurse}**")
            st.info(f"À : **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")

        st.markdown("---")

        # --- Section 2: Détails des soins (plus précis) ---
        st.subheader("2. Détails des soins")

        type_soin = st.selectbox(
            "Type de soin prodigué",
            [
                "Soins post-partum",
                "Soins post-opératoires",
                "Suivi des constantes vitales",
                "Soins d'allaitement",
                "Hygiène et confort",
                "Éducation thérapeutique",
                "Autre",
            ],
        )

        notes_soins = st.text_area(
            "Description des soins",
            placeholder="Décrivez les soins effectués, les observations particulières, la réaction de la patiente...",
        )

        st.markdown("---")

        # --- Section 3: Observations cliniques (structurées et validées) ---
        st.subheader("3. Observations cliniques et vitales")

        col3, col4 = st.columns(2)
        with col3:
            pression_arterielle_sys = st.number_input(
                "Pression artérielle systolique (mmHg)", min_value=0, step=1
            )
            pression_arterielle_dia = st.number_input(
                "Pression artérielle diastolique (mmHg)", min_value=0, step=1
            )

            # Alerte pour l'hypertension
            if pression_arterielle_sys > 140 or pression_arterielle_dia > 90:
                st.error(
                    "🚨 ALERTE : Pression artérielle élevée. Risque d'hypertension post-partum."
                )

            temperature = st.number_input(
                "Température (°C)", min_value=35.0, max_value=42.0, step=0.1
            )
            # Alerte pour la fièvre
            if temperature > 38.0:
                st.error("🚨 ALERTE : Fièvre. Risque d'infection.")

        with col4:
            frequence_cardiaque = st.number_input(
                "Fréquence cardiaque (bpm)", min_value=0, step=1
            )
            frequence_respiratoire = st.number_input(
                "Fréquence respiratoire", min_value=0, step=1
            )

            # Alerte pour les constantes vitales
            if not (60 <= frequence_cardiaque <= 100):
                st.warning("⚠️ Fréquence cardiaque hors de la norme (60-100 bpm).")
            if not (12 <= frequence_respiratoire <= 20):
                st.warning("⚠️ Fréquence respiratoire hors de la norme (12-20).")

            douleur_score = st.slider("Évaluation de la douleur (0-10)", 0, 10)

        etat_general = st.text_area(
            "État général de la patiente",
            placeholder="Ex: Alerte et réactive, semble confortable, etc.",
        )

        # Section pour le plan de soins et la continuité des soins
        st.markdown("---")
        st.subheader("4. Plan de soins et suivi")
        st.text_area(
            "Plan de soins",
            placeholder="Objectifs pour le prochain quart de travail (Ex: Surveiller TA toutes les 4h, encourager la marche...)",
        )

        submit = st.form_submit_button("✅ Enregistrer les soins")

        if submit:
            if not selected_patient_name or not notes_soins:
                st.error(
                    "❌ Veuillez remplir le nom de la patiente et la description des soins."
                )
            else:
                st.success("✅ Soins enregistrés avec succès!")
                st.balloons()


if __name__ == "__main__":
    render()
