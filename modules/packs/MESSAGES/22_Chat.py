# BANNER_INJECTED
import streamlit as st
from datetime import datetime
import uuid

# Cette variable simule l'utilisateur connecté dans une application réelle
# où l'authentification est gérée.
current_user = "Infirmière Sophie"
st.set_page_config(page_title="Chat interne sécurisé", page_icon="💬", layout="wide")


def render():
    """
    Cette application Streamlit sert de formulaire pour un chat interne,
    permettant aux collègues de communiquer en obstétrique de manière sécurisée.
    """
    st.title("💬 Chat interne")
    st.info("Échangez des messages avec vos collègues en temps réel en toute sécurité.")

    # Simuler la liste des patients et des utilisateurs connectés
    patients_list = ["Patient 1", "Patient 2", "Patient 3"]
    users_online = ["Dr. Dupont", "Sage-femme Marie", "Infirmière Sophie"]

    # Simuler une base de données de messages persistants
    # Dans une application réelle, on utiliserait une base de données comme Firestore.
    if "messages_db" not in st.session_state:
        st.session_state.messages_db = []

    # Afficher les messages existants, en les triant par heure
    st.subheader("Fil de conversation")

    if st.session_state.messages_db:
        # Trier les messages par date pour s'assurer qu'ils sont affichés dans l'ordre chronologique
        messages_sorted = sorted(
            st.session_state.messages_db, key=lambda x: x["timestamp"]
        )

        for message in messages_sorted:
            # Afficher le message avec des informations supplémentaires pour le contexte
            pseudo_display = f"**{message['pseudo']}**"
            date_display = f"({message['timestamp'].strftime('%H:%M:%S')})"
            patient_display = (
                f" - **Patient:** {message['patient']}"
                if message["patient"] != "Aucun"
                else ""
            )

            st.markdown(
                f"{pseudo_display} {date_display} {patient_display} - **Priorité:** {message['priority']}"
            )
            st.write(message["message"])
            st.markdown("---")
    else:
        st.info("Aucun message pour le moment.")

    # Formulaire pour envoyer un nouveau message
    st.subheader("Écrire un nouveau message")
    with st.form("chat_form"):
        col1, col2 = st.columns(2)
        with col1:
            patient_select = st.selectbox("Patient associé", ["Aucun"] + patients_list)
        with col2:
            priority_select = st.selectbox(
                "Priorité", ["Normal", "Important", "Urgent"]
            )

        message_body = st.text_area("Message", height=150)

        submit = st.form_submit_button("Envoyer le message")

        if submit:
            if not message_body:
                st.warning("❌ Veuillez remplir le champ 'Message'.")
            else:
                timestamp = datetime.now()
                new_message = {
                    "id": str(uuid.uuid4()),  # ID unique pour la traçabilité
                    "pseudo": current_user,  # Nom d'utilisateur automatique
                    "message": message_body,
                    "timestamp": timestamp,
                    "patient": patient_select,
                    "priority": priority_select,
                }
                st.session_state.messages_db.append(new_message)
                st.success("Message envoyé avec succès! 🎉")
                st.rerun()


if __name__ == "__main__":
    render()
