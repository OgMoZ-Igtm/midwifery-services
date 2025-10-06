import streamlit as st


def get_active_role(session):
    """Retourne le rôle actif depuis session_state.permissions"""
    return session.permissions.get("role", "inconnu")


def get_user_email(session):
    """Retourne l'email utilisateur depuis session_state.permissions"""
    return session.permissions.get("email", "non défini")


def display_status(session):
    """Affiche le rôle et l'email dans l'interface Streamlit"""
    role = get_active_role(session)
    email = get_user_email(session)
    st.caption(f"🔐 Rôle : `{role}` — 📧 {email}")
