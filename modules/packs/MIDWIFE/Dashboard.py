# BANNER_INJECTED
import streamlit as st

if st.session_state.get("readonly", False):
    st.warning(
        "🔒 Vous êtes en mode lecture seule. Les modifications sont désactivées."
    )


def render():
    st.set_page_config(page_title="🌾 Tableau de bord Sage-femme", page_icon="🌾")
    st.title("🌾 Espace Sage-femme")

    st.success(
        f"Bonjour {st.session_state.username}, votre tableau de bord est prêt 🌼"
    )

    prefs = st.session_state.get("user_preferences", {})
    st.write(f"Langue : **{prefs.get('language', 'Français')}**")
    st.write(f"Thème : **{prefs.get('theme', 'Clair')}**")
    st.write(
        f"Notifications : {'✅ Activées' if prefs.get('notifications') else '❌ Désactivées'}"
    )

    st.subheader("📋 Suivis récents")
    st.markdown("- Consultation prénatale du 2025-09-05")
    st.markdown("- Accouchement enregistré le 2025-09-03")
    st.markdown("- Postnatal en attente de validation")

    st.subheader("📅 Rendez-vous à venir")
    st.metric("Demain", "0 patientes")
    st.metric("Cette semaine", "0 suivis")

    st.subheader("📬 Messagerie")
    st.markdown("📨 0 nouveaux messages non lus")
    st.button("📥 Ouvrir la messagerie")


if __name__ == "__main__":
    render()
