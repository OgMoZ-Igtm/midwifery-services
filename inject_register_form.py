import os
import re
from pathlib import Path

FORM_PATHS = {
    "PUBLIC": "modules/public",
    "MIDWIFE": "modules/forms_midwife",
    "ADMIN": "modules/forms_admin",
}


def inject_decorator(filepath, role):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Vérifie si déjà décoré
    if "@register_form" in content:
        return False

    # 🔍 Trouve le nom du formulaire (à partir du nom de fichier)
    name = Path(filepath).stem.replace("form_", "").replace("_", " ").title()

    # 🔍 Trouve la première classe ou fonction contenant render_form
    match = re.search(r"(class|def)\s+(\w+).*?render_form", content, flags=re.DOTALL)
    if not match:
        return False

    target_line = match.group(0)
    decorator = (
        f'@register_form("{name}", role="{role}", icon="📄", description="{name}")\n'
    )

    # 🧩 Injecte le décorateur
    content = content.replace(target_line, decorator + target_line)

    # 🧩 Injecte l'importation si manquante
    if "register_form" not in content:
        import_line = "from modules.public.form_registry import register_form\n"
        content = import_line + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Décorateur injecté : {filepath}")
    return True


if __name__ == "__main__":
    print("🌿 Injection des décorateurs @register_form...\n")
    for role, folder_path in FORM_PATHS.items():
        folder = Path(folder_path)
        for file in folder.glob("form_*.py"):
            inject_decorator(file, role)
