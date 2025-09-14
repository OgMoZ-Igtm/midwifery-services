import streamlit as st
import pandas as pd
from datetime import date, datetime


def render():
    """
    Cette application Streamlit sert de formulaire de saisie pour les
    prescriptions médicales, intégrant des fonctionnalités de sécurité cruciales.
    """
    st.set_page_config(
        page_title="Prescriptions médicales", page_icon="💊", layout="wide"
    )
    st.title("💊 Prescriptions médicales")
    st.info(
        "Formulaire détaillé pour la création de prescriptions médicales, avec vérification des données."
    )

    # --- Données simulées (à remplacer par une connexion à une base de données) ---
    patients_df = pd.DataFrame(
        {
            "id": ["P101", "P102", "P103"],
            "nom": ["Jane Doe", "Alice Smith", "Marie Curia"],
            "allergies": [["Pénicilline"], ["Ibuprofène"], []],
            "grossesse_active": [True, False, True],
        }
    )

    medications_df = pd.DataFrame(
        {
            "nom": ["Paracétamol", "Amoxicilline", "Antihistaminique", "Ibuprofène"],
            "compatible_grossesse": [True, True, False, False],
            "posologies_standard": [
                ["500 mg", "1 g"],
                ["250 mg", "500 mg"],
                ["10 mg"],
                ["200 mg", "400 mg"],
            ],
        }
    )

    doctor_info = {"id": "D201", "nom": "Dr. Jean Dupont"}

    # --- Utilisation d'un formulaire pour regrouper les entrées ---
    with st.form(key="medical_prescription_form"):

        # --- Section 1: Informations de base ---
        st.subheader("1. Informations de la consultation")
        col1, col2 = st.columns(2)
        with col1:
            # Sélection du patient
            patient_name = st.selectbox(
                "Sélectionner le patient",
                patients_df["nom"].tolist(),
                help="Sélectionnez le patient dans la base de données.",
            )
            selected_patient = patients_df[patients_df["nom"] == patient_name].iloc[0]

            # Affichage d'alertes de sécurité
            if selected_patient["grossesse_active"]:
                st.warning(
                    "🤰 Attention : Grossesse en cours. Vérifiez la compatibilité des médicaments."
                )

        with col2:
            prescription_date = st.date_input(
                "Date de la prescription", value=date.today()
            )
            st.info(f"Prescrit par : **{doctor_info['nom']}**")

        st.markdown("---")

        # --- Section 2: Détails de la prescription (avec ajout dynamique) ---
        st.subheader("2. Détails de la prescription")

        # Utilisation de st.session_state pour gérer les médicaments
        if "medications" not in st.session_state:
            st.session_state.medications = [{}]

        for i, med_data in enumerate(st.session_state.medications):
            st.markdown(f"**Médicament #{i+1}**")
            med_name = st.selectbox(
                "Nom du médicament",
                [""] + medications_df["nom"].tolist(),
                key=f"med_name_{i}",
            )

            # Vérification des allergies
            if med_name in selected_patient["allergies"]:
                st.error(
                    f"❌ Alerte d'allergie : Le patient est allergique à {med_name} !"
                )

            # Vérification de la compatibilité avec la grossesse
            if (
                selected_patient["grossesse_active"]
                and med_name
                and not medications_df[medications_df["nom"] == med_name][
                    "compatible_grossesse"
                ].iloc[0]
            ):
                st.error(
                    f"❌ Alerte : {med_name} n'est pas recommandé pendant la grossesse."
                )

            # Affichage de la posologie standard
            col3, col4 = st.columns(2)
            with col3:
                posologies = (
                    medications_df[medications_df["nom"] == med_name][
                        "posologies_standard"
                    ].iloc[0]
                    if med_name
                    else []
                )
                dosage = st.selectbox("Posologie", posologies, key=f"dosage_{i}")

                frequency = st.text_input(
                    "Fréquence", placeholder="Ex: 1x/jour", key=f"freq_{i}"
                )
            with col4:
                duration = st.text_input(
                    "Durée du traitement",
                    placeholder="Ex: 7 jours",
                    key=f"duration_{i}",
                )
                route = st.selectbox(
                    "Voie d'administration",
                    ["Orale", "Injectable", "Topique", "Autre"],
                    key=f"route_{i}",
                )

            st.text_area(
                "Instructions supplémentaires",
                placeholder="Ex: À prendre avec les repas...",
                key=f"instructions_{i}",
            )
            st.markdown("---")

        if st.button("➕ Ajouter un autre médicament"):
            st.session_state.medications.append({})
            st.rerun()

        st.markdown("---")

        # Bouton de soumission
        submit_button = st.form_submit_button(
            "✅ Enregistrer et imprimer la prescription"
        )

    if submit_button:
        # Ici, vous ajouteriez la logique de sauvegarde des données dans la base de données.
        # Enregistrer les données et générer le document PDF
        st.success(
            f"✅ Prescription pour **{patient_name}** enregistrée et prête à être imprimée. "
        )
        st.balloons()


if __name__ == "__main__":
    render()
