# BANNER_INJECTED
import streamlit as st
from datetime import date

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    """
    Cette application Streamlit sert de formulaire pour la prise de rendez-vous
    par la patiente avec un médecin ou une sage-femme.
    """
    st.title("📅 Prise de rendez-vous")
    st.info("Utilisez ce formulaire pour planifier votre prochain rendez-vous médical.")

    with st.form("rendezvous_form"):
        st.subheader("Informations de base")

        col1, col2 = st.columns(2)
        with col1:
            nom_patient = st.text_input(
                "Votre nom et prénom", placeholder="Ex: Lucie Martin"
            )
            date_naissance = st.date_input(
                "Votre date de naissance", max_value=date.today()
            )
        with col2:
            raison_rdv = st.text_area(
                "Raison du rendez-vous",
                placeholder="Ex: Consultation prénatale de routine, questions sur l'allaitement, etc.",
            )

        st.markdown("---")

        st.subheader("Détails du rendez-vous souhaité")

        medecin_specialiste = st.selectbox(
            "Médecin ou sage-femme souhaité(e)",
            [
                "Dr. Claire Dubois (Gynécologue)",
                "Dr. Paul Durand (Généraliste)",
                "Mme Jeanne Morin (Sage-femme)",
                "Peu importe",
            ],
        )

        col3, col4 = st.columns(2)
        with col3:
            date_souhaitee = st.date_input("📅 Date souhaitée", min_value=date.today())
        with col4:
            heure_souhaitee = st.time_input("⏰ Heure souhaitée")

        st.markdown("---")

        email = st.text_input(
            "Votre adresse e-mail", placeholder="Ex: votre.email@example.com"
        )
        telephone = st.text_input(
            "Votre numéro de téléphone", placeholder="Ex: +33 6 12 34 56 78"
        )

        submit = st.form_submit_button("✅ Demander le rendez-vous")

        if submit:
            if nom_patient and raison_rdv and date_souhaitee:
                st.success(
                    "✅ Votre demande de rendez-vous a été envoyée. Nous vous contacterons sous peu pour la confirmation."
                )
                st.balloons()
            else:
                st.error(
                    "❌ Veuillez remplir les champs obligatoires : nom, raison du rendez-vous et date souhaitée."
                )


if __name__ == "__main__":
    render()
