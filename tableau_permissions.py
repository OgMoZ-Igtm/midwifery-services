import streamlit as st
from modules.services.security import PACK_PERMISSIONS_MAP

st.set_page_config(page_title="Carte des Permissions", layout="wide")

st.title("🔐 Carte des Packs et Permissions Requises")

pack_data = []
for pack_id, data in PACK_PERMISSIONS_MAP.items():
    pack_data.append(
        {
            "ID du Pack": pack_id,
            "Label": data.get("label", "—"),
            "Icône": data.get("icon", "—"),
            "Permissions Requises": ", ".join(data.get("required_permissions", []))
            or "✅ Aucune",
        }
    )

st.dataframe(pack_data, use_container_width=True)

search = st.text_input("🔍 Filtrer par nom de pack ou permission")
if search:
    filtered = [
        row
        for row in pack_data
        if search.lower() in row["ID du Pack"].lower()
        or search.lower() in row["Permissions Requises"].lower()
    ]
    st.dataframe(filtered, use_container_width=True)
