# BANNER_INJECTED
import streamlit as st
import pandas as pd
from datetime import date
import json
import uuid

# Les modules Firebase ne sont pas importés directement dans Streamlit.
# Pour les besoins de ce démonstrateur, nous simulons l'intégration avec
# des fonctions qui représentent l'interaction avec Firestore.
# Les variables globales __firebase_config, __app_id, etc. sont fournies
# par l'environnement Canvas pour la communication avec le backend.


# --- Fonctions de simulation de base de données ---
def get_firestore_client():
    """Simule la connexion à une base de données Firestore."""
    try:
        # Tente de charger les configurations fournies par l'environnement
        _ = json.loads(__firebase_config)
        _ = __app_id
        st.session_state.db_connected = True
        return "Simulated Firestore Client"
    except (NameError, json.JSONDecodeError):
        st.session_state.db_connected = False
        return None


def get_user_id():
    """Simule l'obtention d'un ID utilisateur sécurisé."""
    # En production, on utiliserait le token d'authentification pour obtenir l'ID de l'utilisateur
    # Pour cette démo, on utilise un ID statique ou généré si non existant
    if "user_id" not in st.session_state:
        # Normalement, ceci serait basé sur le token d'authentification
        st.session_state.user_id = "demo_user_" + str(uuid.uuid4())
    return st.session_state.user_id


def save_patient_to_db(user_id, patient_id, patient_data):
    """Simule la sauvegarde ou la mise à jour d'un dossier patient dans Firestore."""
    st.info(f"💾 Sauvegarde du dossier patient...")

    # Simuler la sauvegarde dans un dictionnaire de session_state
    if "patients" not in st.session_state:
        st.session_state.patients = {}

    if user_id not in st.session_state.patients:
        st.session_state.patients[user_id] = {}

    st.session_state.patients[user_id][patient_id] = patient_data
    st.success("✅ Dossier sauvegardé avec succès.")


def load_patients_from_db(user_id):
    """Simule le chargement de tous les dossiers patients pour un utilisateur donné."""
    st.info(f"🔄 Chargement des dossiers patients...")
    if "patients" not in st.session_state:
        st.session_state.patients = {user_id: {}}

    # Données de démonstration pour un utilisateur spécifique
    if not st.session_state.patients.get(user_id):
        st.session_state.patients[user_id] = {
            str(uuid.uuid4()): {
                "Nom": "Mme Tremblay",
                "Numéro de Dossier": "123456",
                "Date de Naissance": "1992-05-15",
                "Sexe": "Femme",
                "Adresse": "123 Rue Principale, Montréal",
                "Téléphone": "+1 514 123 4567",
                "Diagnostic": "Grossesse à risque modéré, suivi intensif.",
            }
        }
    return st.session_state.patients[user_id]


def find_patient_by_file_number(user_id, file_number):
    """Recherche un patient dans la liste existante par numéro de dossier."""
    patients_data = st.session_state.patients.get(user_id, {})
    for patient_id, patient_data in patients_data.items():
        if patient_data.get("Numéro de Dossier") == file_number:
            return patient_id, patient_data
    return None, None


# --- Application Streamlit principale ---
def render():
    """
    Cette application Streamlit est un système sécurisé de gestion de dossiers
    médicaux pour les patientes. Elle permet de créer, consulter et
    modifier des dossiers détaillés.
    """
    st.title("🗂️ Système de Dossiers Médicaux Sécurisé")
    st.info(
        "Utilisez ce formulaire pour créer, consulter et mettre à jour un dossier médical complet."
    )

    # Simuler la connexion et obtenir l'ID utilisateur
    db = get_firestore_client()
    user_id = get_user_id()

    if not st.session_state.db_connected:
        st.warning(
            "⚠️ Application en mode déconnecté. Les données ne seront pas sauvegardées de manière persistante."
        )

    # Chargement initial des patients pour l'utilisateur
    if "patients_loaded" not in st.session_state:
        st.session_state.current_patients = load_patients_from_db(user_id)
        st.session_state.patients_loaded = True
        st.session_state.current_patient_id = None
        st.session_state.current_patient_data = {}

    # --- Section de recherche ---
    st.subheader("🔍 Rechercher ou sélectionner un dossier")

    file_numbers = [
        p["Numéro de Dossier"] for p in st.session_state.current_patients.values()
    ]
    selected_file_number = st.selectbox(
        "Sélectionner un numéro de dossier", ["Créer un nouveau"] + file_numbers
    )

    if selected_file_number != "Créer un nouveau":
        found_id, found_data = find_patient_by_file_number(
            user_id, selected_file_number
        )
        st.session_state.current_patient_id = found_id
        st.session_state.current_patient_data = found_data
    else:
        st.session_state.current_patient_id = None
        st.session_state.current_patient_data = {}

    st.markdown("---")

    # --- Section du formulaire de création/modification ---
    st.subheader("📝 Ajouter ou modifier un dossier")

    with st.form("dossier_patient_form"):
        # Définir les valeurs par défaut du formulaire
        default_data = st.session_state.current_patient_data

        # Section : Informations de base
        st.markdown("##### Informations de base")
        col1, col2 = st.columns(2)
        with col1:
            nom_complet = st.text_input(
                "Nom et prénom de la patiente",
                value=default_data.get("Nom", ""),
                placeholder="Ex: Mme Lucie Martin",
            )
            date_naissance = st.date_input(
                "📅 Date de naissance",
                value=pd.to_datetime(
                    default_data.get("Date de Naissance", date.today().isoformat())
                ),
                max_value=date.today(),
            )
        with col2:
            numero_dossier = st.text_input(
                "Numéro de dossier",
                value=default_data.get("Numéro de Dossier", ""),
                placeholder="Ex: 123456",
            )
            sexe = st.selectbox(
                "Sexe",
                ["Femme", "Homme", "Autre"],
                index=["Femme", "Homme", "Autre"].index(
                    default_data.get("Sexe", "Femme")
                ),
            )
            groupe_sanguin = st.selectbox(
                "Groupe sanguin",
                ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Inconnu"],
                index=[
                    "A+",
                    "A-",
                    "B+",
                    "B-",
                    "AB+",
                    "AB-",
                    "O+",
                    "O-",
                    "Inconnu",
                ].index(default_data.get("Groupe sanguin", "Inconnu")),
            )

        st.markdown("---")

        # Section : Informations de contact et d'urgence
        st.markdown("##### Informations de contact et d'urgence")
        col3, col4 = st.columns(2)
        with col3:
            telephone = st.text_input(
                "Numéro de téléphone",
                value=default_data.get("Téléphone", ""),
                placeholder="Ex: +33 6 12 34 56 78",
            )
            adresse = st.text_area(
                "Adresse complète",
                value=default_data.get("Adresse", ""),
                placeholder="Ex: 12 Rue de la Paix, 75000 Paris",
            )
        with col4:
            nom_contact_urgence = st.text_input(
                "Nom du contact d'urgence",
                value=default_data.get("Nom Contact Urgence", ""),
                placeholder="Ex: Marc Martin",
            )
            relation_contact = st.text_input(
                "Relation avec la patiente",
                value=default_data.get("Relation Contact", ""),
                placeholder="Ex: Époux, frère, ami(e)...",
            )
            telephone_contact = st.text_input(
                "Téléphone du contact d'urgence",
                value=default_data.get("Téléphone Contact", ""),
                placeholder="Ex: +33 6 98 76 54 32",
            )

        st.markdown("---")

        # Section : Antécédents médicaux et diagnostic
        st.markdown("##### Antécédents médicaux et diagnostic")
        allergies = st.text_area(
            "Allergies",
            value=default_data.get("Allergies", ""),
            placeholder="Ex: Pénicilline, arachides...",
        )
        antecedents_medicaux = st.text_area(
            "Antécédents médicaux pertinents",
            value=default_data.get("Antécédents Médicaux", ""),
            placeholder="Ex: Diabète, hypertension, chirurgies antérieures...",
        )
        diagnostic = st.text_area(
            "Diagnostic médical",
            value=default_data.get("Diagnostic", ""),
            placeholder="Saisissez ici le diagnostic principal.",
        )

        st.markdown("---")

        # Section : Historique des grossesses (Obstétrique)
        st.markdown("##### Historique des grossesses (Obstétrique)")
        col5, col6 = st.columns(2)
        with col5:
            gravida = st.number_input(
                "Nombre de grossesses (Gravida)",
                value=default_data.get("Gravida", 0),
                min_value=0,
                step=1,
            )
            date_derniere_regle = st.date_input(
                "Date des dernières règles (DDR)",
                value=pd.to_datetime(default_data.get("DDR", date.today().isoformat())),
                max_value=date.today(),
            )
        with col6:
            parite = st.number_input(
                "Nombre de naissances (Parité)",
                value=default_data.get("Parité", 0),
                min_value=0,
                step=1,
            )
            nombre_cesariennes = st.number_input(
                "Nombre de césariennes",
                value=default_data.get("Césariennes", 0),
                min_value=0,
                step=1,
            )

        notes_grossesse = st.text_area(
            "Notes sur les grossesses précédentes",
            value=default_data.get("Notes Grossesse", ""),
            placeholder="Complications, accouchements particuliers...",
        )

        st.markdown("---")

        # Section : Saisie de documents
        st.markdown("##### Saisie de documents")
        uploaded_files = st.file_uploader(
            "📥 Ajouter des documents (échographies, rapports, etc.)",
            accept_multiple_files=True,
        )
        if uploaded_files:
            st.success(
                f"{len(uploaded_files)} fichier(s) prêt(s) à être enregistré(s)."
            )

        submit = st.form_submit_button("✅ Enregistrer le dossier")

        if submit:
            # Validation des données
            if not nom_complet or not numero_dossier:
                st.error(
                    "❌ Veuillez remplir les champs obligatoires : Nom et prénom, et Numéro de dossier."
                )
            else:
                new_data = {
                    "Nom": nom_complet,
                    "Numéro de Dossier": numero_dossier,
                    "Date de Naissance": str(date_naissance),
                    "Sexe": sexe,
                    "Groupe sanguin": groupe_sanguin,
                    "Téléphone": telephone,
                    "Adresse": adresse,
                    "Nom Contact Urgence": nom_contact_urgence,
                    "Relation Contact": relation_contact,
                    "Téléphone Contact": telephone_contact,
                    "Allergies": allergies,
                    "Antécédents Médicaux": antecedents_medicaux,
                    "Diagnostic": diagnostic,
                    "Gravida": gravida,
                    "Parité": parite,
                    "Césariennes": nombre_cesariennes,
                    "DDR": str(date_derniere_regle),
                    "Notes Grossesse": notes_grossesse,
                }

                # Attribuer ou conserver l'ID du patient
                patient_id = (
                    st.session_state.current_patient_id
                    if st.session_state.current_patient_id
                    else str(uuid.uuid4())
                )

                # Sauvegarde du dossier
                save_patient_to_db(user_id, patient_id, new_data)

                # Recharger l'application pour afficher les données mises à jour
                st.experimental_rerun()

    st.markdown("---")

    # --- Section : Vue d'ensemble des dossiers ---
    st.subheader("📊 Vue d'ensemble des dossiers")
    if st.session_state.current_patients:
        df_patients = pd.DataFrame.from_dict(
            st.session_state.current_patients, orient="index"
        )
        df_patients.reset_index(inplace=True)
        df_patients.rename(columns={"index": "ID Dossier (UUID)"}, inplace=True)
        st.dataframe(df_patients, use_container_width=True)
    else:
        st.info("Aucun dossier de patiente n'est encore enregistré.")

    st.markdown("---")
    st.write(f"ID Utilisateur : **{user_id}**")


# Point d'entrée de l'application
if __name__ == "__main__":
    render()
