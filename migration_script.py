import os

# 🔍 Cibles à remplacer
TARGETS = [
    "LINKED_FORMS_EXTENDED",
    "LINKED_FORMS",
    "FORM_REGISTRY_EXTENDED",
    "FORM_REGISTRY",
]

# 📦 Remplacement standard
REPLACEMENT = "from modules.backend.form_utils import get_linked_forms\nlinked_forms = get_linked_forms()"

# 📁 Extensions à scanner
EXTENSIONS = [".py"]

# 📂 Dossiers à exclure
EXCLUDE_DIRS = ["venv", "__pycache__", "node_modules", ".git"]


def should_exclude(path):
    return any(excluded in path for excluded in EXCLUDE_DIRS)


def scan_and_replace():
    for root, _, files in os.walk("."):
        if should_exclude(root):
            continue
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                if any(target in content for target in TARGETS):
                    new_lines = []
                    replaced = False
                    for line in content.splitlines():
                        if any(target in line for target in TARGETS):
                            if not replaced:
                                new_lines.append(REPLACEMENT)
                                replaced = True
                        else:
                            new_lines.append(line)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write("\n".join(new_lines) + "\n")
                    print(f"✅ Corrigé : {path}")


if __name__ == "__main__":
    scan_and_replace()
