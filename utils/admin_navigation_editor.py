import streamlit as st
from utils.navigation_data import charger_config, sauvegarder_config
import pandas as pd

st.title("🛠️ Éditeur de navigation")

config = charger_config()
roles = list(config.keys())

# 🔹 Ajout d’un nouveau rôle
st.subheader("➕ Ajouter un rôle")
new_role = st.text_input("Nom du nouveau rôle")
if st.button("Ajouter le rôle"):
    if new_role and new_role not in config:
        config[new_role] = {}
        sauvegarder_config(config)
        st.success(f"✅ Rôle '{new_role}' ajouté.")
        st.rerun()

# 🔹 Sélection du rôle existant
st.subheader("🎭 Modifier un rôle existant")
selected_role = st.selectbox("Choisir un rôle", roles)


# 🔹 Ajout d’une nouvelle section
new_section = st.text_input("Nom de la nouvelle section")
if st.button("Ajouter la section"):
    if new_section and new_section not in config[selected_role]:
        config[selected_role][new_section] = []
        sauvegarder_config(config)
        st.success(f"✅ Section '{new_section}' ajoutée.")
        st.rerun()


# 🔹 Sélection de la section existante
sections = list(config[selected_role].keys())
selected_section = st.selectbox("Choisir une section", sections)

# 🔹 Ajout d’un bouton
st.subheader("📌 Ajouter un bouton")
new_label = st.text_input("Nom du bouton")
new_page = st.text_input("Code de la page")
if st.button("Ajouter le bouton"):
    if new_label and new_page:
        config[selected_role][selected_section].append(
            {"label": new_label, "page": new_page}
        )
        sauvegarder_config(config)
        st.success("✅ Bouton ajouté.")
        st.rerun()



st.subheader("🔀 Reorder buttons")
buttons_df = pd.DataFrame(config[selected_role][selected_section])
edited_df = st.data_editor(buttons_df, num_rows="dynamic", use_container_width=True)

if st.button("💾 Save new order"):
    config[selected_role][selected_section] = edited_df.to_dict(orient="records")
    save_config(config)
    st.success("✅ Button order saved.")
    st.rerun()

# 🔹 Liste des boutons existants avec suppression
st.subheader("🗑️ Boutons existants")
for i, item in enumerate(config[selected_role][selected_section]):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"🔹 {item['label']} → `{item['page']}`")
    with col2:
        if st.button("❌ Supprimer", key=f"delete_{i}"):
            config[selected_role][selected_section].pop(i)
            sauvegarder_config(config)
            st.success("✅ Bouton supprimé.")
            st.rerun()
