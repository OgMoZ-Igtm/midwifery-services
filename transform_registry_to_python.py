from modules.public.form_registry import form_registry

linked_forms = {
    name: entry for name, entry in form_registry.items() if entry.get("is_extended", False)
}

import json

# Charge le dictionnaire enrichi depuis le fichier JSON
with open("enriched_registry.json", "r") as f:
    registry = json.load(f)

# Génère le dictionnaire Python avec références de fonctions
print("": {{')
    for field in ["title", "role", "module"]:
        print(f'        "{field}": "{config[field]}",')
    print(f'        "render": {config["render"]},')
    print(f'        "validate": {config["validate"]},')
    print("    },")
print("}")
