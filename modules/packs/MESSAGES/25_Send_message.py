# BANNER_INJECTED
import streamlit as st
from datetime import datetime
import uuid

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )

# Simule l'utilisateur connecté
current_user = "Infirmier Jean"


def show():
    """
    Page pour envoyer un nouveau message sécurisé.
    """
    st.set_page_config(page_title="Envoyer un message", page_icon="📨", layout="wide")
    st.title("📨 Envoyer un message")
    st.markdown(
        "Composez un nouveau message sécurisé et envoyez-le à un ou plusieurs membres de l'équipe."
    )

    # Simuler une liste de destinataires et de patients
    destinataires = ["Admin", "Dr. Dupont", "Sage-femme Marie", "Infirmière Sophie"]
    patients = ["Mme Tremblay", "Mme Dubois", "Patient 302", "Nouveau patient"]

    # Utilisation d'un formulaire pour regrouper les entrées
    with st.form(key="message_form"):
        # --- Section : Destinataire et priorité ---
        st.subheader("1. Destinataire et Priorité")
        col1, col2 = st.columns(2)
        with col1:
            destinataire_choisi = st.selectbox(
                "Destinataire",
                options=destinataires,
                help="Sélectionnez le destinataire de votre message.",
            )
        with col2:
            priorite = st.selectbox(
                "Priorité du message",
                ["Normal", "Important", "Urgent"],
                index=0,
                help="Définissez le niveau d'urgence de ce message.",
            )

        # --- Section : Sujet et contenu ---
        st.subheader("2. Sujet et contenu")
        sujet = st.text_input("Sujet", placeholder="Entrez le sujet de votre message")

        # Ajout d'un champ pour associer le message à un patient
        patient_associe = st.selectbox(
            "Patient associé (optionnel)",
            options=["Aucun"] + patients,
            help="Sélectionnez le patient concerné par ce message.",
        )

        message_corps = st.text_area(
            "Message", placeholder="Tapez votre message ici...", height=200
        )

        # Ajout d'une option pour la confidentialité
        st.checkbox(
            "Ce message contient des informations confidentielles sur un patient.",
            help="Avertissement : Les messages sont sécurisés, mais la prudence est de mise lors de l'envoi d'informations sensibles.",
        )

        # --- Section : Envoi ---
        st.markdown("---")
        col_submit, col_info = st.columns([1, 2])
        with col_submit:
            envoyer_button = st.form_submit_button("Envoyer le message")
        with col_info:
            st.info(
                "Un identifiant unique sera automatiquement généré pour la traçabilité de ce message."
            )

    if envoyer_button:
        if not sujet or not message_corps:
            st.error("❌ Le sujet et le corps du message ne peuvent pas être vides.")
        else:
            # Dans une application réelle, cette partie enverrait les données à une base de données sécurisée (ex: Firestore).
            # Les données stockées seraient:
            # - un ID unique (uuid.uuid4())
            # - l'expéditeur (current_user)
            # - le destinataire (destinataire_choisi)
            # - le sujet (sujet)
            # - le contenu (message_corps)
            # - la date/heure (datetime.now())
            # - la priorité (priorite)
            # - le patient associé (patient_associe)

            message_id = str(uuid.uuid4())
            st.success(
                f"🎉 Votre message (ID: {message_id[:8]}) a été envoyé à **{destinataire_choisi}** avec la priorité **'{priorite}'** !"
            )
            st.balloons()


def render():
    show()


if __name__ == "__main__":
    render()
