from pathlib import Path

# 📁 Dossier racine à scanner
ROOT = Path("modules")

# 🔍 Ligne à injecter
IMPORT_LINE = "from modules.backend.supabase_core import supabase\n"


def inject_supabase_import(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # ⚠️ Ignore si déjà importé
    if "from modules.backend.supabase_core import supabase" in content:
        return False

    # ⚠️ Ignore si le mot 'supabase' n’est pas utilisé
    if "supabase" not in content:
        return False

    # 🧩 Injecte après les imports existants
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("import") or line.startswith("from"):
            continue
        # Injecte juste après le dernier import
        lines.insert(i, IMPORT_LINE)
        break

    # 📝 Réécrit le fichier
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Importation injectée : {file_path}")
    return True


# 🔁 Parcours tous les fichiers Python
for file in ROOT.rglob("*.py"):
    inject_supabase_import(file)
