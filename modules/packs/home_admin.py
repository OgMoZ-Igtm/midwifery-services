# modules/packs/home_admin.py
import streamlit as st

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="⚙️ Accueil Admin", page_icon="⚙️")
    st.title("⚙️ Bienvenue sur le tableau de bord d'administration")

    st.markdown(
        """
    Ce portail est votre centre de commande pour la gestion des utilisateurs, la configuration du système et la surveillance des activités.

    ### 🧭 Navigation
    - **Gestion des utilisateurs** : Créez, modifiez ou supprimez les comptes
    - **Logs d'audit** : Surveillez les accès et les actions
    - **Configuration du système** : Ajustez les paramètres globaux
    - **Statistiques** : Analysez l'utilisation et la performance
    - **Sécurité** : Gérez les permissions et les accès

    ### 🔐 Sécurité
    - Vos privilèges sont étendus, mais vos responsabilités aussi
    - Chaque action est enregistrée et auditée
    - Protégez votre mot de passe et vos informations d'identification

    ### 🧡 Notre mission
    Maintenir la stabilité et l'intégrité du système pour garantir un environnement sécurisé pour tous les professionnels de santé.
    """
    )
    st.image(
        "images/welcome_admin.png",
        caption="Votre centre de commande pour la gestion du système",
        use_container_width=True,
    )


if __name__ == "__main__":
    render()
