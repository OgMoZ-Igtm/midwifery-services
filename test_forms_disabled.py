import importlib
import pkgutil
import traceback
import sys

BASE_PACKAGES = [
    "modules.forms_admin",
    "modules.forms_midwife",
    "modules.forms_doctor",
    "modules.forms_nurse",
    "modules.forms_patient",
    "modules.forms_doctoral",
    "modules.forms_intern",
    "modules.forms_student",
    "modules.forms_guest",
]

results = {"tested": 0, "success": 0, "errors": 0}


def test_form_module(module_name, execute=False):
    try:
        mod = importlib.import_module(module_name)
        for attr in dir(mod):
            if attr.startswith("form_"):
                func = getattr(mod, attr)
                if callable(func):
                    results["tested"] += 1
                    print(f"▶ {module_name}.{attr} trouvé")
                    if execute:
                        try:
                            print(f"⏩ Exécution de {attr}()…")
                            func()
                            results["success"] += 1
                            print(f"✔ {attr} exécuté sans erreur")
                        except Exception as e:
                            results["errors"] += 1
                            print(f"❌ Erreur dans {attr}: {e}")
                            traceback.print_exc()
                    else:
                        results["success"] += 1
                        print(f"✔ {attr} est bien défini et appelable")
    except Exception as e:
        print(f"❌ Impossible d’importer {module_name}: {e}")
        traceback.print_exc()
        results["errors"] += 1


def main(execute=False):
    for base in BASE_PACKAGES:
        for _, name, ispkg in pkgutil.iter_modules([base.replace(".", "/")]):
            if name.startswith("form_"):
                module_name = f"{base}.{name}"
                test_form_module(module_name, execute=execute)

    # Rapport final
    print("\n" + "=" * 60)
    print("📊 RAPPORT FINAL")
    print(f"Nombre de formulaires testés : {results['tested']}")
    print(f"✔ Succès : {results['success']}")
    print(f"❌ Erreurs : {results['errors']}")
    print("=" * 60)


if __name__ == "__main__":
    # Détection du mode : si lancé avec Streamlit, on exécute vraiment
    execute_mode = "streamlit" in sys.argv[0]
    main(execute=execute_mode)
