import streamlit as st

st.set_page_config(
    page_title="Accueil",
    page_icon="🏠",
)

st.title("Système de gestion de la Clinique de Sages-Femmes")
st.sidebar.success("Sélectionnez une option de connexion ci-dessus.")

st.markdown(
    """
    Bienvenue sur le système de gestion de la Clinique de Sages-Femmes.
    Veuillez vous **connecter** ou vous **inscrire** en utilisant les options
    disponibles dans la barre latérale.
"""
)
