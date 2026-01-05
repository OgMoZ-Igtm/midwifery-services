import importlib
from pathlib import Path
from modules.backend.form_decorator import form_registry

# 📁 Dossiers à scanner
FORM_PATHS = {
    "admin": "modules/forms_admin",
    "midwife": "modules/forms_midwife",
}


def scan_forms():
    for role, folder in FORM_PATHS.items():
        path = Path(folder)
        for file in path.glob("form_*.py"):
            module_name = f"{folder.replace('/', '.')}.{file.stem}"
            try:
                importlib.import_module(module_name)
            except Exception as e:
                print(f"⚠️ Échec d’importation de {module_name} : {e}")


def generate_linked_forms():
    scan_forms()
    linked_forms = {}
    roles_detectés = set()

    for key, config in form_registry.items():
        role = config.get("role", "ADMIN")
        roles_detectés.add(role)
        linked_forms[key] = {
            "roles_allowed": [role],
            "description": config.get("description", "Formulaire"),
            "icon": config.get("icon", "📄"),
        }

    print("🌐 Rôles détectés :", sorted(roles_detectés))
    return linked_forms


if __name__ == "__main__":
    linked_forms = generate_linked_forms()
    print("# 🌿 LINKED_FORMS_EXTENDED")
    print("LINKED_FORMS_EXTENDED = {")
    for key, meta in linked_forms.items():
        print(f'    "{key}": {meta},')
    print("}")
