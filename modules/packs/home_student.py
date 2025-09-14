# modules/packs/home_student.py
import streamlit as st

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="📚 Accueil Étudiant", page_icon="📚")
    st.title("📚 Bienvenue, Étudiant")

    st.markdown(
        """
    Ce portail est votre ressource d'apprentissage et votre compagnon pour vos études cliniques.

    ### 🧭 Navigation
    - **Cours et modules** : Accédez au matériel pédagogique
    - **Cas cliniques** : Pratiquez vos compétences de diagnostic
    - **Bibliothèque** : Consultez des articles et des recherches
    - **Notes de cours** : Organisez et partagez vos observations
    - **Messagerie** : Communiquez avec vos professeurs et collègues

    ### 🔐 Sécurité
    - Les données de patient sont anonymisées ou à des fins de formation uniquement
    - Apprenez l'importance de la confidentialité et du respect des données
    - Pour toute question, contactez votre superviseur

    ### 🧡 Notre mission
    Vous offrir les outils nécessaires pour devenir un professionnel de la santé compétent et éthique.
    """
    )
    st.image(
        "images/welcome_student.png",
        caption="Un espace pour apprendre, grandir et se préparer à l'avenir",
        use_container_width=True,
    )


if __name__ == "__main__":
    render()
