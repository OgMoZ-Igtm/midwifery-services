import streamlit as st
import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
menu_path = os.path.join(script_dir, "..", "data", "menu_mapping.json")

with open(menu_path, "r", encoding="utf-8") as f:
    menu_mapping = json.load(f)


def get_visible_packs(role):
    if role == "ADMIN":
        return list(menu_mapping.keys())
    elif role == "MIDWIFE":
        return ["MIDWIFE", "MESSAGES"]
    elif role == "NURSE":
        return ["NURSE", "PATIENT", "MESSAGES"]
    elif role in ["STUDENT", "INTERN", "DOCTORAL"]:
        return [role, "MESSAGES"]
    else:
        return [role]


def afficher_menu(role):
    visible_packs = get_visible_packs(role)
    choix = None
    with st.sidebar:
        st.header("🧭 Navigation")
        for pack in visible_packs:
            st.markdown(f"### 📦 {pack}")
            for page in sorted(menu_mapping.get(pack, []), key=lambda x: x["order"]):
                if st.button(page["name"], key=page["id"]):
                    choix = page["file"]
        st.markdown("---")
        st.markdown(f"👤 Rôle : **{role}**")
        st.markdown(
            f"👤 Utilisateur : **{st.session_state.get('username', 'inconnu')}**"
        )
        if st.button("🔓 Déconnexion", key="logout_button"):
            st.session_state.clear()
            st.rerun()
    return choix
