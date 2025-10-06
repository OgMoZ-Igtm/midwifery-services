import streamlit as st


def init_session_state():
    defaults = {
        "permissions": {},
        "current_view": "🏠 Tableau de bord",
        "is_authenticated": False,
        "username": "Invité",
        "email": "",
        "role": "guest",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
