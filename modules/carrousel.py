# modules/carrousel.py
import streamlit as st
import time


def afficher_carrousel():
    images = [
        "/home/ygd/projets-midwifery-Services/static/Grand_mere_et enfant.jpg",
        "/home/ygd/projets-midwifery-Services/static/Accueil_territoire.png",
        "/home/ygd/projets-midwifery-Services/static/Mere_crie.png",
    ]

    captions = [
        "👵 Grand-mère et enfant — sagesse transmise par les aînées cries",
        "🌿 Accueil sur le territoire — lien sacré avec la terre et les ancêtres",
        "👩‍👧 Mère crie — force, tendresse et continuité des générations",
    ]

    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0

    index = st.session_state.carousel_index
    st.image(images[index], caption=captions[index], use_container_width=True)

    time.sleep(3)
    st.session_state.carousel_index = (index + 1) % len(images)
    st.rerun()
