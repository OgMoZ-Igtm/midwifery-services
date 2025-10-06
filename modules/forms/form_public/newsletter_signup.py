# newsletter_signup.py
import streamlit as st


def render_newsletter_signup():
    st.header("📰 Inscription à la newsletter")
    st.text_input("Email")
    st.checkbox("Je souhaite recevoir des mises à jour")
