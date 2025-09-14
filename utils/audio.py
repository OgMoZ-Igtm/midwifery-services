import streamlit as st
from utils.audio_utils import play_audio


def render():
    st.title("🔊 Lecteur audio interactif")
    st.write("Choisissez un son à écouter :")

    sons = {
        "👶 Bébé qui pleure": "utils/assets/bebe_pleure.mp3",
        "💓 Battement de cœur": "utils/assets/battement_coeur.mp3",
        "🗣️ Voix douce": "utils/assets/voix_douce.mp3",
    }

    choix = st.selectbox("Sélectionnez un son :", list(sons.keys()))
    if st.button("▶️ Écouter"):
        play_audio(sons[choix])
