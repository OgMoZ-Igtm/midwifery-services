import streamlit as st
import pandas as pd
from datetime import date, datetime


def render():
    """
    Page : Historique médical du patient
    Rôle : DOCTOR
    Objectif : Permet au médecin de consulter ou compléter l’historique médical.
    """
    st.set_page_config(
        page_title="Historique médical du patient", page_icon="📜", layout="wide"
    )

    st.title("📜 Historique médical du patient")
    st.info(
        "Cette page est destinée aux médecins pour **documenter les antécédents médicaux** d’un patient (allergies, antécédents familiaux, grossesses précédentes, etc.)."
    )

    # Simulation d'une base de données de patients
    patients_data = {
        "id": ["pat_001", "pat_002", "pat_003"],
        "nom": ["Alice Martin", "Julien Dubois", "Léa Garnier"],
    }
    df_patients = pd.DataFrame(patients_data)

    # --- Section de sélection du patient et affichage de l'historique ---
    st.subheader("Sélection du patient")

    selected_patient_name = st.selectbox(
        "Sélectionnez le patient",
        df_patients["nom"].tolist(),
        help="Recherchez et sélectionnez le patient pour accéder à son dossier.",
    )

    # Affichage de l'historique existant (simulé)
    st.markdown(f"### Historique pour **{selected_patient_name}**")
    st.warning(
        "⚠️ Fonctionnalité en cours de développement : Affichage de l'historique complet (diagnostics, traitements, etc.)"
    )
    st.dataframe(
        pd.DataFrame(
            {
                "Date": ["2023-05-10", "2023-08-15"],
                "Type de consultation": ["Initial", "Suivi pré-natal"],
                "Diagnostic": ["Grossesse à 8 SA", "Diabète gestationnel"],
            }
        )
    )

    st.markdown("---")

    # --- Formulaire de saisie pour ajouter une nouvelle entrée à l'historique ---
    st.subheader("Ajouter une nouvelle entrée à l'historique")

    with st.form("historique_medical_form"):
        # Informations de base (patient et médecin sont gérés par le système)
        st.write("Date de l'entrée : ", date.today().strftime("%Y-%m-%d"))

        # --- Section 2: Antécédents médicaux et chirurgicaux ---
        st.subheader("2. Antécédents médicaux et chirurgicaux")
        col1, col2 = st.columns(2)

        with col1:
            medical_history = st.text_area(
                "📖 Antécédents médicaux pertinents",
                placeholder="Diabète, hypertension, maladies cardiaques, etc.",
            )
            allergies_list = st.multiselect(
                "🤧 Allergies connues",
                [
                    "Pénicilline",
                    "Acide acétylsalicylique (aspirine)",
                    "Arachides",
                    "Lactose",
                ],
                help="Sélectionnez toutes les allergies connues du patient.",
            )

        with col2:
            surgical_history = st.text_area(
                "🩺 Chirurgies passées",
                placeholder="Appendicectomie, césarienne, hystérectomie, etc.",
            )
            medications = st.text_area(
                "💉 Médicaments actuels",
                placeholder="Nom du médicament, posologie, fréquence (ex: Paracétamol 500mg, 1x/jour)",
            )
            st.warning(
                "⚠️ Les champs Médicaments et Allergies devraient être liés à une base de données standardisée pour plus de sécurité."
            )

        st.markdown("---")

        # --- Section 3: Antécédents familiaux ---
        st.subheader("3. Antécédents familiaux")
        st.text_area(
            "👨‍👩‍👧‍👦 Antécédents familiaux",
            placeholder="Ex: Diabète, cancers, maladies génétiques, etc.",
        )

        st.markdown("---")

        # --- Section 4: Historique gynécologique et obstétrical (structuré) ---
        st.subheader("4. Historique gynécologique et obstétrical (GTPAL)")
        col3, col4, col5, col6, col7 = st.columns(5)

        # Utilisation de la notation standard GTPAL
        with col3:
            gravida = st.number_input(
                "Gravida (Nombre total de grossesses)", min_value=0, step=1
            )
        with col4:
            term = st.number_input("Nombre de naissances à terme", min_value=0, step=1)
        with col5:
            preterm = st.number_input(
                "Nombre de naissances prématurées", min_value=0, step=1
            )
        with col6:
            abortion = st.number_input(
                "Nombre de fausses couches/avortements", min_value=0, step=1
            )
        with col7:
            living = st.number_input("Nombre d'enfants vivants", min_value=0, step=1)

        st.text_area(
            "Historique gynécologique et complications",
            placeholder="Cycles menstruels, infections, complications des grossesses précédentes, etc.",
        )

        st.markdown("---")

        # Bouton de soumission avec horodatage
        submit = st.form_submit_button("💾 Enregistrer l'historique")

    if submit:
        # Ici, vous ajouteriez la logique de sauvegarde dans une vraie base de données
        # avec l'horodatage et l'ID du médecin
        st.success(
            f"✅ Historique médical pour {selected_patient_name} sauvegardé le {datetime.now().strftime('%Y-%m-%d à %H:%M')}."
        )
        st.balloons()


if __name__ == "__main__":
    render()
