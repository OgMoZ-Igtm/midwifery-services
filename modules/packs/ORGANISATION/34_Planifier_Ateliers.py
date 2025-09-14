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
def get_firestore_client():
    """Simule la connexion à une base de données Firestore."""
    try:
        firebase_config = json.loads(__firebase_config)
        app_id = __app_id
        st.success("Connexion à la base de données réussie.")
        return "Simulated Firestore Client"
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None


def save_event_to_db(db_client, user_id, event_data):
    """Simule la sauvegarde d'un événement dans Firestore."""
    st.info(f"Sauvegarde de l'événement pour l'utilisateur '{user_id}'...")
    st.session_state.events.append(event_data)
    st.success("Événement sauvegardé avec succès dans la base de données.")


def load_events_from_db(db_client, user_id):
    """Simule le chargement des événements depuis Firestore."""
    st.info(f"Chargement des événements pour l'utilisateur '{user_id}'...")
    return st.session_state.get("events", [])


def render():
    """
    Cette application Streamlit sert de calendrier sécurisé pour la gestion des
    événements et des ateliers de prévention en obstétrique.
    """
    st.title("🗓️ Calendrier des événements et ateliers sécurisé")
    st.info(
        "Planifiez, gérez et consultez les événements de prévention pour les patientes."
    )

    # Simuler un ID utilisateur pour la persistance des données
    user_id = "demo_user_organisation"

    # Initialisation de la base de données
    db = get_firestore_client()
    if not db:
        st.warning(
            "Application en mode déconnecté. Les données ne seront pas sauvegardées de manière persistante."
        )
        if "events" not in st.session_state:
            st.session_state.events = []

    # Chargement initial des événements (si la connexion a réussi)
    if db and "events" not in st.session_state:
        st.session_state.events = load_events_from_db(db, user_id)

    st.subheader("➕ Ajouter un nouvel événement ou atelier")
    with st.form("add_event_form"):
        col1, col2 = st.columns(2)
        with col1:
            date_event = st.date_input("📅 Date de l'événement", datetime.now().date())
            sujet_event = st.text_input(
                "Sujet de l'événement",
                placeholder="Ex: Atelier sur la gestion du stress",
            )
            lieu = st.text_input("Lieu", placeholder="Ex: Salle de conférence A")
        with col2:
            heure_event = st.time_input(
                "⏰ Heure de l'événement", datetime.now().time()
            )
            participants = st.number_input(
                "Nombre de participants", min_value=0, step=1
            )

        notes = st.text_area(
            "Notes importantes",
            placeholder="Ajoutez des détails sur le contenu et le matériel nécessaire...",
        )

        submitted = st.form_submit_button("✅ Enregistrer l'événement")

        if submitted:
            if not sujet_event or participants is None:
                st.error(
                    "❌ Le sujet et le nombre de participants sont des champs obligatoires."
                )
            else:
                new_event = {
                    "Date": str(date_event),
                    "Heure": str(heure_event),
                    "Sujet": sujet_event,
                    "Lieu": lieu,
                    "Participants": str(participants),
                    "Notes": notes,
                    "created_at": str(datetime.now()),
                }

                save_event_to_db(db, user_id, new_event)
                st.experimental_rerun()

    st.markdown("---")

    st.subheader("🗓️ Vue d'ensemble du calendrier des événements")

    events_to_show = sorted(
        st.session_state.events,
        key=lambda x: (x["Date"], x["Heure"]),
        reverse=False,
    )

    if events_to_show:
        df_events = pd.DataFrame(events_to_show)
        st.dataframe(df_events, use_container_width=True)
    else:
        st.info("Aucun événement n'est encore planifié.")

    st.markdown("---")
    st.write(f"ID utilisateur : **{user_id}**")


if __name__ == "__main__":
    render()
