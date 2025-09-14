# BANNER_INJECTED
import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )

def render():
"""

# Simule une base de données (à remplacer par Supabase ou PostgreSQL)
def charger_messages():
    # Exemple de messages simulés
    return pd.DataFrame(
        [
            {
                "id": str(uuid.uuid4()),
                "expediteur": "Dr. Claire Dubois",
                "destinataire": "Sacré",
                "role_destinataire": "MIDWIFE",
                "message": "Merci pour le suivi du patient Martin. Très bon travail.",
                "lu": False,
                "envoye_le": datetime(2025, 9, 12, 14, 30),
            },
            {
                "id": str(uuid.uuid4()),
                "expediteur": "Admin",
                "destinataire": "Sacré",
                "role_destinataire": "MIDWIFE",
                "message": "Rappel : réunion d'équipe demain à 9h.",
                "lu": True,
                "envoye_le": datetime(2025, 9, 11, 10, 0),
            },
        ]
    )


def marquer_comme_lu(message_id, df):
    df.loc[df["id"] == message_id, "lu"] = True
    st.session_state["unread_messages"] = df[df["lu"] == False].shape[0]


def afficher_inbox():
    st.title("📨 Messagerie interne")
    st.info("Consultez vos messages professionnels en toute sécurité.")

    role = st.session_state.get("role", "GUEST").upper()
    utilisateur = st.session_state.get("nom", "Utilisateur")

    messages = charger_messages()
    messages_utilisateur = messages[
        (messages["destinataire"] == utilisateur)
        & (messages["role_destinataire"] == role)
    ].sort_values(by="envoye_le", ascending=False)

    if messages_utilisateur.empty:
        st.warning("📭 Aucun message pour le moment.")
        return

    for _, msg in messages_utilisateur.iterrows():
        with st.expander(
            f"De : {msg['expediteur']} — {msg['envoye_le'].strftime('%d/%m/%Y %H:%M')}"
        ):
            st.write(msg["message"])
            if not msg["lu"]:
                if st.button("✅ Marquer comme lu", key=msg["id"]):
                    marquer_comme_lu(msg["id"], messages)
                    st.success("Message marqué comme lu.")

    st.markdown("---")
    st.caption(f"🔒 {messages_utilisateur.shape[0]} message(s) reçu(s) — rôle : {role}")

    
if __name__ == "__main__":
    render()

