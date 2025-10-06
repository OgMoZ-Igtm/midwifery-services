# contact_form.py
import streamlit as st


def render_contact_form():
    st.header("📬 Formulaire de contact")
    st.text_input("Nom")
    st.text_input("Email")
    st.text_area("Message")
