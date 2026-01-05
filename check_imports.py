# ⚠️ import cassé : os
# ⚠️ import cassé : re

# Dossiers obsolètes ou interdits
INVALID_MODULES = ["pages", "ui.", "forms.", "services."]  # sans préfixe "modules."

# Dossier racine à scanner
ROOT_DIR = "modules"


def scan_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    issues = []
    for i, line in enumerate(lines):
        if "import" in line or "from" in line:
            for invalid in INVALID_MODULES:
                if re.search(rf"\b{invalid}\b", line):
                    issues.append((i + 1, line.strip()))
    return issues


def scan_project():
    print(f"🔍 Vérification des imports dans `{ROOT_DIR}/`...\n")
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                issues = scan_file(path)
                if issues:
                    print(f"❌ {path}")
                    for line_num, content in issues:
                        print(f"   Ligne {line_num}: {content}")
                    print()
    print("✅ Scan terminé.")


if __name__ == "__main__":
    scan_project()
