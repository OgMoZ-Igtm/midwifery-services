# validate_form_registry.py

import importlib
from modules.public.form_registry_data import form_registry


def validate_registry():
    print("🔍 Validation des formulaires dans form_registry...\n")
    success = 0
    errors = 0

    for form_name, config in form_registry.items():
        module_path = config.get("module")
        expected_func = form_name

        try:
            module = importlib.import_module(module_path)
            if hasattr(module, expected_func):
                print(f"✅ {form_name} — OK")
                success += 1
            else:
                print(
                    f"❌ {form_name} — fonction `{expected_func}` absente dans {module_path}"
                )
                errors += 1
        except Exception as e:
            print(f"❌ {form_name} — erreur d'import: {e}")
            errors += 1

    print(f"\n🎯 Résultat : {success} succès, {errors} erreurs")


if __name__ == "__main__":
    validate_registry()
