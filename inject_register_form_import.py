import os
from pathlib import Path

# 📁 Dossiers à scanner
FORM_FOLDERS = [
    "modules/forms_admin",
    "modules/forms_midwife",
    "modules/forms_patient",
    "modules/forms_nurse",
    "modules/forms_intern",
    "modules/forms_student",
    "modules/public",
]

IMPORT_LINE = "from modules.backend.form_decorator import register_form\n"


def needs_injection(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        uses_decorator = "@register_form" in content
        already_imported = (
            "from modules.backend.form_decorator import register_form" in content
        )
        return uses_decorator and not already_imported


def inject_import(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Trouver l’endroit idéal pour injecter (après les imports existants)
    insert_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("import") or line.strip().startswith("from"):
            insert_index = i + 1

    lines.insert(insert_index, IMPORT_LINE)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Injection faite dans : {file_path}")


def main():
    for folder in FORM_FOLDERS:
        path = Path(folder)
        for file in path.glob("form_*.py"):
            if needs_injection(file):
                inject_import(file)


if __name__ == "__main__":
    main()
