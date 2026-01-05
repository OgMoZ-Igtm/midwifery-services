# ⚠️ import cassé : os

DASHBOARD_DIR = "modules/forms/dashboards"

if not os.path.exists(DASHBOARD_DIR):
    print(f"❌ Dossier introuvable : {DASHBOARD_DIR}")
    exit()

for filename in os.listdir(DASHBOARD_DIR):
    if filename.startswith("dashboard_") and filename.endswith(".py"):
        path = os.path.join(DASHBOARD_DIR, filename)

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if any("def run(" in line for line in lines):
            print(f"✅ {filename} contient déjà run() — ignoré.")
            continue

        # Sauvegarde de sécurité
        backup_path = path + ".bak"
        with open(backup_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"🛟 Sauvegarde créée : {backup_path}")

        # Injection de run()
        new_lines = []
        has_import = any("import streamlit" in line for line in lines)
        if not has_import:
            new_lines.append("import streamlit as st\n\n")

        new_lines.append("def run():\n")
        for line in lines:
            if line.strip():
                new_lines.append("    " + line)
            else:
                new_lines.append("\n")

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print(f"🔧 {filename} refactoré avec run()")

print("\n🎉 Tous les dashboards sont prêts pour la navigation dynamique !")
