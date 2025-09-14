# BANNER_INJECTED
import streamlit as st
from datetime import datetime
import uuid
import pandas as pd

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


# This variable simulates the authenticated user. In a real-world app,
# this would be retrieved from the authentication system.
current_user = "Infirmière Sophie"


def render():
    """
    Cette application Streamlit sert de boîte de réception sécurisée pour les
    messages internes, avec des fonctionnalités de filtrage et de priorité.
    """
    st.set_page_config(page_title="Boîte de réception", page_icon="📬", layout="wide")
    st.title("📬 Boîte de réception")
    st.markdown(
        f"Bienvenue, **{current_user}**. Gérez et consultez vos messages en toute sécurité."
    )

    # We simulate a secure, persistent database for demonstration.
    # In a real application, this would be an API call to a database like Firestore.
    if "messages_db" not in st.session_state:
        st.session_state.messages_db = [
            {
                "id": str(uuid.uuid4()),
                "expediteur": "Admin",
                "destinataire": "Infirmière Sophie",
                "sujet": "Bienvenue !",
                "contenu": "Bonjour, bienvenue sur notre plateforme. Nous sommes ravis de vous compter parmi nous !",
                "date": "2025-08-29 10:00:00",
                "lu": False,
                "priorite": "Normal",
                "patient": "Aucun",
            },
            {
                "id": str(uuid.uuid4()),
                "expediteur": "Dr. Dupont",
                "destinataire": "Infirmière Sophie",
                "sujet": "Rappel de rendez-vous",
                "contenu": "N'oubliez pas le rendez-vous de Mme Tremblay le 05/09/2025 à 14h. Elle a des antécédents de diabète gestationnel.",
                "date": "2025-09-05 10:00:00",
                "lu": False,
                "priorite": "Important",
                "patient": "Mme Tremblay",
            },
            {
                "id": str(uuid.uuid4()),
                "expediteur": "Dr. Dubois",
                "destinataire": "Infirmière Sophie",
                "sujet": "CAS URGENT - Patient Dubois",
                "contenu": "Veuillez surveiller de près la pression artérielle de la patiente Dubois dans la chambre 302. J'ai un mauvais pressentiment. Rappelez-moi immédiatement en cas de changement.",
                "date": "2025-09-06 09:15:00",
                "lu": False,
                "priorite": "Urgent",
                "patient": "Mme Dubois",
            },
            {
                "id": str(uuid.uuid4()),
                "expediteur": "Laboratoire",
                "destinataire": "Infirmière Sophie",
                "sujet": "Résultats d'analyse",
                "contenu": "Les résultats des analyses de la patiente Dubois sont disponibles. Veuillez les consulter dans son dossier électronique.",
                "date": "2025-09-06 09:30:00",
                "lu": True,
                "priorite": "Normal",
                "patient": "Mme Dubois",
            },
        ]

    messages_recus = [
        msg
        for msg in st.session_state.messages_db
        if msg["destinataire"] == current_user
    ]

    if not messages_recus:
        st.info("Votre boîte de réception est vide.")
    else:
        st.subheader("Filtres")
        col_filtre1, col_filtre2, col_filtre3 = st.columns([1, 1, 2])

        with col_filtre1:
            filtre_lu = st.checkbox(
                "Afficher seulement les messages non lus", value=False
            )
        with col_filtre2:
            priorite_filtre = st.selectbox(
                "Priorité",
                ["Toutes les priorités", "Urgent", "Important", "Normal"],
                help="Filtrez les messages par niveau d'urgence.",
            )
        with col_filtre3:
            recherche = st.text_input(
                "Rechercher un message", placeholder="Sujet, expéditeur ou mot-clé..."
            )

        messages_filtres = []
        for msg in messages_recus:
            # Apply filters
            if filtre_lu and msg["lu"]:
                continue

            if (
                priorite_filtre != "Toutes les priorités"
                and msg["priorite"] != priorite_filtre
            ):
                continue

            if (
                recherche.lower() in msg["sujet"].lower()
                or recherche.lower() in msg["expediteur"].lower()
                or recherche.lower() in msg["contenu"].lower()
            ):
                messages_filtres.append(msg)

        # Sort messages by priority
        messages_filtres.sort(
            key=lambda x: {"Urgent": 0, "Important": 1, "Normal": 2}.get(
                x["priorite"], 3
            )
        )

        st.markdown("---")
        if not messages_filtres:
            st.info("Aucun message ne correspond à votre recherche.")
        else:
            st.subheader("Liste des messages")
            for msg in messages_filtres:
                status_icon = (
                    "🔴"
                    if msg["priorite"] == "Urgent"
                    else "🟡" if msg["priorite"] == "Important" else "⚪"
                )

                with st.expander(
                    f"{status_icon} **De:** {msg['expediteur']} - **Sujet:** {msg['sujet']} - **Date:** {msg['date']}",
                    expanded=False,
                ):
                    st.markdown(f"**Priorité :** {msg['priorite']}")
                    st.markdown(f"**Patient :** {msg['patient']}")
                    st.write(msg["contenu"])

                    if not msg["lu"]:
                        if st.button("Marquer comme lu", key=f"read_{msg['id']}"):
                            msg["lu"] = True
                            st.rerun()


if __name__ == "__main__":
    render()
