# =========================================================
# 📝 Page 1_Home.py - Accueil Midwifery
# =========================================================

import streamlit as st
import os

# =========================================================
# ⚙️ CONFIGURATION DE LA PAGE
# =========================================================
st.set_page_config(page_title="Accueil Midwifery", page_icon="🌿", layout="wide")

# =========================================================
# 🎨 CONTENU DE LA PAGE
# =========================================================

# # 📝 Message d'accueil et dut du projet
# st.header("🏡 Welcome to the Midwifery Services Data Tool Collection !")
# st.write("Thank you for taking the time to fill out this tool!")
# st.markdown(
#         """
#         For any questions, suggestions, or modification requests, please do not hesitate to contact Katia Lessard, PPRO-Midwifery, at:
#         **Katia.Lessard.reg18@ssss.gouv.qc.ca**
#         This tool has been created to support the continuous improvement and provision of high-quality midwifery care in Eeyou Istchee. It will allow us to operate a constant follow-up on the services, outcomes, and impacts of Midwifery Services amongst our clientele.
#         Some variables collected here were specifically requested by Nishiyuu. Other variables were selected through various consultations with Midwifery Services and are inspired by different databases and organizations, including:
#         * The National Indigenous Association of Midwives
#         * I-CLSC, Care 4, CHB, RSFQ
#         * The Canadian Midwifery Minimum Database
#         * MSSS
#         Data analysis is a public matter and will be reported back yearly to Eeyou Istchee Communities via the Midwifery Services' and Cree Health Board's Annual Report.
#         Thank you all for your commitment to providing high-quality midwifery care to families in Eeyou Istchee.
#         """
#     )
# st.write(
#         """
#         Use the "Previous" or "Next" navigation buttons below to move between different sections.
#         """
#         For any questions, suggestions, or modification requests, please do not hesitate to contact:

#         **Responsable :** Katia Lessard, PPRO-Midwifery
#     📧 **Contact :** Katia.Lessard.reg18@ssss.gouv.qc.ca
#     """
# )

# =========================================================
# 📸 IMAGE MAMAN + BÉBÉ
# =========================================================
st.image(
    "https://bing.com/th/id/BCO.d86e4f63-09c8-4384-84f2-3e39c85f00c7.png",
    caption="Midwifery - Mother & Baby",
    use_container_width=True,
)


# =========================================================
# 🔊 SON AUTOMATIQUE BÉBÉ
# =========================================================
def play_audio(file_path):
    """Joue un son si disponible."""
    if os.path.exists(file_path):
        with open(file_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3", autoplay=True)


# Chemin du son (mets ton fichier dans utils/assets/bebe_pleure.mp3)
AUDIO_PATH = "utils/assets/bebe_pleure.mp3"

if "mute" not in st.session_state:
    st.session_state.mute = False

col1, col2 = st.columns([3, 1])
with col2:
    if st.button(
        "🔇 Couper le son" if not st.session_state.mute else "🔊 Activer le son"
    ):
        st.session_state.mute = not st.session_state.mute

if not st.session_state.mute:
    play_audio(AUDIO_PATH)

# =========================================================
# 🚦 NAVIGATION : PRÉCÉDENT / SUIVANT
# =========================================================
st.markdown("---")
col_prev, col_next = st.columns([1, 1])

with col_prev:
    if st.button("⬅️ Page précédente"):
        st.switch_page("Midwifery_Services.py")

with col_next:
    if st.button("➡️ Page suivante"):
        st.switch_page("pages/.py")
