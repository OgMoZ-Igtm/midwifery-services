# feedback_form.py
import streamlit as st


def render_feedback_form():
    st.header("📝 Feedback interne")
    st.text_area("Votre avis")
    st.selectbox(
        "Satisfaction", ["Très satisfait", "Satisfait", "Neutre", "Insatisfait"]
    )
