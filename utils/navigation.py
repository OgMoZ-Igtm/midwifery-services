import streamlit as st
import json
import os
import uuid

MENU_FILE = "utils/menu_mapping.json"


def load_menu_mapping():
    """Charge le mapping JSON des menus."""
    if not os.path.exists(MENU_FILE):
        st.error(
            "❌ `menu_mapping.json` est introuvable. Veuillez lancer le script de génération."
        )
        return {}
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def display_menus(role: str):
    """Affiche les menus latéraux selon le rôle de l'utilisateur."""
    mapping = load_menu_mapping()  # ← cette ligne initialise 'mapping'
    if not mapping:
        return

    st.sidebar.title("📂 Navigation")
    role = role.upper()

    if "expander_states" not in st.session_state:
        st.session_state.expander_states = {pack: False for pack in mapping.keys()}

    for pack, entries in mapping.items():
        # Affichage du pack MESSAGES pour tous les rôles
        if pack == "MESSAGES":
            filtered_entries = entries
        else:
            filtered_entries = [
                entry for entry in entries if role in entry.get("roles", [])
            ]

        if not filtered_entries:
            continue

        is_expanded = st.session_state.expander_states.get(pack, False)

        with st.sidebar.expander(f"📦 {pack}", expanded=is_expanded):
            for entry in sorted(filtered_entries, key=lambda x: x.get("order", 999)):
                label = (
                    f"{entry.get('order', ''):02d} - {entry.get('name', 'Nom inconnu')}"
                )
                button_key = entry.get("id", str(uuid.uuid4()))

                if st.button(label, key=button_key):
                    st.session_state.current_page = entry.get("file", "Home")
                    for other_pack in mapping.keys():
                        st.session_state.expander_states[other_pack] = False
                    st.session_state.expander_states[pack] = True
