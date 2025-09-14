def init_session_state(defaults):
    import streamlit as st

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
