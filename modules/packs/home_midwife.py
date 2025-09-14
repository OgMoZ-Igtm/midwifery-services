# modules/packs/home_midwife.py
import streamlit as st

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="🤱 Accueil Sage-femme", page_icon="🤱")
    st.title("🤱 Bienvenue, Sage-femme")

    st.markdown(
        """
    Ce portail est votre allié pour un suivi complet et personnalisé des patientes.

    ### 🧭 Navigation
    - **Dossiers de grossesse** : Gérez le suivi prénatal et post-partum
    - **Plans de naissance** : Accompagnez les patientes dans leurs projets
    - **Historique** : Consultez l'évolution de chaque cas
    - **Prescriptions** : Rédigez et suivez les traitements
    - **Messagerie** : Communiquez avec les autres professionnels

    ### 🔐 Sécurité
    - Vos accès sont personnels et sécurisés
    - Les données sont protégées et confidentielles
    - En cas de problème, contactez l’administrateur

    ### 🧡 Notre mission
    Offrir un espace numérique rigoureux, collaboratif et centré sur la santé des patientes.
    """
    )
    st.image(
        "images/welcome_midwife.png",
        caption="Un espace pour accompagner la vie, de la conception à la naissance",
        use_container_width=True,
    )


if __name__ == "__main__":
    render()
