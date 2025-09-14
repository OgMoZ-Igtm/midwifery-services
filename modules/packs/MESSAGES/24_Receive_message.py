# BANNER_INJECTED
import streamlit as st
from datetime import datetime
import uuid

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


# Dans une application réelle, ceci serait géré par une base de données (ex: Firestore)
# et l'authentification de l'utilisateur.
# Nous simulons ici une base de données et un utilisateur connecté.
if "db" not in st.session_state:
    st.session_state.db = [
        {
            "id": str(uuid.uuid4()),
            "expediteur": "Admin",
            "destinataire": "Infirmier Jean",
            "sujet": "Bienvenue !",
            "contenu": "Bonjour, bienvenue sur notre plateforme. Nous sommes ravis de vous compter parmi nous !",
            "date": "2025-08-29 10:00:00",
            "lu": False,
            "priorite": "Normal",
        },
        {
            "id": str(uuid.uuid4()),
            "expediteur": "Dr. Dupont",
            "destinataire": "Infirmier Jean",
            "sujet": "Rappel de rendez-vous",
            "contenu": "N'oubliez pas le rendez-vous de Mme Tremblay le 05/09/2025 à 14h.",
            "date": "2025-08-28 17:30:00",
            "lu": False,
            "priorite": "Important",
        },
        {
            "id": str(uuid.uuid4()),
            "expediteur": "Dr. Dubois",
            "destinataire": "Infirmier Jean",
            "sujet": "CAS URGENT - Patient 302",
            "contenu": "Veuillez surveiller de près la pression artérielle de la patiente Dubois dans la chambre 302. J'ai un mauvais pressentiment. Rappelez-moi immédiatement en cas de changement.",
            "date": "2025-09-06 09:15:00",
            "lu": False,
            "priorite": "Urgent",
        },
        {
            "id": str(uuid.uuid4()),
            "expediteur": "Laboratoire",
            "destinataire": "Infirmier Jean",
            "sujet": "Résultats d'analyse",
            "contenu": "Les résultats des analyses de la patiente Dubois sont disponibles. Veuillez les consulter dans son dossier électronique.",
            "date": "2025-09-06 09:30:00",
            "lu": False,
            "priorite": "Normal",
        },
    ]


# Simule l'utilisateur connecté
# Dans une application réelle, le nom d'utilisateur serait récupéré depuis l'objet d'authentification.
current_user = "Infirmier Jean"


def show():
    """
    Page de réception des messages avec des fonctionnalités de sécurité et d'efficacité.
    """
    st.set_page_config(page_title="Boîte de réception", page_icon="📬", layout="wide")
    st.title("📬 Boîte de réception")
    st.markdown(
        "Gérez et consultez les messages que vous avez reçus en toute sécurité."
    )

    # Filtre les messages en fonction du destinataire
    messages_recus = [
        msg for msg in st.session_state.db if msg["destinataire"] == current_user
    ]

    if not messages_recus:
        st.info("Votre boîte de réception est vide.")
    else:
        # --- Section de recherche et de filtres ---
        st.markdown("---")
        st.subheader("Filtrage des messages")
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
            # Applique les filtres de lecture
            if filtre_lu and msg["lu"]:
                continue

            # Applique le filtre de priorité
            if (
                priorite_filtre != "Toutes les priorités"
                and msg["priorite"] != priorite_filtre
            ):
                continue

            # Applique le filtre de recherche
            if (
                recherche.lower() in msg["sujet"].lower()
                or recherche.lower() in msg["expediteur"].lower()
                or recherche.lower() in msg["contenu"].lower()
            ):
                messages_filtres.append(msg)

        # Trie les messages par priorité pour afficher les plus urgents en premier
        messages_filtres.sort(
            key=lambda x: {"Urgent": 0, "Important": 1, "Normal": 2}.get(
                x["priorite"], 3
            )
        )

        if not messages_filtres:
            st.info("Aucun message ne correspond à votre recherche.")
        else:
            st.markdown("---")
            st.subheader("Liste des messages")
            for msg in messages_filtres:
                # Ajout de l'icône de priorité
                if msg["priorite"] == "Urgent":
                    status_icon = "🔴"
                    color = "red"
                elif msg["priorite"] == "Important":
                    status_icon = "🟡"
                    color = "orange"
                else:
                    status_icon = "⚪"
                    color = "gray"

                # Mise en gras si le message n'est pas lu
                status_style = (
                    f"font-weight: bold; color: {color};" if not msg["lu"] else ""
                )

                with st.expander(
                    f"{status_icon} **De:** {msg['expediteur']} - **Sujet:** {msg['sujet']} - **Date:** {msg['date']}",
                    expanded=False,
                ):
                    st.markdown(
                        f"**Priorité :** {msg['priorite']}", unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<span style='{status_style}'>{msg['contenu']}</span>",
                        unsafe_allow_html=True,
                    )

                    if not msg["lu"]:
                        if st.button("Marquer comme lu", key=f"read_{msg['id']}"):
                            # Dans une vraie application, cela mettrait à jour la base de données
                            msg["lu"] = True
                            st.rerun()


# Fonction principale pour l'application
def render():
    show()


if __name__ == "__main__":
    render()
