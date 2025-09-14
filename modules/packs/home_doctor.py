# BANNER_INJECTED
import streamlit as st

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="🩺 Accueil Médecin", page_icon="🩺")
    st.title("🩺 Bienvenue sur Midwifery Services")

    st.markdown(
        """
    Ce portail est conçu pour vous accompagner dans l’analyse clinique, le diagnostic, et la coordination des soins.

    ### 🧭 Navigation
    - **Demandes de consultation** : Gérez les requêtes des patientes
    - **Diagnostic** : Enregistrez vos observations et conclusions
    - **Historique médical** : Consultez les antécédents
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
        "images/welcome_doctor.png",
        caption="Un espace pour soigner avec précision et humanité",
        use_container_width=True,
    )


if __name__ == "__main__":
    render()
