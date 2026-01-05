# generate_missing_form_files.py

import os
from pathlib import Path
from modules.public.form_registry_data import form_registry


def ensure_form_file(module_path: str, func_name: str):
    parts = module_path.split(".")
    file_path = Path(os.path.join(*parts))  # modules/forms_role/form_name.py
    file_path = file_path.with_suffix(".py")

    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(
                f'import streamlit as st\n\ndef {func_name}():\n    st.info("Formulaire `{func_name}` en cours de construction.")\n'
            )
        print(f"🆕 Créé : {file_path}")
    else:
        print(f"✅ Existe déjà : {file_path}")


def generate_missing_form_files():
    print("🔧 Génération des fichiers manquants...\n")
    for form_name, config in form_registry.items():
        module_path = config.get("module")
        ensure_form_file(module_path, form_name)


if __name__ == "__main__":
    generate_missing_form_files()
