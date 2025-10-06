# help_request_form.py
import streamlit as st

def render_help_request_form():
    st.header("🆘 Demande d'assistance")
    st.text_input("Nom")
    st.text_area("Description du problème")