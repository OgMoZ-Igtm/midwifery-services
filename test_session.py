# ⚠️ import cassé : streamlit as st
from modules.utils.session import inject_session_keys


    inject_session_keys()
def run():
    st.write("✅ Session keys injectées")
    st.write("Username:", st.session_state.username)
    st.write("Role:", st.session_state.role)
    st.write("Last session:", st.session_state.last_session)


run()
