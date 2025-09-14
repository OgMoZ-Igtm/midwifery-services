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


def save_complication_to_db(db_client, user_id, complication_data):
    """Simule la sauvegarde d'une complication dans Firestore."""
    st.info(f"Sauvegarde de la complication pour l'utilisateur '{user_id}'...")
    st.session_state.complications.append(complication_data)
    st.success("Complication sauvegardée avec succès dans la base de données.")


def load_complications_from_db(db_client, user_id):
    """Simule le chargement des complications depuis Firestore."""
    st.info(f"Chargement des complications pour l'utilisateur '{user_id}'...")
    return st.session_state.get("complications", [])


def render():
    """
    Cette application Streamlit sert de formulaire sécurisé pour la saisie et le suivi
    des complications médicales chez les patientes en obstétrique.
    """
    st.title("🧠 Suivi des Complications Sécurisé")
    st.info(
        "Utilisez ce formulaire pour documenter et suivre les complications médicales de la patiente."
    )

    # Simuler un ID utilisateur pour la persistance des données
    user_id = "demo_user_complications"

    # Initialisation de la base de données
    db = get_firestore_client()
    if not db:
        st.warning(
            "Application en mode déconnecté. Les données ne seront pas sauvegardées de manière persistante."
        )
        if "complications" not in st.session_state:
            st.session_state.complications = []

    # Chargement initial des complications (si la connexion a réussi)
    if db and "complications" not in st.session_state:
        st.session_state.complications = load_complications_from_db(db, user_id)

    st.subheader("➕ Ajouter une nouvelle complication")
    with st.form("add_complication_form"):
        col1, col2 = st.columns(2)
        with col1:
            date_detection = st.date_input(
                "📅 Date de détection", datetime.now().date()
            )
            nom_patiente = st.text_input(
                "Nom de la patiente", placeholder="Ex: Mme Martin"
            )
            type_complication = st.selectbox(
                "Type de complication",
                [
                    "Pré-éclampsie",
                    "Diabète gestationnel",
                    "Hémorragie post-partum",
                    "Infection urinaire",
                    "Autre",
                ],
            )
        with col2:
            severite = st.selectbox("Sévérité", ["Légère", "Modérée", "Sévère"])
            statut = st.selectbox("Statut", ["En cours", "Géré", "Résolu"])
            cause = st.text_input(
                "Cause ou facteur de risque",
                placeholder="Ex: Antécédents familiaux, etc.",
            )

        notes = st.text_area(
            "Description et plan de suivi",
            placeholder="Décrivez la complication, les symptômes et le plan d'action...",
        )

        submitted = st.form_submit_button("✅ Enregistrer la complication")

        if submitted:
            if not nom_patiente or not type_complication:
                st.error(
                    "❌ Le nom de la patiente et le type de complication sont obligatoires."
                )
            else:
                new_complication = {
                    "Date": str(date_detection),
                    "Patiente": nom_patiente,
                    "Type": type_complication,
                    "Sévérité": severite,
                    "Statut": statut,
                    "Cause": cause,
                    "Notes": notes,
                    "created_at": str(datetime.now()),
                }
                save_complication_to_db(db, user_id, new_complication)
                st.experimental_rerun()

    st.markdown("---")

    st.subheader("📊 Vue d'ensemble des complications")
    complications_to_show = sorted(
        st.session_state.complications, key=lambda x: x["Date"], reverse=True
    )

    if complications_to_show:
        df_complications = pd.DataFrame(complications_to_show)
        st.dataframe(df_complications, use_container_width=True)
    else:
        st.info("Aucune complication n'est encore enregistrée.")

    st.markdown("---")
    st.write(f"ID utilisateur : **{user_id}**")


if __name__ == "__main__":
    render()
