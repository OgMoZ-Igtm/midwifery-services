import json

# Charge le dictionnaire enrichi depuis le fichier JSON
with open("enriched_registry.json", "r") as f:
    registry = json.load(f)

# Génère les lignes d'import
lines = []
for key, config in registry.items():
    module_path = config.get("module")
    if not module_path:
        continue

    module_name = module_path.split(".")[-1]
    render_alias = f"render_{module_name}"
    validate_alias = f"validate_{module_name}"

    line = (
        f"from {module_path} import render_form as {render_alias}, "
        f"validate_form as {validate_alias}"
    )
    lines.append(line)

# Sauvegarde dans un fichier texte
with open("generated_imports.txt", "w") as f:
    f.write("# 🔄 Imports générés automatiquement\n")
    for line in sorted(lines):
        f.write(line + "\n")

print("✅ Imports sauvegardés dans generated_imports.txt")
