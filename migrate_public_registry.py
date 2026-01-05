import os
import re

PROJECT_ROOT = "./"
TARGET = "PUBLIC_FORMS_REGISTRY"

REPLACEMENT_BLOCK = """from modules.public.form_registry import form_registry

public_forms = {
    name: entry for name, entry in form_registry.items() if entry.get("role") == "PUBLIC"
}
"""

migrated_files = []


def replace_registry_usages(content):
    """
    Supprime la déclaration de PUBLIC_FORMS_REGISTRY et remplace ses usages par public_forms.
    """
    # 🔥 Supprimer la déclaration complète
    content = re.sub(
        r"PUBLIC_FORMS_REGISTRY\s*=\s*\{[^}]*\}\n?", "", content, flags=re.DOTALL
    )

    # 🔁 Remplacer les usages typiques
    content = re.sub(
        r"list\(PUBLIC_FORMS_REGISTRY\.keys\(\)\)", "list(public_forms.keys())", content
    )
    # Ligne corrigée : PUBLIC_FORMS_REGISTRY\[(.*?)\]
    content = re.sub(r"PUBLIC_FORMS_REGISTRY\[(.*?)\]", r"public_forms[\1]", content)

    return content


def migrate_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if TARGET not in content:
        return False

    print(f"\n📜 Fichier détecté : {filepath}")
    confirm = input("Souhaites-tu migrer ce fichier ? (o/n) : ").strip().lower()
    if confirm != "o":
        print("⏭️ Migration ignorée.")
        return False

    # 🧩 Appliquer les remplacements
    content = replace_registry_usages(content)

    # 🧩 Ajouter le bloc de remplacement si nécessaire
    if "form_registry" not in content:
        last_import = re.search(r"^(from .*? import.*?)$", content, flags=re.MULTILINE)
        if last_import:
            content = content.replace(
                last_import.group(0), last_import.group(0) + "\n\n" + REPLACEMENT_BLOCK
            )
        else:
            content = REPLACEMENT_BLOCK + "\n" + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    migrated_files.append(filepath)
    print("✅ Migration réussie.")
    return True


if __name__ == "__main__":
    print("🌿 Démarrage de la migration PUBLIC_FORMS_REGISTRY...\n")
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
