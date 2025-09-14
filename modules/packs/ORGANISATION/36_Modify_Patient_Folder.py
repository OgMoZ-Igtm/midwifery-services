import streamlit as st
import pandas as pd
from datetime import datetime
import json
import uuid

# Les modules Firebase ne sont pas importés directement dans Streamlit
# Pour les besoins de ce démonstrateur, nous simulons l'intégration avec
# des fonctions qui représentent l'interaction avec Firestore.
# Les variables globales __firebase_config, __app_id, etc. sont fournies
# par l'environnement Canvas pour la communication avec le backend.


# Initialisation de la base de données (conceptuel pour cette démo)
def get_firestore_client():
    """Simule la connexion à une base de données Firestore."""
    try:
        firebase_config = json.loads(__firebase_config)
        app_id = __app_id
        return "Simulated Firestore Client"
    except Exception as e:
        st.error(f"❌ Erreur de connexion à la base de données : {e}")
        return None


def save_patient_to_db(db_client, user_id, patient_id, patient_data):
    """
    Simule la sauvegarde ou la mise à jour d'un dossier patient dans Firestore.
    Le dossier est stocké avec un ID unique pour la persistance.
    """
    st.info(
        f"💾 Sauvegarde du dossier patient '{patient_id}' pour l'utilisateur '{user_id}'..."
    )

    # Simuler la sauvegarde en mettant à jour la session_state
    if "patients" not in st.session_state:
        st.session_state.patients = {}

    st.session_state.patients[patient_id] = patient_data
    st.success("✅ Dossier sauvegardé avec succès dans la base de données.")


def load_patients_from_db(db_client, user_id):
    """Simule le chargement de tous les dossiers patients depuis Firestore."""
    st.info(f"🔄 Chargement des dossiers patients pour l'utilisateur '{user_id}'...")
    # Données de démonstration persistantes
    if "patients" not in st.session_state:
        st.session_state.patients = {
            str(uuid.uuid4()): {
                "Nom": "Mme Tremblay",
                "Date de Naissance": "1992-05-15",
                "Numéro de Dossier": "123456",
                "Historique Médical": "Antécédents de diabète gestationnel.",
                "Dernière Consultation": str(datetime.now().date()),
            },
            str(uuid.uuid4()): {
                "Nom": "Mme Dubois",
                "Date de Naissance": "1988-11-22",
                "Numéro de Dossier": "654321",
                "Historique Médical": "Grossesse à risque modéré, suivi intensif.",
                "Dernière Consultation": str(datetime.now().date()),
            },
        }
    return st.session_state.patients


def find_patient_by_name(patient_name):
    """Recherche un patient dans la liste existante par nom."""
    if "patients" in st.session_state:
        for patient_id, patient_data in st.session_state.patients.items():
            if patient_data.get("Nom", "").lower() == patient_name.lower():
                return patient_id, patient_data
    return None, None


def render():
    """
    Cette application Streamlit permet de rechercher, d'ajouter et de modifier
    les dossiers des patientes en obstétrique de manière sécurisée.
    """
    st.title("📂 Gestion Sécurisée des Dossiers Patients")
    st.info(
        "Recherchez, modifiez ou créez des dossiers de patientes avec ce formulaire sécurisé."
    )

    # Simuler un ID utilisateur pour la persistance des données
    user_id = "demo_user_patients"

    # Initialisation de la base de données
    db = get_firestore_client()
    if not db:
        st.warning(
            "Application en mode déconnecté. Les données ne seront pas sauvegardées de manière persistante."
        )

    # Chargement initial des patients
    load_patients_from_db(db, user_id)

    # État pour gérer la sélection d'un patient
    if "current_patient_id" not in st.session_state:
        st.session_state.current_patient_id = None
        st.session_state.current_patient_data = None

    # ---
    # Section de recherche
    # ---
    st.subheader("🔍 Rechercher une patiente")
    search_query = st.text_input(
        "Rechercher par nom de patiente", placeholder="Ex: Mme Tremblay"
    )
    search_button = st.button("Rechercher")

    if search_button and search_query:
        found_id, found_data = find_patient_by_name(search_query)
        if found_id:
            st.session_state.current_patient_id = found_id
            st.session_state.current_patient_data = found_data
            st.success(
                f"✅ Dossier de '{found_data['Nom']}' trouvé. Le formulaire est pré-rempli pour la modification."
            )
        else:
            st.session_state.current_patient_id = None
            st.session_state.current_patient_data = None
            st.warning(
                "⚠️ Aucune patiente trouvée avec ce nom. Vous pouvez en créer une nouvelle ci-dessous."
            )

    # ---
    # Section du formulaire
    # ---
    st.subheader("📝 Ajouter ou modifier un dossier")
    with st.form("patient_folder_form"):
        # Les valeurs par défaut du formulaire sont celles du patient sélectionné
        default_name = (
            st.session_state.current_patient_data.get("Nom", "")
            if st.session_state.current_patient_data
            else ""
        )
        default_dob = (
            st.session_state.current_patient_data.get(
                "Date de Naissance", datetime.now().date().isoformat()
            )
            if st.session_state.current_patient_data
            else datetime.now().date().isoformat()
        )
        default_file_number = (
            st.session_state.current_patient_data.get("Numéro de Dossier", "")
            if st.session_state.current_patient_data
            else ""
        )
        default_history = (
            st.session_state.current_patient_data.get("Historique Médical", "")
            if st.session_state.current_patient_data
            else ""
        )

        col1, col2 = st.columns(2)
        with col1:
            nom_patiente = st.text_input(
                "Nom de la patiente", value=default_name, placeholder="Ex: Mme Martin"
            )
            numero_dossier = st.text_input(
                "Numéro de Dossier", value=default_file_number, placeholder="Ex: 123456"
            )
        with col2:
            date_naissance = st.date_input(
                "Date de Naissance",
                value=(
                    datetime.strptime(default_dob, "%Y-%m-%d").date()
                    if default_dob
                    else datetime.now().date()
                ),
            )

        historique = st.text_area(
            "Historique Médical et Notes",
            value=default_history,
            placeholder="Historique des grossesses, pathologies, etc.",
        )

        submitted = st.form_submit_button("✅ Enregistrer le dossier")

        if submitted:
            # Validation des données
            if not nom_patiente or not numero_dossier:
                st.error(
                    "❌ Le nom de la patiente et le numéro de dossier sont obligatoires."
                )
            else:
                new_data = {
                    "Nom": nom_patiente,
                    "Date de Naissance": str(date_naissance),
                    "Numéro de Dossier": numero_dossier,
                    "Historique Médical": historique,
                    "Dernière Consultation": str(datetime.now().date()),
                }

                patient_id = (
                    st.session_state.current_patient_id
                    if st.session_state.current_patient_id
                    else str(uuid.uuid4())
                )

                # Sauvegarde ou mise à jour du dossier dans la base de données
                save_patient_to_db(db, user_id, patient_id, new_data)

                # Réinitialiser la sélection
                st.session_state.current_patient_id = None
                st.session_state.current_patient_data = None
                st.experimental_rerun()

    # ---
    # Vue d'ensemble des dossiers
    # ---
    st.markdown("---")
    st.subheader("📊 Vue d'ensemble des dossiers patients")
    if "patients" in st.session_state and st.session_state.patients:
        df_patients = pd.DataFrame.from_dict(st.session_state.patients, orient="index")
        st.dataframe(df_patients, use_container_width=True)
    else:
        st.info("Aucun dossier de patiente n'est encore enregistré.")

    st.markdown("---")
    st.write(f"ID utilisateur : **{user_id}**")


if __name__ == "__main__":
    render()
