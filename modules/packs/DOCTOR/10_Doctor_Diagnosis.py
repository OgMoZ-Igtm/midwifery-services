import streamlit as st
import pandas as pd
from datetime import date, datetime


def render():
    st.title("🩺 Diagnostic médical")

    if st.session_state.get("role") == "ADMIN":
        st.warning("⛔ Accès en lecture seule pour les administrateurs.")
        st.markdown("Cette page est visible à des fins de supervision uniquement.")
        return

    """
    Cette application Streamlit sert de formulaire de saisie pour le diagnostic
    médical d'une patiente, avec une attention particulière aux besoins en obstétrique.
    """
    st.set_page_config(page_title="Diagnostic médical", page_icon="🩺", layout="wide")
    st.title("🩺 Saisie de Diagnostic médical")
    st.info(
        "Formulaire détaillé pour la saisie des observations, diagnostics et plans de traitement, intégrant des informations obstétricales clés."
    )

    # Données simulées pour la sélection du patient (remplacez par une base de données)
    patients_data = {
        "id_patient": [1, 2, 3],
        "nom": ["Jane Doe", "Alice Smith", "Marie Curia"],
        "age_gestationnel_sa": ["32 SA", "15 SA", "40 SA"],
        "dpa": ["2024-01-25", "2024-04-10", "2023-11-01"],
    }
    df_patients = pd.DataFrame(patients_data)

    # Utilisation d'un formulaire Streamlit pour une soumission groupée
    with st.form(key="medical_diagnosis_form"):
        # --- Section 1: Identification du patient et informations de base ---
        st.subheader("1. Informations sur la consultation et le patient")

        col1, col2, col3 = st.columns(3)
        with col1:
            # Sélection du patient à partir de la base de données
            selected_patient_name = st.selectbox(
                "Nom du patient",
                df_patients["nom"].tolist(),
                help="Sélectionnez le patient dans la liste pour associer la consultation à son dossier.",
            )
            # Affichage des informations clés du patient
            patient_info = df_patients[
                df_patients["nom"] == selected_patient_name
            ].iloc[0]

        with col2:
            st.date_input("Date de la consultation", value=date.today())
            st.markdown(f"**Âge gestationnel :** {patient_info['age_gestationnel_sa']}")

        with col3:
            st.text_input(
                "Heure de la consultation", value=datetime.now().strftime("%H:%M")
            )
            st.markdown(f"**Date prévue d'accouchement (DPA) :** {patient_info['dpa']}")

        st.markdown("---")

        # --- Section 2: Données vitales et observations ---
        st.subheader("2. Données vitales et observations cliniques")

        col_vitals1, col_vitals2, col_vitals3 = st.columns(3)
        with col_vitals1:
            st.number_input("Poids (kg)", min_value=0.0, format="%.2f")
            st.text_input("Pression artérielle (mmHg)", placeholder="Ex: 120/80")
        with col_vitals2:
            st.number_input(
                "Température (°C)", min_value=30.0, max_value=45.0, format="%.1f"
            )
            st.text_input("Fréquence cardiaque fœtale (bpm)", placeholder="Ex: 140")
        with col_vitals3:
            st.number_input("Hauteur utérine (cm)", min_value=0.0, format="%.1f")
            st.selectbox(
                "Présentation fœtale",
                ["Céphalique", "Siège", "Transverse", "Indéterminée"],
            )

        st.text_area(
            "Plaintes du patient et observations",
            placeholder="Ex: Douleurs abdominales, nausées, état général, etc.",
        )
        st.text_area(
            "Résultats d'examens physiques",
            placeholder="Ex: Palpation, auscultation, etc.",
        )

        st.markdown("---")

        # --- Section 3: Diagnostic et Plan de traitement ---
        st.subheader("3. Diagnostic, plan de traitement et signature")

        col_diag1, col_diag2 = st.columns(2)
        with col_diag1:
            st.text_area(
                "Diagnostic présomptif ou final",
                placeholder="Ex: Diabète gestationnel, pré-éclampsie, infection urinaire, etc.",
            )
        with col_diag2:
            st.text_area(
                "Plan de traitement et recommandations",
                placeholder="Ex: Médicaments prescrits, régime alimentaire, repos, rendez-vous de suivi, etc.",
            )

        st.markdown("---")

        # Champ de signature du médecin
        doctor_signature = st.text_input(
            "Nom du praticien (signature électronique)",
            help="Ce champ est requis pour la traçabilité.",
        )

        # Bouton de soumission
        submit_button = st.form_submit_button("✅ Enregistrer le diagnostic")

    if submit_button:
        # Vérification minimale des champs obligatoires
        if not selected_patient_name or not doctor_signature:
            st.error(
                "❌ Veuillez remplir tous les champs obligatoires (patient et signature)."
            )
        else:
            # Ici, vous ajouteriez la logique de sauvegarde des données dans une vraie base de données.
            st.success("✅ Diagnostic enregistré avec succès!")
            st.balloons()
            st.text_input("Diagnostic")
            st.text_area("Observations")
            st.button("Valider")


if __name__ == "__main__":
    render()
