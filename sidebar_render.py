import streamlit as st
from typing import Dict, Any

# 🌸 Style doux pour la sidebar
st.sidebar.markdown(
    """
<style>
    .sidebar-title {
        font-size: 1.2rem;
        color: #d6336c;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sidebar-button {
        background-color: #ffe4e1;
        color: #6f1d1b;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.3rem 0.6rem;
        margin-bottom: 0.3rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# 🌐 Bandeau de navigation publique
def render_top_strip():
    st.markdown("### 🌐 Navigation publique")
    cols = st.columns(10)
    top_items = [
        ("🏠 HOME", "top_home"),
        ("🎯 Mission", "top_mission"),
        ("📦 Modules", "top_modules"),
        ("❓ FAQ", "top_faq"),
        ("📬 Contact", "top_contact"),
        ("🧰 Soutien technique", "top_support"),
        ("👥 Qui-sommes-nous ?", "top_about"),
        ("🎭 Cultural", "top_cultural"),
        ("🗣️ Les Papotines", "top_papotines"),
        ("🔗 Liens utiles", "top_links"),
    ]
    for i, (label, key) in enumerate(top_items):
        with cols[i]:
            st.button(label, key=key)


# 🧭 Sidebar dynamique avec rôle sélectionnable
def render_sidebar(current_role: str, form_map: Dict[str, Dict[str, Any]]) -> Any:
    st.sidebar.markdown("## 🧭 Navigation")

    # 🎭 Menu déroulant pour changer de rôle à la volée
    available_roles = list(form_map.keys())
    role = st.sidebar.selectbox(
        "👤 Rôle actif", available_roles, index=available_roles.index(current_role)
    )
    st.session_state["user_role"] = role

    # 🔐 Accès rapide au générateur de mot de passe
    if st.sidebar.button("🔐 Générateur de mot de passe"):
        st.session_state["user_action"] = "boot_password"

    # 📌 Formulaires spécifiques
    options = form_map.get(role, form_map["default"])
    specific_keys = [
        key for key in options.keys() if "Tableau de Bord" in key or "Accueil" in key
    ]
    shared_keys = [key for key in options.keys() if key not in specific_keys]

    selected_specific = st.sidebar.selectbox(
        "📌 Formulaires spécifiques", specific_keys
    )

    # 🔄 Formulaires partagés
    st.sidebar.markdown("### 🔄 Formulaires partagés")
    selected_shared = None
    for key in shared_keys:
        if st.sidebar.button(f"🔘 {key}", key=f"shared_{key}"):
            selected_shared = key

    return selected_shared or selected_specific
