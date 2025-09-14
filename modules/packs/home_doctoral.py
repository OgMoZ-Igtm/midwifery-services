# modules/packs/home_doctoral.py
import streamlit as st

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="🎓 Accueil Doctorant", page_icon="🎓")
    st.title("🎓 Bienvenue, Doctorant")

    st.markdown(
        """
    Ce portail est votre laboratoire numérique pour la recherche et la publication.

    ### 🧭 Navigation
    - **Recherches** : Gérez vos projets et vos données
    - **Publications** : Soumettez et suivez vos articles
    - **Statistiques** : Analysez vos données de recherche
    - **Bibliothèque** : Accédez à des ressources académiques et des revues
    - **Messagerie** : Communiquez avec votre comité de thèse

    ### 🔐 Sécurité
    - Assurez la confidentialité des données de recherche
    - Respectez les protocoles d'éthique et de protection des informations
    - Pour tout problème, contactez l'administrateur

    ### 🧡 Notre mission
    Soutenir votre travail académique pour faire avancer la connaissance dans le domaine de la santé.
    """
    )
    st.image(
        "images/welcome_doctoral.png",
        caption="Un espace pour la recherche et l'innovation",
        use_container_width=True,
    )


if __name__ == "__main__":
    render()
