import os

# Dossier cible
target_dir = "modules/forms_autogen"

# Fonctions manquantes à générer
from modules.dashboard.pack_registry import PACK_RENDER_MAP
from modules.dashboard.dashboard_render_map import get_render_func_names

missing_funcs = [f for f in get_render_func_names() if f not in PACK_RENDER_MAP]

# Crée le dossier s’il n’existe pas
os.makedirs(target_dir, exist_ok=True)

for func_name in missing_funcs:
    filename = f"{target_dir}/form_{func_name}.py"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(
                f"""import streamlit as st

def {func_name}():
    st.info("🧩 Formulaire `{func_name}` à compléter.")
"""
            )
        print(f"✅ Fichier généré : {filename}")
    else:
        print(f"⏩ Fichier déjà existant : {filename}")
