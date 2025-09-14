# BANNER_INJECTED
import streamlit as st
import time

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="🌸 Bienvenue", page_icon="🌸")
    st.title("🌸 Midwifery Services")

    st.markdown("### Chargement de votre espace personnel...")
    with st.spinner("Préparation de votre environnement..."):
        time.sleep(2)

    st.success("✅ Espace prêt !")
    st.balloons()
    # Le fichier audio n'a pas été fourni, cette ligne a été commentée.
    # st.audio("audio/harpe_nature.mp3")
    st.markdown("Cliquez sur votre rôle dans le menu pour commencer 🌼")
