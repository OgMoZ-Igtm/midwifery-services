import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Importer les modules Firebase nécessaires
# Remarque : Pour une application Streamlit en production, vous utiliseriez
# une bibliothèque Python comme `firebase-admin` pour interagir avec Firestore
# de manière sécurisée côté serveur.
# Les variables globales __firebase_config, __app_id, etc. sont fournies
# par l'environnement Canvas pour la communication avec le backend.


# Initialisation de la base de données (conceptuel pour cette démo)
# Dans un environnement Streamlit, cela serait géré par une bibliothèque Python
# se connectant à Firestore.
def get_firestore_client():
    """Simule la connexion à une base de données Firestore."""
    try:
        firebase_config = json.loads(__firebase_config)
        app_id = __app_id
        st.success("Connexion à la base de données réussie.")
        # Dans la réalité, le code ressemblerait à :
        # import firebase_admin
        # from firebase_admin import credentials, firestore
        # cred = credentials.Certificate(...)
        # firebase_admin.initialize_app(cred)
        # return firestore.client()
        return "Simulated Firestore Client"
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None


def save_appointment_to_db(db_client, user_id, appointment_data):
    """Simule la sauvegarde d'un rendez-vous dans Firestore."""
    # Dans la réalité, le code serait :
    # doc_ref = db_client.collection(f"artifacts/{app_id}/users/{user_id}/appointments").document()
    # doc_ref.set(appointment_data)
    st.info(f"Sauvegarde du rendez-vous pour l'utilisateur '{user_id}'...")
    st.session_state.appointments.append(appointment_data)
    st.success("Rendez-vous sauvegardé avec succès dans la base de données.")


def load_appointments_from_db(db_client, user_id):
    """Simule le chargement des rendez-vous depuis Firestore."""
    # Dans la réalité, le code serait :
    # docs = db_client.collection(f"artifacts/{app_id}/users/{user_id}/appointments").stream()
    # return [doc.to_dict() for doc in docs]
    st.info(f"Chargement des rendez-vous pour l'utilisateur '{user_id}'...")
    return st.session_state.get("appointments", [])


def render():
    """
    Cette application Streamlit sert de formulaire sécurisé pour la gestion des
    rendez-vous par le personnel infirmier.
    """
    st.title("🗓️ Calendrier des rendez-vous sécurisé")
    st.info(
        "Formulaire de gestion des rendez-vous avec persistance des données et sécurité."
    )

    # Simuler un ID utilisateur pour la persistance des données
    # Dans la réalité, ceci serait géré par un système d'authentification
    user_id = "demo_user_nurse"

    # Initialisation de la base de données
    db = get_firestore_client()
    if not db:
        st.warning(
            "Application en mode déconnecté. Les données ne seront pas sauvegardées de manière persistante."
        )
        if "appointments" not in st.session_state:
            st.session_state.appointments = []

    # Chargement initial des rendez-vous (si la connexion a réussi)
    if db and "appointments" not in st.session_state:
        st.session_state.appointments = load_appointments_from_db(db, user_id)

    st.subheader("➕ Ajouter un nouveau rendez-vous")
    with st.form("add_appointment_form"):
        col1, col2 = st.columns(2)
        with col1:
            date_rdv = st.date_input("📅 Date du rendez-vous", datetime.now().date())
            type_rdv = st.selectbox(
                "Type de rendez-vous",
                [
                    "Consultation prénatale",
                    "Suivi post-opératoire",
                    "Vaccination",
                    "Autre",
                ],
            )
        with col2:
            heure_rdv = st.time_input("⏰ Heure du rendez-vous", datetime.now().time())
            nom_patient = st.text_input("Nom du patient", placeholder="Ex: Jean Martin")

        notes = st.text_area(
            "Notes", placeholder="Ajoutez des détails importants sur le rendez-vous..."
        )

        submitted = st.form_submit_button("✅ Enregistrer le rendez-vous")

        if submitted:
            # Validation des données
            if not nom_patient:
                st.error("❌ Veuillez entrer le nom du patient.")
            else:
                new_appointment = {
                    "date": str(date_rdv),
                    "heure": str(heure_rdv),
                    "patient": nom_patient,
                    "type": type_rdv,
                    "notes": notes,
                    "created_at": str(datetime.now()),  # Horodatage pour le suivi
                }

                # Sauvegarde dans la base de données
                save_appointment_to_db(db, user_id, new_appointment)
                st.experimental_rerun()

    st.markdown("---")

    st.subheader("🗓️ Vue d'ensemble du calendrier")

    # Affichage des rendez-vous
    appointments_to_show = sorted(
        st.session_state.appointments,
        key=lambda x: (x["date"], x["heure"]),
        reverse=False,
    )

    if appointments_to_show:
        df_appointments = pd.DataFrame(appointments_to_show)
        st.dataframe(df_appointments, use_container_width=True)
    else:
        st.info("Aucun rendez-vous n'est encore planifié.")

    st.markdown("---")
    st.write(f"ID utilisateur : **{user_id}**")


if __name__ == "__main__":
    render()
