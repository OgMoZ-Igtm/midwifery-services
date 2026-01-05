import os
import re

root_dir = "/home/ygd/projets-midwifery-Services/modules"


def inject_mock_insert(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Vérifie si le fichier contient un formulaire Streamlit
    if "st.button" not in content:
        return False

    # Supprime les anciens blocs supabase désactivés
    content = re.sub(r"if not supabase:.*?return", "", content, flags=re.S)

    # Remplace les insertions directes par mock_or_insert
    content = re.sub(
        r"supabase\.table\([\"'](\w+)[\"']\)\.insert\(.*?\)\.execute\(\)",
        r"mock_or_insert('\1', data)",
        content,
        flags=re.S,
    )

    # Ajoute l’import si absent
    if "mock_or_insert" not in content:
        content = (
            "from modules.backend.supabase_utils import mock_or_insert\n\n" + content
        )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Corrigé et injecté : {file_path}")
    return True


# Parcours des dossiers de formulaires par rôle
for subdir, _, files in os.walk(root_dir):
    if "forms_" in subdir:  # cible uniquement les dossiers de formulaires
        for file in files:
            if file.endswith(".py"):
                inject_mock_insert(os.path.join(subdir, file))
