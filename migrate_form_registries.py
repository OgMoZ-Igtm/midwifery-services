import os
import re

PROJECT_ROOT = "./"

REGISTRIES = {
    "PUBLIC_FORMS_REGISTRY": {
        "filter": 'entry.get("role") == "PUBLIC"',
        "variable": "public_forms",
    },
    "SHARED_FORMS_REGISTRY": {
        "filter": 'entry.get("role") == "SHARED"',
        "variable": "shared_forms",
    },
    "LINKED_FORMS_EXTENDED": {
        "filter": 'entry.get("is_extended", False)',
        "variable": "linked_forms",
    },
}

REPLACEMENT_TEMPLATE = """from modules.public.form_registry import form_registry

{variable} = {{
    name: entry for name, entry in form_registry.items() if {filter}
}}
"""

migrated_files = []


def replace_registry_usages(content, registry_name, variable_name, filter_condition):
    # 🔥 Supprimer la déclaration complète
    content = re.sub(
        rf"{registry_name}\s*=\s*\{{[^}}]*\}}\n?", "", content, flags=re.DOTALL
    )

    # 🔁 Remplacer les usages typiques
    content = re.sub(
        rf"list\({registry_name}\.keys\(\)\)", f"list({variable_name}.keys())", content
    )
    # CORRECTION : Suppression du saut de ligne dans l'expression régulière pour cibler l'accès par clé.
    content = re.sub(rf"{registry_name}\[(.*?)\]", f"{variable_name}[\\1]", content)

    return content


def migrate_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    found = [r for r in REGISTRIES if r in content]
    if not found:
        return False

    print(f"\n📜 Fichier détecté : {filepath}")
    confirm = (
        input(f"Migrer ces registres : {', '.join(found)} ? (o/n) : ").strip().lower()
    )
    if confirm != "o":
        print("⏭️ Migration ignorée.")
        return False

    for registry_name in found:
        variable = REGISTRIES[registry_name]["variable"]
        filter_condition = REGISTRIES[registry_name]["filter"]
        content = replace_registry_usages(
            content, registry_name, variable, filter_condition
        )

        # 🧩 Ajouter le bloc de remplacement si nécessaire
        # NOTE: Cette logique ajoute le bloc DEUX FOIS si deux registres différents
        # sont migrés dans le même fichier et que "form_registry" n'y est pas (ce qui pourrait être un problème).
        # Je ne modifie pas la logique, mais elle pourrait nécessiter une révision.
        if "form_registry" not in content:
            last_import = re.search(
                r"^(from .*? import.*?)$", content, flags=re.MULTILINE
            )
            replacement_block = REPLACEMENT_TEMPLATE.format(
                variable=variable, filter=filter_condition
            )
            if last_import:
                content = content.replace(
                    last_import.group(0),
                    last_import.group(0) + "\n\n" + replacement_block,
                )
            else:
                content = replacement_block + "\n" + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    migrated_files.append(filepath)
    print("✅ Migration réussie.")
    return True


if __name__ == "__main__":
    print("🌿 Démarrage de la migration multi-registres...\n")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                migrate_file(path)

    print("\n🎉 Migration terminée.")
    if migrated_files:
        print("🗂️ Fichiers migrés :")
        for f in migrated_files:
            print(f"  - {f}")
    else:
        print("Aucun fichier migré.")
