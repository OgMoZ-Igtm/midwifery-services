import streamlit as st
import datetime
import pandas as pd
from utils.security import afficher_badge_securite


# Assurez-vous d'avoir une fonction `render()` dans chaque page
def render():
    """
    Formulaire de saisie pour les informations cliniques d'un patient.
    """

    # Affichage du badge de sécurité pour le rôle "DOCTOR"
    st.markdown(afficher_badge_securite("DOCTOR"), unsafe_allow_html=True)

    st.title("👨‍⚕️ Formulaire de consultation patient")
    st.info(
        "Utilisez ce formulaire pour saisir les informations cliniques et les plans de traitement."
    )

    with st.form(key="doctor_form"):
        st.subheader("1. Informations du patient")

        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input(
                "ID Patient", max_chars=10, help="ID unique du patient"
            )
            full_name = st.text_input("Nom et Prénom")

        with col2:
            dob = st.date_input("Date de naissance", max_value=datetime.date.today())
            gender = st.selectbox("Sexe", ["Non spécifié", "Femme", "Homme"])

        st.markdown("---")

        st.subheader("2. Informations médicales")

        col3, col4 = st.columns(2)
        with col3:
            weight = st.number_input("Poids (kg)", min_value=1.0, step=0.1)
            height = st.number_input("Taille (cm)", min_value=10.0, step=0.1)
            blood_pressure = st.text_input("Tension artérielle (ex: 120/80)")

        with col4:
            temperature = st.number_input(
                "Température (°C)", min_value=30.0, max_value=45.0, step=0.1
            )
            heart_rate = st.number_input("Rythme cardiaque (bpm)", min_value=10, step=1)
            allergies = st.text_area(
                "Allergies connues",
                height=100,
                help="Listez les allergies séparées par des virgules",
            )

        st.markdown("---")

        st.subheader("3. Diagnostic et traitement")

        diagnosis = st.text_area("Diagnostic principal", height=150)
        treatment_plan = st.text_area("Plan de traitement et prescriptions", height=200)

        # Ajout d'une option pour les fichiers attachés
        st.info("Vous pouvez joindre des fichiers de laboratoire ou d'imagerie.")
        uploaded_file = st.file_uploader(
            "Joindre des documents",
            type=["pdf", "jpg", "png"],
            accept_multiple_files=True,
        )

        if uploaded_file:
            for file in uploaded_file:
                st.write(f"Fichier joint : {file.name}")

        submit_button = st.form_submit_button("✅ Soumettre le formulaire")

    if submit_button:
        # Vérification minimale des champs obligatoires
        if not patient_id or not full_name:
            st.error("❌ Veuillez remplir les champs ID Patient et Nom et Prénom.")
        else:
            # Traitement des données soumises (simulation)
            st.success("🎉 Données patient soumises avec succès!")
            st.balloons()

            # Affichage des données soumises pour vérification
            st.subheader("📝 Récapitulatif de la soumission")
            data = {
                "ID Patient": [patient_id],
                "Nom": [full_name],
                "Date de naissance": [dob],
                "Sexe": [gender],
                "Poids (kg)": [weight],
                "Taille (cm)": [height],
                "Tension artérielle": [blood_pressure],
                "Température (°C)": [temperature],
                "Rythme cardiaque": [heart_rate],
                "Allergies": [allergies],
                "Diagnostic": [diagnosis],
                "Plan de traitement": [treatment_plan],
            }

            df = pd.DataFrame(data)
            st.dataframe(df)


# Pour que la page s'affiche correctement lorsque le module est importé
if __name__ == "__main__":
    render()
