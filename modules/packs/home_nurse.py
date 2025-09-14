# modules/packs/home_nurse.py
import streamlit as st

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="💉 Accueil Infirmière", page_icon="💉")
    st.title("💉 Bienvenue, Infirmière")

    st.markdown(
        """
    Ce portail est votre assistant pour la gestion des soins, la planification et la communication.

    ### 🧭 Navigation
    - **Plan de soins** : Gérez les tâches quotidiennes et les suivis
    - **Administration de médicaments** : Enregistrez et suivez les prescriptions
    - **Observations cliniques** : Notez les signes vitaux et les observations
    - **Rendez-vous** : Coordonnez le calendrier des consultations
    - **Messagerie** : Communiquez avec les autres professionnels

    ### 🔐 Sécurité
    - Vos accès sont personnels et sécurisés
    - Les données sont protégées et confidentielles
    - En cas de problème, contactez l’administrateur

    ### 🧡 Notre mission
    Optimiser les flux de travail pour vous permettre de vous concentrer sur le soin direct aux patients, avec précision et compassion.
    """
    )
    st.image(
        "images/welcome_nurse.png",
        caption="Un espace pour prendre soin avec efficacité et humanité",
        use_container_width=True,
    )


if __name__ == "__main__":
    render()
