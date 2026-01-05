import os
import re

root_dir = "/home/ygd/projets-midwifery-Services/modules"


def inject_mock_fetch(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "dashboard" not in file_path:
        return False

    # Supprime les anciens blocs supabase désactivés
    content = re.sub(r"if not supabase:.*?return", "", content, flags=re.S)

    # Remplace les appels directs à supabase par mock_or_fetch
    content = re.sub(
        r"supabase\.table\([\"'](\w+)[\"']\)\.select\(.*?\)\.execute\(\)",
        r"mock_or_fetch('\1')",
        content,
        flags=re.S,
    )

    # Corrige indentation éventuelle (supprime espaces multiples en début de ligne)
    content = re.sub(
        r"(?m)^[ \t]+", lambda m: "    " if "\n" in m.string else m.group(0), content
    )

    # Ajoute l’import si absent
    if "mock_or_fetch" not in content:
        content = (
            "from modules.backend.supabase_utils import mock_or_fetch\n\n" + content
        )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Dashboard corrigé et injecté : {file_path}")
    return True


# Parcours des dossiers
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".py"):
            inject_mock_fetch(os.path.join(subdir, file))
