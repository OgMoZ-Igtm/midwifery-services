# modules/packs/home_intern.py
import streamlit as st

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="🧑‍⚕️ Accueil Stagiaire", page_icon="🧑‍⚕️")
    st.title("🧑‍⚕️ Bienvenue, Stagiaire")

    st.markdown(
        """
    Ce portail est votre journal de bord pour un suivi optimal de votre stage.

    ### 🧭 Navigation
    - **Journal de stage** : Enregistrez vos observations et vos apprentissages
    - **Évaluations** : Suivez vos performances et obtenez du feedback
    - **Tâches** : Gérez vos responsabilités quotidiennes
    - **Ressources** : Accédez à des guides pratiques et des procédures
    - **Messagerie** : Communiquez avec votre superviseur

    ### 🔐 Sécurité
    - Les données de patient sont anonymisées ou à des fins de formation uniquement
    - Apprenez l'importance de la confidentialité et du respect des données
    - Pour toute question, contactez votre superviseur

    ### 🧡 Notre mission
    Vous offrir un environnement de travail structuré pour vous aider à atteindre vos objectifs de stage.
    """
    )
    st.image(
        "images/welcome_intern.png",
        caption="Un espace pour une expérience de stage enrichissante et organisée",
        use_container_width=True,
    )


if __name__ == "__main__":
    render()
