import os
import re

# Dossiers à scanner
source_dirs = [
    "modules/forms",
    "modules/forms_midwife",
    "modules/forms_admin",
    "modules/forms_doctoral",
]

# Dossier des fichiers générés
autogen_dir = "modules/forms_autogen"

# Fonctions attendues
from modules.dashboard.dashboard_render_map import get_render_func_names

expected_funcs = get_render_func_names()


# Détection
def find_existing_files_without_render():
    missing = []
    for func in expected_funcs:
        found = False
        for folder in source_dirs:
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.endswith(".py"):
                        path = os.path.join(root, file)
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if func in content and re.search(
                                rf"def\s+{func}\s*\(", content
                            ):
                                found = True
        if not found:
            missing.append(func)
    return missing


missing_funcs = find_existing_files_without_render()
print(f"Fonctions manquantes dans les fichiers existants : {missing_funcs}")
