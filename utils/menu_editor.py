import streamlit as st
from utils.menu_config import load_config, save_config
import pandas as pd

st.title("🛠️ Navigation Editor")

config = load_config()
roles = list(config.keys())

# 🔹 Ajout d’un nouveau rôle
st.subheader("➕ Add a new role")
new_role = st.text_input("New role name")
if st.button("Add role"):
    if new_role and new_role not in config:
        config[new_role] = {}
        save_config(config)
        st.success(f"✅ Role '{new_role}' added.")
        st.rerun()

# 🔹 Sélection du rôle existant
st.subheader("🎭 Edit existing role")
selected_role = st.selectbox("Select a role", roles)

# 🔹 Ajout d’une nouvelle section
new_section = st.text_input("New section name")
if st.button("Add section"):
    if new_section and new_section not in config[selected_role]:
        config[selected_role][new_section] = []
        save_config(config)
        st.success(f"✅ Section '{new_section}' added.")
        st.rerun()

# 🔹 Sélection de la section existante
sections = list(config[selected_role].keys())
selected_section = st.selectbox("Select a section", sections)

# 🔹 Ajout d’un bouton
st.subheader("📌 Add a new button")
new_label = st.text_input("Button label")
new_page = st.text_input("Page code")
if st.button("Add button"):
    if new_label and new_page:
        config[selected_role][selected_section].append(
            {"label": new_label, "page": new_page}
        )
        save_config(config)
        st.success("✅ Button added.")
        st.rerun()

# 🔹 Réorganisation des boutons
st.subheader("🔀 Reorder buttons")
buttons_df = pd.DataFrame(config[selected_role][selected_section])
edited_df = st.data_editor(buttons_df, num_rows="dynamic", use_container_width=True)

if st.button("💾 Save new order"):
    config[selected_role][selected_section] = edited_df.to_dict(orient="records")
    save_config(config)
    st.success("✅ Button order saved.")
    st.rerun()

# 🔹 Liste des boutons existants avec suppression
st.subheader("🗑️ Existing buttons")
for i, item in enumerate(config[selected_role][selected_section]):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"🔹 {item['label']} → `{item['page']}`")
    with col2:
        if st.button("❌ Delete", key=f"delete_{i}"):
            config[selected_role][selected_section].pop(i)
            save_config(config)
            st.success("✅ Button deleted.")
            st.rerun()
