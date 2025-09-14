import streamlit as st


def bouton_unique(label, prefix="", index=None):
    """
    Crée un bouton Streamlit avec une clé unique basée sur un préfixe et un index.

    Args:
        label (str): Texte affiché sur le bouton.
        prefix (str): Identifiant de contexte (ex: "nav", "auto", "action").
        index (int or str): Identifiant dynamique (ex: index du carrousel).

    Returns:
        bool: True si le bouton est cliqué, False sinon.
    """
    key = f"{prefix}_{index}" if index is not None else prefix
    return st.button(label, key=key)


def bouton_menu(label: str, page_code: str, context: str = ""):
    key = (
        f"{context}_{page_code.replace('.', '_')}"
        if context
        else page_code.replace(".", "_")
    )
    if st.button(label, key=key):
        st.session_state.current_page = page_code
        st.rerun()
