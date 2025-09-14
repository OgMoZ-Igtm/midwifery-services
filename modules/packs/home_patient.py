# modules/packs/home_patient.py
import streamlit as st

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="💖 Accueil Patient", page_icon="💖")
    st.title("💖 Bienvenue sur votre espace personnel")

    st.markdown(
        """
    Cet espace est conçu pour vous accompagner dans votre parcours de santé et vous connecter avec votre équipe soignante.

    ### 🧭 Navigation
    - **Mon dossier médical** : Consultez votre historique, vos rendez-vous et vos prescriptions
    - **Ressources** : Accédez à des informations fiables sur la santé maternelle et infantile
    - **Messagerie** : Communiquez en toute sécurité avec votre sage-femme ou votre médecin
    - **Rendez-vous** : Gérez vos prochaines consultations

    ### 🔐 Confidentialité
    - Vos données sont strictement confidentielles et accessibles uniquement par vous-même et votre équipe soignante
    - Ne partagez jamais vos identifiants
    - Déconnectez-vous toujours après utilisation

    ### 🧡 Notre mission
    Vous donner le pouvoir de prendre part activement à votre bien-être, en toute confiance et sécurité.
    """
    )
    st.image(
        "images/welcome_patient.png",
        caption="Un espace pour gérer votre santé en toute confiance",
        use_container_width=True,
    )


if __name__ == "__main__":
    render()
