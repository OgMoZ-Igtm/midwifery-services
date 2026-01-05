import os
import re

# Racine des modules de formulaires
BASE_DIR = "modules"


def add_wrapper_to_file(file_path):
    """Ajoute un wrapper form_xxx() -> render_form() à la fin du fichier si absent."""
    filename = os.path.basename(file_path)
    # Exemple : form_prenatal_care.py -> prenatal_care
    match = re.match(r"form_(.+)\.py", filename)
    if not match:
        return False

    form_name = match.group(1)
    wrapper_name = f"form_{form_name}"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Vérifie si le wrapper existe déjà
    if wrapper_name in content:
        print(f"✔ Wrapper déjà présent dans {filename}")
        return False

    # Bloc à ajouter
    wrapper_block = f"""

# ==============================================================================
# 🧩 Fonction générée automatiquement pour correspondre au dashboard
# ==============================================================================
def {wrapper_name}():
    \"\"\"Wrapper pour afficher le vrai contenu du formulaire {form_name}.\"\"\"
    render_form()
"""

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(wrapper_block)

    print(f"➕ Wrapper ajouté dans {filename}")
    return True


def walk_and_patch(base_dir):
    """Parcourt tous les fichiers form_*.py et ajoute les wrappers manquants."""
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.startswith("form_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                add_wrapper_to_file(file_path)


if __name__ == "__main__":
    walk_and_patch(BASE_DIR)
    print("✅ Migration terminée : tous les wrappers ont été ajoutés si nécessaires.")
