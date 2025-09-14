# modules/packs/saisie_medicaments.py
import streamlit as st
from datetime import datetime


# =========================================================
# 📝 FORMULAIRE DE SAISIE
# =========================================================
def render():
    """
    Rend l'interface du formulaire de saisie de médicaments.
    """
    st.header("Saisie de Médicaments pour Patient")
    st.markdown("---")

    # Initialisation de la liste des médicaments enregistrés dans la session
    if "medications_list" not in st.session_state:
        st.session_state.medications_list = []

    with st.form(key="medication_form", clear_on_submit=True):
        st.subheader("Informations Patient")
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("ID Patient", placeholder="Ex: P-4567-890")
        with col2:
            nom_patient = st.text_input(
                "Nom Complet du Patient", placeholder="Ex: Sarah Dubois"
            )

        st.subheader("Informations Médicament")
        nom_medicament = st.text_input("Nom du Médicament", placeholder="Ex: Oxytocine")
        dose = st.text_input("Dose", placeholder="Ex: 10 UI")
        voie = st.selectbox(
            "Voie d'Administration",
            options=[
                "Intraveineuse (IV)",
                "Intramusculaire (IM)",
                "Orale",
                "Sous-cutanée",
                "Topique",
                "Autre",
            ],
        )
        frequence = st.text_input(
            "Fréquence d'Administration", placeholder="Ex: 1x/jour"
        )
        motif = st.text_area(
            "Motif de l'Administration", placeholder="Ex: Induction du travail"
        )

        st.subheader("Vérification et Signature")
        nom_infirmiere = st.text_input(
            "Nom de l'Infirmière", st.session_state.get("full_name", "")
        )

        st.info(
            "Vérification en double : La dose et le médicament ont-ils été vérifiés par un autre professionnel de la santé ?"
        )
        verification_double = st.checkbox("Oui, double vérification effectuée")

        st.markdown("---")
        submit_button = st.form_submit_button("Enregistrer la Saisie")

    if submit_button:
        # Vérification de la validité des champs
        if not all(
            [patient_id, nom_patient, nom_medicament, dose, voie, nom_infirmiere]
        ):
            st.error("❌ Veuillez remplir tous les champs obligatoires.")
        elif not verification_double:
            st.warning(
                "⚠️ L'administration doit être doublement vérifiée pour la sécurité du patient."
            )
        else:
            # Création du dictionnaire de données
            data_saisie = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "patient_id": patient_id,
                "nom_patient": nom_patient,
                "nom_medicament": nom_medicament,
                "dose": dose,
                "voie_administration": voie,
                "frequence": frequence,
                "motif": motif,
                "nom_infirmiere": nom_infirmiere,
                "verification_double": verification_double,
            }

            # Ajout des données à la liste en session
            st.session_state.medications_list.append(data_saisie)
            st.success("✅ La saisie du médicament a été enregistrée avec succès.")

            # Affichage de la dernière saisie pour confirmation visuelle
            st.markdown("---")
            st.subheader("Dernière Saisie Enregistrée")
            st.json(st.session_state.medications_list[-1])

    st.markdown("---")
    if st.session_state.medications_list:
        st.subheader("Historique des Saisies")
        st.table(st.session_state.medications_list)
