# Fichier: form_constants_generator.py
import importlib
import sys
import os
from typing import Dict, Any, List

# Ajout du répertoire racine du projet au chemin d'accès
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 1. Tenter d'importer le registre central
try:
    from modules.public.form_registry import (
        LINKED_FORMS_EXTENDED,
        SHARED_FORMS_REGISTRY,
        PUBLIC_FORMS_REGISTRY,
    )

    FORM_REGISTRIES = {
        "LINKED_FORMS_EXTENDED": LINKED_FORMS_EXTENDED,
        "SHARED_FORMS_REGISTRY": SHARED_FORMS_REGISTRY,
        "PUBLIC_FORMS_REGISTRY": PUBLIC_FORMS_REGISTRY,
    }
except ImportError as e:
    print(f"⚠️ Échec d’importation du registre central : {e}")
    FORM_REGISTRIES = {}

# 2. Concaténer tous les registres pour l'analyse
ALL_FORMS = {}
for registry in FORM_REGISTRIES.values():
    ALL_FORMS.update(registry)

# --- Fichiers de sortie pour les constantes ---
OUTPUT_DIR = "constants"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "form_constants.py")


def generate_form_constants(all_forms: Dict[str, Any]):
    forms_metadata: Dict[str, Any] = {}
    print("\n🔍 Vérification et extraction des métadonnées des formulaires...")

    for key, metadata in all_forms.items():
        module_path = metadata.get("module")
        if not module_path:
            forms_metadata[key] = metadata
            continue

        try:
            module = importlib.import_module(module_path)
            forms_metadata[key] = metadata
            forms_metadata[key]["status"] = "OK"

        except ImportError as e:
            print(f"⚠️ Échec d’importation de {module_path} : {e}")
            forms_metadata[key] = metadata
            forms_metadata[key]["status"] = "ERROR"

        except Exception as e:
            if "SUPABASE_URL" in str(e) or "SUPABASE_KEY" in str(e):
                print(f"⏸️ Supabase désactivé pour : {module_path}")
            else:
                print(f"⚠️ Erreur inattendue lors de l'import de {module_path} : {e}")
            forms_metadata[key] = metadata
            forms_metadata[key]["status"] = "ERROR"

    # 3. Générer le fichier de constantes
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Fichier généré automatiquement par form_constants_generator.py\n")
        f.write("# Contient les métadonnées de base de tous les formulaires.\n\n")
        f.write("ALL_FORM_METADATA = {\n")
        for key, meta in forms_metadata.items():
            simple_meta = {
                k: v
                for k, v in meta.items()
                if k not in ["render", "validate", "module"] and not callable(v)
            }
            f.write(f'    "{key}": {simple_meta},\n')
        f.write("}\n")

    print(f"\n✅ Fichier de constantes généré : {OUTPUT_FILE}")
    print(f"Total de formulaires traités : {len(forms_metadata)}")


if __name__ == "__main__":
    if FORM_REGISTRIES:
        ALL_FORMS_TO_CHECK = {}
        for reg_name, reg_data in FORM_REGISTRIES.items():
            print(f"Chargement du registre : {reg_name} ({len(reg_data)} entrées)")
            ALL_FORMS_TO_CHECK.update(reg_data)

        generate_form_constants(ALL_FORMS_TO_CHECK)
    else:
        print(
            "\n❌ Impossible de continuer car le registre central n'a pas pu être chargé."
        )
